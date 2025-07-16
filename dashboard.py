import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

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

# Visualization: Frequent Asset Usage Over Time
st.markdown("### 📈 Frequent Asset Usage Over Time")
if 'date' in raw_data.columns:
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
    st.warning("⚠️ Date column not found in data. Skipping usage trend visualization.")

# Visualization: Most Common Failures in Past Month
st.markdown("### 🔧 Most Common Failures in the Past Month")
if 'date' in raw_data.columns:
    latest_month = raw_data['date'].dt.to_period('M').max()
    raw_data['Month'] = raw_data['date'].dt.to_period('M')
    past_month_data = raw_data[raw_data['Month'] == latest_month]
    common_failures = past_month_data['failure_mode'].value_counts().head(5)

    fig, ax = plt.subplots()
    common_failures.plot(kind='bar', ax=ax)
    ax.set_title(f'Most Common Failures in {latest_month}')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)
else:
    st.warning("⚠️ Date column not found. Skipping common failures for the past month visualization.")

# Visualization: Most Problematic Assets Overall
st.markdown("### 🚨 Most Problematic Assets Overall")
problematic_assets = raw_data['Asset ID'].value_counts().head(5)
fig2, ax2 = plt.subplots()
problematic_assets.plot(kind='bar', ax=ax2, color='tomato')
ax2.set_title('Top 5 Problematic Assets')
ax2.set_ylabel('Number of Work Orders')
st.pyplot(fig2)

st.success("✅ Dashboard loaded successfully.")
