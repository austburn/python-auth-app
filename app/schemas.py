import os
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
import diceware

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    confirmed = Column(Boolean)

    def __init__(self, name=None, email=None, password=None, confirmed=False):
        self.name = name
        self.email = email
        self.password = password
        self.confirmed = confirmed


class OTP(Base):
    __tablename__ = 'otp'

    id = Column(Integer, primary_key=True)
    key = Column(String)
    created = Column(DateTime)

    def __init__(self, id):
        self.id = id
        self.key = diceware.get_passphrase()
        print('KEY', self.key)
        self.created = datetime.now()
