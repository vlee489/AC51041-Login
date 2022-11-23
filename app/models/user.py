"""User DB Model"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True, index=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    password_hash = Column(String)
    last_login = Column(DateTime, nullable=True)

    subscriptions = relationship("Subscription", back_populates="subscriber")

    def __repr__(self):
        return f"User(id={self.id!r}, email={self.email!r}, fullname={self.first_name!r} {self.last_name!r}, " \
               f"last_login={self.last_login!r})"
