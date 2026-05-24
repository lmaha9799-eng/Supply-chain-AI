import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

st.set_page_config(page_title="Supply Chain AI Dashboard", layout="wide")
st.title("📊 Intelligent Supply Chain & Demand Forecasting Dashboard")

# 1. DATA ENGINEERING LAYER: Fetching data from SQL
def fetch_data_from_db(category):
    conn = sqlite3.connect('supply_chain.db')
    query = f"SELECT month, units_sold FROM product_sales WHERE category = '{category}'"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# 2. AI ENGINEERING LAYER: Mathematical Forecasting Model
def generate_ai_forecast(sales_data):
    """
    Takes historical sales and calculates a trend-based projection 
    for the upcoming month using momentum tracking.
    """
    if len(sales_data) < 2:
        return sales_data[-1] * 1.10 # Fallback default growth
        
    # Calculate recent momentum: how much did sales change from month to month?
    recent_changes = []
    for i in range(1, len(sales_data)):
        change = sales_data[i] - sales_data[i-1]
        recent_changes.append(change)
    
    # Take the average growth momentum of the last 3 months
    recent_momentum = sum(recent_changes[-3:]) / len(recent_changes[-3:])
    
    # Project next month's demand: Last Month's Value + Trend Momentum
    predicted_demand = sales_data[-1] + recent_momentum
    return round(predicted_demand)

# Dropdown selection trigger
product_selected = st.selectbox("Select a Product Category to View:", ["Electronics", "Apparel", "Home Goods"])

# Execute Data & AI pipeline
df_sales = fetch_data_from_db(product_selected)
months = df_sales['month'].tolist()
sales = df_sales['units_sold'].tolist()

# Run our forecasting model
next_month_prediction = generate_ai_forecast(sales)

# 3. VISUALIZATION & KPI LAYER
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1: 
    st.metric(label="Last Month Sales (Jun)", value=f"{sales[-1]} Units")
with col2: 
    # Highlight the forecast metric
    st.metric(label="AI Predicted Demand (Jul)", value=f"{next_month_prediction} Units", delta=f"{next_month_prediction - sales[-1]} units trended")
with col3: 
    # Safety stock optimization logic
    safety_stock = round(next_month_prediction * 0.20)
    st.metric(label="Recommended Safety Stock", value=f"{safety_stock} Units", delta="20% Buffer Buffer")

st.markdown("---")
st.subheader("📈 Historical Sales Trends & Predictive AI Horizon")

# Prepare data for the extended chart line
extended_months = months + ["Jul (Forecast)"]
extended_sales = sales + [next_month_prediction]

# Plotting the visualization
fig, ax = plt.subplots(figsize=(10, 4))
# Plot historical data in green
ax.plot(months, sales, marker='o', color='#4CAF50', linewidth=2.5, label="Actual Sales (SQL Data)")
# Plot the AI forecast transition line in dashed gold
ax.plot(extended_months[-2:], extended_sales[-2:], linestyle="--", color="#FFC107", marker='o', linewidth=2.5, label="AI Predictive Horizon")

ax.set_ylabel("Units Sold")
ax.grid(True, linestyle=":", alpha=0.5)
ax.legend()

st.pyplot(fig)