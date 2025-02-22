import pandas as pd
import os
import numpy as np
import streamlit as st
import altair as alt
import pydeck as pdk
from sqlalchemy import create_engine

# Set page configuration
st.set_page_config(layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get current directory
DB_PATH = os.path.join(BASE_DIR, "api", "database.sqlite")

engine = create_engine(f"sqlite:///{DB_PATH}")

# Fetch data from the database
sales_data = pd.read_sql('SELECT * FROM sales_data', engine)
order_accuracy = pd.read_sql('SELECT * FROM order_accuracy', engine)
inventory_to_sales = pd.read_sql('SELECT * FROM inventory_to_sales', engine)
delivery_status = pd.read_sql('SELECT * FROM delivery_status', engine)
loading_time_weight = pd.read_sql('SELECT * FROM loading_time_weight', engine)
delivery_locations = pd.read_sql('SELECT * FROM delivery_locations', engine)

# Convert date columns to datetime
sales_data['date'] = pd.to_datetime(sales_data['date'])

# Extract months from sales_data
months = sales_data['date'].dt.strftime('%b').unique()

# Streamlit App
st.title("Logistics Dashboard")

# Date picker
st.sidebar.header("Select Date Range")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2023-04-10"))

# Filter data based on date range
filtered_data = sales_data[(sales_data["date"] >= pd.to_datetime(start_date)) & (sales_data["date"] <= pd.to_datetime(end_date))]

# First row: Metrics
left, centre, right, extra = st.columns(4)
with left:
    st.metric(label="Total Sales", value=f"${filtered_data['sales'].sum():,.2f}", delta=f"{filtered_data['sales'].pct_change().iloc[-1]*100:.2f}%", delta_color="normal", border=True)
with centre:
    st.metric(label="Total Expenses", value=f"${filtered_data['expenses'].sum():,.2f}", delta=f"{filtered_data['expenses'].pct_change().iloc[-1]*100:.2f}%", delta_color="normal", border=True)
with right:
    st.metric(label="Net Profit Ratio", value=f"{(filtered_data['net_profit'].sum() / filtered_data['sales'].sum())*100:.2f}%", delta=f"{filtered_data['net_profit'].pct_change().iloc[-1]*100:.2f}%", delta_color="normal", border=True)
with extra:
    st.metric(label="Average Delivery Time", value=f"{filtered_data['delivery_time'].mean():.2f} days", delta=f"{filtered_data['delivery_time'].pct_change().iloc[-1]*100:.2f}%", delta_color="normal", border=True)

# Second row: Donut pie chart and bar chart
left, right = st.columns(2)
with left:
    st.subheader("Orders by Delivery Status")
    donut_chart = alt.Chart(delivery_status).mark_arc(innerRadius=60).encode(
        theta=alt.Theta(field="orders", type="quantitative"),
        color=alt.Color(field="status", type="nominal")
    )
    total_orders = delivery_status["orders"].sum()
    text = alt.Chart(pd.DataFrame({'text': [f'Total Orders\n{total_orders}']})).mark_text(
        align='center', baseline='middle', fontSize=15
    ).encode(text='text')
    st.altair_chart(donut_chart + text, use_container_width=True)
with right:
    st.subheader("Order Accuracy by Month")
    bar_chart = alt.Chart(order_accuracy).mark_bar().encode(
        x=alt.X('month', sort=months),
        y='accuracy'
    )
    st.altair_chart(bar_chart, use_container_width=True)

# Third row: Horizontal bar chart and area chart
left, right = st.columns(2)
with left:
    st.subheader("Monthly Sales")
    horizontal_bar_chart = alt.Chart(order_accuracy).mark_bar().encode(
        y=alt.Y('month', sort=months),
        x='accuracy'
    ).properties(
        width=300  # Adjust width as needed
    ).interactive()
    st.altair_chart(horizontal_bar_chart, use_container_width=True)
with right:
    st.subheader("Inventory to Sales")
    area_chart = alt.Chart(inventory_to_sales).mark_area(opacity=0.5).encode(
        x=alt.X('month', sort=months),
        y=alt.Y('inventory', title='Inventory'),
        y2=alt.Y2('sales', title='Sales')
    ).properties(
    )
    st.altair_chart(area_chart, use_container_width=True)

# Fourth row: Delivery status, loading time to weight, and map
left, centre, right = st.columns(3)
with left:
    st.subheader("Delivery Status")
    delivery_status_chart = alt.Chart(delivery_status).mark_bar().encode(
        x=alt.X('status', sort=delivery_status["status"]),
        y='orders'
    )
    st.altair_chart(delivery_status_chart, use_container_width=True)
with centre:
    st.subheader("Loading Time to Weight")
    line_chart = alt.Chart(loading_time_weight).mark_line().encode(
        x=alt.X('month', sort=months),
        y='loading_time'
    )
    bar_chart = alt.Chart(loading_time_weight).mark_bar(opacity=0.5).encode(
        x=alt.X('month', sort=months),
        y='weight'
    )
    st.altair_chart(line_chart + bar_chart, use_container_width=True)
with right:
    st.subheader("Deliveries by Location")
    map_chart = pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=1.3733,
            longitude=32.2903,
            zoom=6,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=delivery_locations,
                get_position='[longitude, latitude]',
                get_color='[200, 30, 0, 160]',
                get_radius='deliveries',
                radius_scale=500,
            ),
        ],
    )
    st.pydeck_chart(map_chart,use_container_width=True, height=300)