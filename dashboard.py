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

# Summary Paragraph
st.markdown("### 🔍 Asset Summary Paragraph")
most_common_issue = max(asset_details['issues'], key=asset_details['issues'].get)
most_severe = max(asset_details['severity_count'], key=asset_details['severity_count'].get)
summary_paragraph = (
    f"Asset {selected_asset} has been serviced with a total of {asset_details['total_work_orders']} work orders. "
    f"The most frequent issue recorded is '{most_common_issue}', primarily with severity '{most_severe}'. "
    f"Expected average days until failure is approximately {round(asset_details['average_predicted_days_to_failure'], 2)} days."
)
st.info(summary_paragraph)

# Issues Summary
st.markdown("### 📋 Issues Summary")
issues_df = pd.DataFrame.from_dict(asset_details['issues'], orient='index', columns=['Count']).reset_index().rename(columns={'index': 'Issue Description'})
st.dataframe(issues_df)

# Severity Distribution
st.markdown("### ⚠️ Severity Distribution")
severity_df = pd.DataFrame.from_dict(asset_details['severity_count'], orient='index', columns=['Count']).reset_index().rename(columns={'index': 'Severity Level'})
st.dataframe(severity_df)

# Frequent Asset Usage Over Time
st.markdown("### 📈 Frequent Asset Usage Over Time")
if 'date' in raw_data.columns and 'Asset ID' in raw_data.columns:
    raw_data['date'] = pd.to_datetime(raw_data['date'], errors='coerce')
    raw_data['Month'] = raw_data['date'].dt.to_period('M')
    usage_trend = raw_data.groupby(['Month', 'Asset ID']).size().reset_index(name='Work Orders')

    plt.figure(figsize=(12,6))
    sns.lineplot(data=usage_trend, x='Month', y='Work Orders', hue='Asset ID', marker='o')
    plt.xticks(rotation=45)
    plt.title('Monthly Work Orders per Asset')
    plt.tight_layout()
    st.pyplot(plt)
else:
    st.warning("⚠️ 'date' or 'Asset ID' column not found. Skipping usage trend visualization.")

# Most Common Failures in the Past Month
st.markdown("### 🔧 Most Common Failures in the Past Month")
if 'date' in raw_data.columns and 'failure_mode' in raw_data.columns:
    raw_data['date'] = pd.to_datetime(raw_data['date'], errors='coerce')
    raw_data['Month'] = raw_data['date'].dt.to_period('M')
    latest_month = raw_data['Month'].max()
    past_month_data = raw_data[raw_data['Month'] == latest_month]
    common_failures = past_month_data['failure_mode'].value_counts().head(5)

    if not common_failures.empty:
        fig, ax = plt.subplots()
        common_failures.plot(kind='bar', ax=ax, color='skyblue')
        ax.set_title(f'Most Common Failures in {latest_month}')
        ax.set_ylabel('Frequency')
        st.pyplot(fig)
    else:
        st.info("No failure data available for the latest month.")
else:
    st.warning("⚠️ 'date' or 'failure_mode' column not found. Skipping common failures visualization.")

# Most Problematic Assets Overall
st.markdown("### 🚨 Most Problematic Assets Overall")
if 'Asset ID' in raw_data.columns:
    problematic_assets = raw_data['Asset ID'].value_counts().head(5)

    if not problematic_assets.empty:
        fig2, ax2 = plt.subplots()
        problematic_assets.plot(kind='bar', ax=ax2, color='tomato')
        ax2.set_title('Top 5 Problematic Assets')
        ax2.set_ylabel('Number of Work Orders')
        st.pyplot(fig2)
    else:
        st.info("No asset data available to visualize problematic assets.")
else:
    st.warning("⚠️ 'Asset ID' column not found. Skipping problematic assets visualization.")

st.success("✅ Dashboard loaded successfully.")
