import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
import pydeck as pdk

# Set page configuration
st.set_page_config(layout="wide")

# Generate dummy data
np.random.seed(42)
dates = pd.date_range(start="2023-01-01", periods=100)
sales_data = pd.DataFrame({
    "Date": dates,
    "Sales": np.random.randint(1000, 5000, size=len(dates)),
    "Deliveries": np.random.randint(50, 200, size=len(dates)),
    "Net_Profit": np.random.randint(500, 3000, size=len(dates)),
    "Expenses": np.random.randint(200, 1500, size=len(dates)),
    "Delivery_Time": np.random.uniform(1, 5, size=len(dates))
})
sales_data["Revenue"] = sales_data["Sales"] - sales_data["Expenses"]
sales_data["Net_Profit_Ratio"] = sales_data["Net_Profit"] / sales_data["Sales"]

# Generate additional dummy data for charts
months = pd.date_range(start="2023-01-01", periods=12, freq='M').strftime('%b')
order_accuracy = pd.DataFrame({
    "Month": months,
    "Accuracy": np.random.uniform(90, 100, size=12)
})
inventory_to_sales = pd.DataFrame({
    "Month": months,
    "Inventory": np.random.randint(5000, 20000, size=12),
    "Sales": np.random.randint(1000, 5000, size=12)
})
delivery_status = pd.DataFrame({
    "Status": ["Delivered", "In Transit", "Cancelled"],
    "Orders": [450, 120, 30]
})
loading_time_weight = pd.DataFrame({
    "Month": months,
    "Loading_Time": np.random.uniform(1, 5, size=12),
    "Weight": np.random.randint(1000, 5000, size=12)
})
delivery_locations = pd.DataFrame({
    "Location": ["Kampala", "Entebbe", "Jinja", "Gulu", "Mbarara"],
    "Latitude": [0.3476, 0.0517, 0.4394, 2.7666, -0.6077],
    "Longitude": [32.5825, 32.4637, 33.2032, 32.3056, 30.6586],
    "Deliveries": [150, 80, 60, 40, 30]
})

# Streamlit App
st.title("Logistics Dashboard")

# Date picker
st.sidebar.header("Select Date Range")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2023-04-10"))

# Filter data based on date range
filtered_data = sales_data[(sales_data["Date"] >= pd.to_datetime(start_date)) & (sales_data["Date"] <= pd.to_datetime(end_date))]

# First row: Metrics
left, centre, right, extra = st.columns(4)
with left:
    st.metric(label="Total Sales", value=f"${filtered_data['Sales'].sum():,.2f}", delta=f"{filtered_data['Sales'].pct_change().iloc[-1]*100:.2f}%", delta_color="inverse", border=True)
with centre:
    st.metric(label="Total Expenses", value=f"${filtered_data['Expenses'].sum():,.2f}", delta=f"{filtered_data['Expenses'].pct_change().iloc[-1]*100:.2f}%", delta_color="inverse", border=True)
with right:
    st.metric(label="Net Profit Ratio", value=f"{filtered_data['Net_Profit_Ratio'].mean()*100:.2f}%", delta=f"{filtered_data['Net_Profit_Ratio'].pct_change().iloc[-1]*100:.2f}%", delta_color="inverse", border=True)
with extra:
    st.metric(label="Average Delivery Time", value=f"{filtered_data['Delivery_Time'].mean():.2f} days", delta=f"{filtered_data['Delivery_Time'].pct_change().iloc[-1]*100:.2f}%", delta_color="inverse", border=True)

# Second row: Donut pie chart and bar chart
left, right = st.columns(2)
with left:
    st.subheader("Orders by Delivery Status")
    donut_chart = alt.Chart(delivery_status).mark_arc(innerRadius=80).encode(
        theta=alt.Theta(field="Orders", type="quantitative"),
        color=alt.Color(field="Status", type="nominal")
    )
    total_orders = delivery_status["Orders"].sum()
    text = alt.Chart(pd.DataFrame({'text': [f'Total Orders\n{total_orders}']})).mark_text(
        align='center', baseline='middle', fontSize=20
    ).encode(text='text')
    st.altair_chart(donut_chart + text, use_container_width=True)
with right:
    st.subheader("Order Accuracy by Month")
    bar_chart = alt.Chart(order_accuracy).mark_bar().encode(
        x=alt.X('Month', sort=months),
        y='Accuracy'
    )
    st.altair_chart(bar_chart, use_container_width=True)

# Third row: Horizontal bar chart and area chart
left, right = st.columns(2)
with left:
    st.subheader("Monthly Sales")
    horizontal_bar_chart = alt.Chart(order_accuracy).mark_bar().encode(
        y=alt.Y('Month', sort=months),
        x='Accuracy'
    ).properties(
        height=alt.Step(40),  # Display only 5 months at a time
        width=400  # Adjust width as needed
    ).interactive()
    st.altair_chart(horizontal_bar_chart, use_container_width=True)
with right:
    st.subheader("Inventory to Sales")
    area_chart = alt.Chart(inventory_to_sales).mark_area(opacity=0.5).encode(
        x=alt.X('Month', sort=months),
        y=alt.Y('Inventory', title='Inventory'),
        y2=alt.Y2('Sales', title='Sales')
    ).properties(
        height=alt.Step(40) # Match height with the horizontal bar chart
    )
    st.altair_chart(area_chart, use_container_width=True)

# Fourth row: Delivery status, loading time to weight, and map
left, centre, right = st.columns(3)
with left:
    st.subheader("Delivery Status")
    delivery_status_chart = alt.Chart(delivery_status).mark_bar().encode(
        x=alt.X('Status', sort=delivery_status["Status"]),
        y='Orders'
    )
    st.altair_chart(delivery_status_chart, use_container_width=True)
with centre:
    st.subheader("Loading Time to Weight")
    line_chart = alt.Chart(loading_time_weight).mark_line().encode(
        x=alt.X('Month', sort=months),
        y='Loading_Time'
    )
    bar_chart = alt.Chart(loading_time_weight).mark_bar(opacity=0.5).encode(
        x=alt.X('Month', sort=months),
        y='Weight'
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
                get_position='[Longitude, Latitude]',
                get_color='[200, 30, 0, 160]',
                get_radius='Deliveries',
                radius_scale=1000,
            ),
        ],
    )
    st.pydeck_chart(map_chart)