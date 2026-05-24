import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

st.set_page_config(page_title="Supply Chain AI Dashboard", layout="wide")
st.title("📊 Intelligent Supply Chain & Demand Forecasting Dashboard")

# 1. DATABASE INGESTION LAYER
def fetch_all_data():
    conn = sqlite3.connect('supply_chain.db')
    df = pd.read_sql_query("SELECT * FROM product_sales", conn)
    conn.close()
    return df

df_master = fetch_all_data()

# 2. AI FORECASTING ENGINE
def generate_ai_forecast(sales_data):
    if len(sales_data) < 2:
        return sales_data[-1] * 1.10
    recent_changes = [sales_data[i] - sales_data[i-1] for i in range(1, len(sales_data))]
    recent_momentum = sum(recent_changes[-3:]) / len(recent_changes[-3:])
    return round(sales_data[-1] + recent_momentum)

# 🌟 USER-FRIENDLY FEATURE 1: SIDEBAR CONTROLS & FILTERING
st.sidebar.header("🎛️ Dashboard Controls")
st.sidebar.markdown("Use these filters to instantly segment your warehouse analytics.")

# Dynamic category filter
available_categories = df_master['category'].unique().tolist()
product_selected = st.sidebar.selectbox("Select Product Category:", available_categories)

# Global safe threshold slider tool
safety_buffer_pct = st.sidebar.slider("Adjust Safety Stock Buffer (%)", min_value=10, max_value=50, value=20)

# Filter data dynamically based on selection
df_filtered = df_master[df_master['category'] == product_selected]
months = df_filtered['month'].tolist()
sales = df_filtered['units_sold'].tolist()

# Run AI calculations
next_month_prediction = generate_ai_forecast(sales)
safety_stock = round(next_month_prediction * (safety_buffer_pct / 100))

# 🌟 USER-FRIENDLY FEATURE 2: AUTOMATED OPERATIONAL ALERTS
st.subheader("🔔 Real-Time Operational Alerts")
if next_month_prediction > 150:
    st.error(f"🚨 **High Demand Warning:** Projected demand for {product_selected} is surging. Allocate extra shelf space!")
elif next_month_prediction < 80:
    st.warning(f"⚠️ **Low Turnover Risk:** {product_selected} demand is dropping. Consider running a discount campaign.")
else:
    st.success(f"✅ **Stable Inventory:** {product_selected} inventory levels are balanced and healthy.")

st.markdown("---")

# 3. KPI DISPLAY LAYER
col1, col2, col3 = st.columns(3)
with col1: 
    st.metric(label="Last Month Sales (Jun)", value=f"{sales[-1]} Units")
with col2: 
    st.metric(label="AI Predicted Demand (Jul)", value=f"{next_month_prediction} Units", delta=f"{next_month_prediction - sales[-1]} trended")
with col3: 
    st.metric(label="Optimized Safety Buffer", value=f"{safety_stock} Units", delta=f"Set at {safety_buffer_pct}%")

st.markdown("---")

# 4. CHART & VISUALIZATION HORIZON
st.subheader("📈 Historical Sales Trends & Predictive AI Horizon")
extended_months = months + ["Jul (Forecast)"]
extended_sales = sales + [next_month_prediction]

fig, ax = plt.subplots(figsize=(10, 3.5))
ax.plot(months, sales, marker='o', color='#4CAF50', linewidth=2.5, label="Actual Sales (SQL Database)")
ax.plot(extended_months[-2:], extended_sales[-2:], linestyle="--", color="#FFC107", marker='o', linewidth=2.5, label="AI Predictive Horizon")
ax.set_ylabel("Units Sold")
ax.grid(True, linestyle=":", alpha=0.5)
ax.legend()
st.pyplot(fig)

st.markdown("---")

# 🌟 USER-FRIENDLY FEATURE 3: INTERACTIVE WAREHOUSE DATA LOGGER
st.subheader("📂 Live Database Registry")
st.markdown("This table loads the live rows straight out of your SQL database. You can filter and search this tracking log instantly.")
st.dataframe(df_filtered, use_container_width=True)