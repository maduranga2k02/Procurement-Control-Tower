import streamlit as st
import pandas as pd
import plotly.express as px

# 1. SETUP
st.set_page_config(page_title="Healthcare PPV Dashboard", layout="wide")

# 2. LOAD DATA
@st.cache_data
def load_data():
    return pd.read_excel("healthcare_data.xlsx")

df = load_data()

# 3. TITLE & CONTEXT
st.title("🏥 Healthcare Indirect Procurement: Price Variance Analysis")
st.markdown("Analyzing how **Supplier Price Changes** impact our Total Budget.")

# 4. KPI SUMMARY (The "Financial Hit")
# Variance > 0 means we paid MORE than expected (Bad)
# Variance < 0 means we paid LESS (Good)
total_spend = df['Total_Spend'].sum()
total_variance = df['Price_Variance_Impact'].sum()

c1, c2, c3 = st.columns(3)
c1.metric("Total Spend (YTD)", f"${total_spend:,.0f}")

# If Variance is Positive, we show it in Red (Cost Increase)
c2.metric("Total Price Inflation Impact", f"${total_variance:,.0f}", 
          delta="-Over Budget" if total_variance > 0 else "Under Budget",
          delta_color="inverse")

# 5. ITEM DRILL-DOWN (The "Why")
st.divider()

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Which Items are Driving Cost Increases?")
    # Group by Item and sum the Variance
    item_impact = df.groupby('Item_Name')['Price_Variance_Impact'].sum().reset_index()
    fig1 = px.bar(item_impact, x='Price_Variance_Impact', y='Item_Name', orientation='h',
                  color='Price_Variance_Impact', 
                  color_continuous_scale='RdYlGn_r', # Red = High Variance (Bad)
                  title="Total Extra Cost by Item")
    st.plotly_chart(fig1, use_container_width=True)

with col_chart2:
    st.subheader("Price Trend: Baseline vs. Actual")
    # Let user pick an item to inspect
    selected_item = st.selectbox("Select Item to Inspect:", df['Item_Name'].unique())
    
    # Filter data for that item
    item_data = df[df['Item_Name'] == selected_item].sort_values('Date')
    
    # Line chart comparing Expected vs Actual Price
    fig2 = px.line(item_data, x='Date', y=['Baseline_Price', 'Actual_Price'], 
                   title=f"Price Fluctuation for {selected_item}")
    st.plotly_chart(fig2, use_container_width=True)

# 6. SUPPLIER PERFORMANCE
st.subheader("Supplier Impact Analysis")
st.dataframe(df.groupby('Supplier')[['Total_Spend', 'Price_Variance_Impact']].sum().style.format("${:,.0f}"))