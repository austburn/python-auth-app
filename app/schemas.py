import os
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Binary

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


class OTP(Base):
    __tablename__ = 'otp'

    id = Column(Integer, primary_key=True)
    key = Column(Binary)
    created = Column(DateTime)

    def __init__(self, id):
        self.id = id
        self.key = os.urandom(16)
        self.created = datetime.now()
