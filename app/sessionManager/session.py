"""Session design"""
from datetime import datetime
import ormsgpack


class Session:
    session_id: str
    session_expiry: datetime
    user_id: str
    subscription_id: str

    def __init__(self, session_data: dict):
        self.session_id = session_data.get("session_id")
        self.user_id = session_data.get("user_id")
        self.subscription_id = session_data.get("subscription_id")
        self.session_expiry: datetime = session_data.get("session_expiry")

    @property
    def dict(self) -> dict:
        """
        Get dict of object
        :return:
        """
        return {
            "session_id": self.session_id,
            "session_expiry": self.session_expiry,
            "user_id": self.user_id,
            "subscription_id": self.subscription_id
        }

    @property
    def msgpack(self) -> bytes:
        """
        Get msgpack bytes
        :return: msgpack of object
        """
        return ormsgpack.packb(self.dict, option=ormsgpack.OPT_NAIVE_UTC)

    @classmethod
    def msg_unpack(cls, msg: bytes):
        """
        Unpack Sessions packed using msgpack
        :param msg:
        :return:
        """
        return cls(ormsgpack.unpackb(msg))

    @classmethod
    def create(cls, session_id: str, session_expiry: datetime, user_id: str, subscription_id: str):
        """
        Create session object
        :param session_id: session id
        :param session_expiry: session expiry
        :param user_id: user's id
        :param subscription_id: subscription id
        :return: Session
        """
        return cls({
            "session_id": session_id,
            "session_expiry": session_expiry,
            "user_id": user_id,
            "subscription_id": subscription_id
        })





