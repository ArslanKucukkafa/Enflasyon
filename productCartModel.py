from config import Base
from sqlalchemy import Column, Integer, String, Float, DateTime
import datetime


class productCart(Base):
    __tablename__ = 'productCart'

    processId = Column(Integer, primary_key=True)
    uid = Column(Float)
    cId = Column(Float)
    uPrice = Column(Float)
    uName = Column(String)
    maaş =Column(Float)
    uPiece = Column(Float)
    create_date = Column(DateTime, default=datetime.datetime.now())


