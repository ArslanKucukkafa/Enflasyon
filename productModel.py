import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime

from config import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    productName = Column(String)
    productPrice = Column(Float)
    create_date = Column(DateTime, default=datetime.datetime.now())



