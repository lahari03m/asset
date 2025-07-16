import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

RAW_DATA_PATH = 'sample_data.csv'

st.set_page_config(page_title="📊 Asset Work Orders Trend", layout="wide")
st.title("📊 Combined Asset Work Orders Trend Dashboard")

def load_raw_data():
    return pd.read_csv(RAW_DATA_PATH)

raw_data = load_raw_data()

st.markdown("### 📊 Monthly Work Orders Trend Across All Assets")

if 'date' in raw_data.columns and 'Asset ID' in raw_data.columns:
    raw_data['date'] = pd.to_datetime(raw_data['date'], errors='coerce')
    raw_data['Month'] = raw_data['date'].dt.to_period('M')
    usage_trend = raw_data.groupby(['Month', 'Asset ID']).size().reset_index(name='Work Orders')

    plt.figure(figsize=(14,7))
    sns.lineplot(data=usage_trend, x='Month', y='Work Orders', hue='Asset ID', marker='o', palette='tab10')
    plt.xticks(rotation=45)
    plt.title('📊 Monthly Work Orders Trend Across All Assets')
    plt.xlabel('Month')
    plt.ylabel('Number of Work Orders')
    plt.tight_layout()
    st.pyplot(plt)
else:
    st.warning("⚠️ 'date' or 'Asset ID' column not found in the data. Please verify your dataset.")

st.success("✅ Combined asset trend visualization generated.")
