import bcrypt
from enum import Enum
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from database.base import Base

from models.time_record import TimeRecord
from models.wallet_history import WalletHistory



class Role(str, Enum):
    admin = "admin"
    user = "user"


class User(TimeRecord, Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    phone_number = Column(String, unique=True, nullable=False)
    wallet = Column(Integer, default=0)
    role = Column(String, default=Role.user)
    hashed_password = Column(String, nullable=False)
    address = Column(String, nullable=True)

    orders = relationship("Order", back_populates="user")
    wallet_history = relationship("WalletHistory", back_populates="user")

    def hash_password(self, password: str):
        self.hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify_password(self, password: str):
        return bcrypt.checkpw(password.encode("utf-8"), self.hashed_password.encode("utf-8"))
