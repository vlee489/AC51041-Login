"""Session design"""
from datetime import datetime
from app.functions.packer import pack, unpack
from typing import Optional


class Session:
    session_id: str
    session_expiry: datetime
    user_id: str
    oid: str
    subscription_id: Optional[str]

    def __init__(self, session_data: dict):
        self.session_id = session_data.get("session_id")
        self.user_id = session_data.get("user_id")
        self.subscription_id = session_data.get("subscription_id")
        self.session_expiry: datetime = session_data.get("session_expiry")
        self.oid: datetime = session_data.get("oid")

    @property
    def dict(self) -> dict:
        """
        Get dict of object
        :return:
        """
        return {
            "session_expiry": self.session_expiry,
            "user_id": self.user_id,
            "oid": self.oid,
            "subscription_id": self.subscription_id
        }

    @property
    def msgpack(self) -> bytes:
        """
        Get msgpack bytes
        :return: msgpack of object
        """
        return pack(self.dict)

    @classmethod
    def msg_unpack(cls, msg: bytes):
        """
        Unpack Sessions packed using msgpack
        :param msg:
        :return:
        """
        return cls(unpack(msg))

    @classmethod
    def create(cls, session_id: str, session_expiry: datetime, user_id: str, oid: str, subscription_id: str):
        """
        Create session object
        :param session_id: session id
        :param session_expiry: session expiry
        :param user_id: user's id
        :param oid: user's oid
        :param subscription_id: subscription id
        :return: Session
        """
        return cls({
            "session_id": session_id,
            "session_expiry": session_expiry,
            "user_id": user_id,
            "oid": oid,
            "subscription_id": subscription_id
        })





