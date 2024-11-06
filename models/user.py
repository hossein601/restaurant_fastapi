import uuid
from datetime import datetime, timedelta
from enum import Enum

import bcrypt
import jwt
from config import setting
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from database.base import Base


# class Role(str, Enum):
#     ADMIN = "admin"
#     USER = "user"

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    phone_number = Column(String, unique=True, nullable=False)
    wallet = Column(Float, default=0)
    orders = relationship('Order', back_populates='user')
    reservations = relationship('Reserve', back_populates='user')
    hashed_password = Column(String, nullable=False)
    address = Column(String, nullable=True)
    # role = Column(Enum(Role), default=Role.USER)

    def hash_password(self, password: str):
        self.hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password: str):
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8'))


class TokenTable(Base):
    __tablename__ = "token"
    user_id = Column(Integer, nullable=False)
    access_token = Column(String(450), primary_key=True)
    refresh_token = Column(String(450), nullable=False)
