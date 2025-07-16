import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

FINAL_SUMMARY_PATH = 'final_asset_summary.json'
RAW_DATA_PATH = 'sample_data.csv'

def load_final_summary():
    with open(FINAL_SUMMARY_PATH, 'r') as f:
        data = json.load(f)
    return data

def load_raw_data():
    return pd.read_csv(RAW_DATA_PATH)

st.set_page_config(page_title="🚀 Comprehensive Asset Maintenance Dashboard", layout="wide")
st.title("🚀 Comprehensive Asset Maintenance Dashboard")

summary_data = load_final_summary()
raw_data = load_raw_data()

asset_ids = list(summary_data.keys())
selected_asset = st.sidebar.selectbox('Select Asset ID:', asset_ids)
asset_details = summary_data[selected_asset]

st.header(f"Summary for Asset ID: {selected_asset}")

col1, col2 = st.columns(2)
col1.metric("Total Work Orders", asset_details['total_work_orders'])
col2.metric("Avg. Predicted Days to Failure", round(asset_details['average_predicted_days_to_failure'], 2))

st.markdown("### 🔍 Asset Summary Paragraph")
most_common_issue = max(asset_details['issues'], key=asset_details['issues'].get)
most_severe = max(asset_details['severity_count'], key=asset_details['severity_count'].get)
summary_paragraph = (
    f"Asset {selected_asset} has a total of {asset_details['total_work_orders']} work orders. "
    f"The most common issue is '{most_common_issue}', and the prevailing severity level is '{most_severe}'. "
    f"The average predicted days to failure is approximately {round(asset_details['average_predicted_days_to_failure'], 2)} days."
)
st.info(summary_paragraph)

st.markdown("### 📋 Issues Summary")
st.dataframe(pd.DataFrame.from_dict(asset_details['issues'], orient='index', columns=['Count']).reset_index().rename(columns={'index': 'Issue Description'}))

st.markdown("### ⚠️ Severity Distribution")
st.dataframe(pd.DataFrame.from_dict(asset_details['severity_count'], orient='index', columns=['Count']).reset_index().rename(columns={'index': 'Severity Level'}))

# Visualization: Work Orders per Asset
st.markdown("### 📊 Total Work Orders per Asset")
if 'Asset ID' in raw_data.columns:
    asset_counts = raw_data['Asset ID'].value_counts().reset_index()
    asset_counts.columns = ['Asset ID', 'Work Orders']

    plt.figure(figsize=(12,6))
    sns.barplot(data=asset_counts, x='Asset ID', y='Work Orders', palette='viridis')
    plt.title('Total Work Orders per Asset')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)
else:
    st.warning("⚠️ 'Asset ID' column not found in data. Skipping visualization.")

# Visualization: Most Common Failures
st.markdown("### 🔧 Most Common Failures Overall")
if 'failure_mode' in raw_data.columns:
    common_failures = raw_data['failure_mode'].value_counts().head(5)

    fig, ax = plt.subplots()
    common_failures.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title('Top 5 Most Common Failures Overall')
    ax.set_ylabel('Frequency')
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.warning("⚠️ 'failure_mode' column not found. Skipping common failures visualization.")

st.success("✅ Dashboard loaded successfully.")
