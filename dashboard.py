import streamlit as st
import json
import pandas as pd
import plotly.express as px

FINAL_SUMMARY_PATH = 'final_asset_summary.json'

# Load Final Summary JSON
@st.cache_data
def load_final_summary():
    with open(FINAL_SUMMARY_PATH, 'r') as f:
        return json.load(f)

# App Configuration
st.set_page_config(page_title="🔧 Asset Maintenance Summary Dashboard", layout="wide")
st.title("🔧 Comprehensive Asset Maintenance Summary")

summary_data = load_final_summary()
asset_ids = list(summary_data.keys())
selected_asset = st.sidebar.selectbox('Select Asset ID:', asset_ids)

asset_details = summary_data[selected_asset]

st.header(f"📊 Summary for Asset ID: {selected_asset}")

# KPIs
col1, col2 = st.columns(2)
col1.metric("Total Work Orders", asset_details['total_work_orders'])
col2.metric("Average Predicted Days to Failure", asset_details['average_predicted_days_to_failure'])

# Summary Paragraph
st.markdown("### 📝 Asset Performance Summary")
most_common_issue = max(asset_details['issues'], key=asset_details['issues'].get)
summary_paragraph = (
    f"The asset **{selected_asset}** has undergone **{asset_details['total_work_orders']}** maintenance work orders. "
    f"The most commonly observed issue is '**{most_common_issue}**'. "
    f"All identified issues have been of '**{list(asset_details['severity_count'].keys())[0]}**' severity. "
    f"The asset is predicted to function for an average of **{asset_details['average_predicted_days_to_failure']} days** before potential failure."
)
st.info(summary_paragraph)

# Issues Breakdown
st.markdown("### 🔍 Issue Distribution")
issues_df = pd.DataFrame(list(asset_details['issues'].items()), columns=['Issue Description', 'Count'])
fig_issues = px.bar(issues_df, x='Count', y='Issue Description', orientation='h',
                    title=f"Issues Frequency for {selected_asset}",
                    color='Count', color_continuous_scale='Blues')
st.plotly_chart(fig_issues, use_container_width=True)

# Severity Breakdown
st.markdown("### ⚠️ Severity Distribution")
severity_df = pd.DataFrame(list(asset_details['severity_count'].items()), columns=['Severity Level', 'Count'])
fig_severity = px.pie(severity_df, names='Severity Level', values='Count', 
                      title=f"Severity Levels for {selected_asset}",
                      color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(fig_severity, use_container_width=True)

# ---- Additional: Top Issues Across All Assets (Excluding Scheduled Maintenance) ----
st.markdown("### 🚨 Top Issues Across All Assets (Excluding Scheduled Maintenance)")

# Aggregate issues across all assets
issue_records = []
for asset, details in summary_data.items():
    for issue, count in details['issues'].items():
        if not issue.startswith("nan"):
            issue_records.append({'Asset ID': asset, 'Issue': issue, 'Count': count})

issues_df = pd.DataFrame(issue_records)
total_issue_counts = issues_df.groupby('Issue')['Count'].sum().reset_index().sort_values(by='Count', ascending=False)

# Plot with Plotly
import plotly.express as px
fig_total_issues = px.bar(total_issue_counts, x='Count', y='Issue', orientation='h',
                          title='Total Issue Frequency Across All Assets',
                          color='Count', color_continuous_scale='Viridis')
st.plotly_chart(fig_total_issues, use_container_width=True)


st.success("✅ Dashboard rendered successfully.")
