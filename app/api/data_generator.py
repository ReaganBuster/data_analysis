import pandas as pd
import numpy as np
from api.schemas import SalesData, OrderAccuracy, InventoryToSales, DeliveryStatus, LoadingTimeWeight, DeliveryLocations
from database import session

#Generate random data
np.random.seed(42)
dates = pd.date_range(start="2023-01-01", periods=100)
sales_data = [
    SalesData(date=date, sales=np.random.randint(1000, 5000), deliveries=np.random.randint(50, 200),
              net_profit=np.random.randint(500, 3000), expenses=np.random.randint(200, 1500),
              delivery_time=np.random.uniform(1, 5))
    for date in dates
]

months = pd.date_range(start="2023-01-01", periods=12, freq='M').strftime('%b')
order_accuracy = [
    OrderAccuracy(month=month, accuracy=np.random.uniform(90, 100))
    for month in months
]

inventory_to_sales = [
    InventoryToSales(month=month, inventory=np.random.randint(5000, 20000), sales=np.random.randint(1000, 5000))
    for month in months
]

delivery_status = [
    DeliveryStatus(status="Delivered", orders=450),
    DeliveryStatus(status="In Transit", orders=120),
    DeliveryStatus(status="Cancelled", orders=30)
]

loading_time_weight = [
    LoadingTimeWeight(month=month, loading_time=np.random.uniform(1, 5), weight=np.random.randint(1000, 5000))
    for month in months
]

delivery_locations = [
    DeliveryLocations(location="Kampala", latitude=0.3476, longitude=32.5825, deliveries=150),
    DeliveryLocations(location="Entebbe", latitude=0.0517, longitude=32.4637, deliveries=80),
    DeliveryLocations(location="Jinja", latitude=0.4394, longitude=33.2032, deliveries=60),
    DeliveryLocations(location="Gulu", latitude=2.7666, longitude=32.3056, deliveries=40),
    DeliveryLocations(location="Mbarara", latitude=-0.6077, longitude=30.6586, deliveries=30)
]

# Add data to the session and commit
session.add_all(sales_data)
session.add_all(order_accuracy)
session.add_all(inventory_to_sales)
session.add_all(delivery_status)
session.add_all(loading_time_weight)
session.add_all(delivery_locations)
session.commit()
