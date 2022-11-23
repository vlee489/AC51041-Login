"""Model for user subscriptions"""
from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
import enum


class Validity(enum.Enum):
    CANCELED = "canceled"
    EXPIRED = "expired"
    ACTIVE = "active"


class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    validity = Column(Enum(Validity), default="active")

    subscriber = relationship("User", back_populates="subscriptions")

    def __repr__(self):
        return f"Subscription(id={self.id!r}, start_date={self.start_date!r}, end_date={self.end_date!r}, " \
               f"validity={self.validity!r})"
