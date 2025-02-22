from database import Base
from sqlalchemy import Column, Integer, String, Float, Date

# Define the sales_data table
class SalesData(Base):
    __tablename__ = 'sales_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)
    sales = Column(Integer)
    deliveries = Column(Integer)
    net_profit = Column(Integer)
    expenses = Column(Integer)
    delivery_time = Column(Float)

# Define the order_accuracy table
class OrderAccuracy(Base):
    __tablename__ = 'order_accuracy'
    id = Column(Integer, primary_key=True, autoincrement=True)
    month = Column(String)
    accuracy = Column(Float)

# Define the inventory_to_sales table
class InventoryToSales(Base):
    __tablename__ = 'inventory_to_sales'
    id = Column(Integer, primary_key=True, autoincrement=True)
    month = Column(String)
    inventory = Column(Integer)
    sales = Column(Integer)

# Define the delivery_status table
class DeliveryStatus(Base):
    __tablename__ = 'delivery_status'
    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String)
    orders = Column(Integer)

# Define the loading_time_weight table
class LoadingTimeWeight(Base):
    __tablename__ = 'loading_time_weight'
    id = Column(Integer, primary_key=True, autoincrement=True)
    month = Column(String)
    loading_time = Column(Float)
    weight = Column(Integer)

# Define the delivery_locations table
class DeliveryLocations(Base):
    __tablename__ = 'delivery_locations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    deliveries = Column(Integer)