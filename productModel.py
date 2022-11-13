from sqlalchemy import Column, Integer, String, Float

from config import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    productName = Column(String)
    productPrice = Column(Float)


