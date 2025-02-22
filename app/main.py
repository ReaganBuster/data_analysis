import requests
import pandas as pd
import streamlit as st
import altair as alt
import plotly.graph_objects as go

# Fetch data
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=IXQRCBHRNVU15Q2X'
r = requests.get(url)
data = r.json()

# Convert JSON to DataFrame
time_series = data["Time Series (5min)"]
df = pd.DataFrame.from_dict(time_series, orient="index")
df.index = pd.to_datetime(df.index)  # Convert index to datetime
df = df.rename(columns={
    "1. open": "Open",
    "2. high": "High",
    "3. low": "Low",
    "4. close": "Close",
    "5. volume": "Volume"
})
df = df.astype(float)  # Convert all values to float

st.set_page_config(layout="wide")

# Streamlit App
st.title(f"Stock Data for {data['Meta Data']['2. Symbol']}")

# Show raw data
st.subheader("Raw Data")
st.write("Here is the raw data fetched from Alpha Vantage for the stock symbol IBM. This data includes the open, high, low, close prices, and the trading volume for each 5-minute interval.")
st.dataframe(df)

# Show line chart
st.subheader("Stock Prices Over Time")
st.write("The line chart below shows the stock prices (Open, High, Low, Close) over time. This helps in visualizing the price movements and trends.")
st.line_chart(df[["Open", "High", "Low", "Close"]])

# Show volume as bar chart
st.subheader("Trading Volume Over Time")
st.write("The bar chart below represents the trading volume over time. Higher bars indicate higher trading activity during those intervals.")
st.bar_chart(df["Volume"])

# Calculate moving averages
df['SMA_20'] = df['Close'].rolling(window=20).mean()
df['SMA_50'] = df['Close'].rolling(window=50).mean()

# Show moving averages
st.subheader("Moving Averages")
st.write("The chart below shows the 20-period and 50-period Simple Moving Averages (SMA) along with the closing prices. Moving averages help in identifying the trend direction and potential reversals.")
st.line_chart(df[['Close', 'SMA_20', 'SMA_50']])

# Candlestick chart
st.subheader("Candlestick Chart")
st.write("The candlestick chart below provides a detailed view of the stock's price movements, including the open, high, low, and close prices for each interval. This type of chart is commonly used in technical analysis.")
fig = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])
st.plotly_chart(fig)

# Summary statistics
st.subheader("Summary Statistics")
st.write("The table below provides summary statistics for the stock data, including measures such as mean, standard deviation, min, max, and quartiles. These statistics give an overview of the data distribution.")
st.write(df.describe())

# Correlation matrix
st.subheader("Correlation Matrix")
st.write("The correlation matrix below shows the correlation coefficients between different columns in the dataset. A higher absolute value indicates a stronger relationship between the variables.")
corr = df.corr()
st.write(corr)

# Existing metrics and charts
left, centre, right = st.columns(3)
with left:
    with st.container():
        st.subheader("📊 Sales Report")
        st.metric(label="Total Revenue", value="$120,000", delta="+12%")
        st.write("The Sales Report shows the total revenue generated, with a positive change of 12% compared to the previous period.")
with centre:
    with st.container():
        st.subheader("📊 Revenue Report")
        st.metric(label="Total Revenue", value="$50,000", delta="-18%")
        st.write("The Revenue Report indicates a total revenue of $50,000, with a decrease of 18% compared to the previous period.")
with right:
    with st.container():
        st.subheader("📊 Delivery Report")
        st.metric(label="Total Revenue", value="$86,000", delta="+5%", border=True)
        st.write("The Delivery Report shows a total revenue of $86,000, with a slight increase of 5% compared to the previous period.")
    
source = pd.DataFrame({'category': [1,2,3], 'value': [50,25,25]})
base = alt.Chart(source).mark_arc(innerRadius=120).encode(theta='value', color='category:N')
    
left_1, right_2 = st.columns([2,1])
with left_1:
    with st.container():
        st.subheader("Sample Data Piechart Over Time")
        st.write("The pie chart below represents sample data categorized into three categories. This visualization helps in understanding the distribution of values across different categories.")
        st.altair_chart(base)


