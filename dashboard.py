import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

RAW_DATA_PATH = 'sample_data.csv'

st.set_page_config(page_title="📊 Asset Work Orders Count", layout="wide")
st.title("📊 Total Work Orders per Asset")

def load_raw_data():
    return pd.read_csv(RAW_DATA_PATH)

raw_data = load_raw_data()

if 'Asset ID' in raw_data.columns:
    asset_counts = raw_data['Asset ID'].value_counts().reset_index()
    asset_counts.columns = ['Asset ID', 'Work Orders']

    st.markdown("### 🚀 Work Orders per Asset")

    plt.figure(figsize=(12,6))
    sns.barplot(data=asset_counts, x='Asset ID', y='Work Orders', palette='viridis')
    plt.title('Total Work Orders per Asset')
    plt.xlabel('Asset ID')
    plt.ylabel('Number of Work Orders')
    plt.xticks(rotation=45)
    st.pyplot(plt)
else:
    st.warning("⚠️ 'Asset ID' column not found in data. Please check your CSV.")

st.success("✅ Visualization complete.")
