from sqlalchemy import Column, Integer, String, DateTime
from config import Base
import datetime


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)


    create_date = Column(DateTime, default=datetime.datetime.now())
    update_date = Column(DateTime)


