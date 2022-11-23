"""Login Session Manager"""
import redis
import uuid
import datetime
from typing import Optional
from .session import Session


class SessionManager:
    def __init__(self, uri: str, default_length: int = 18000):
        """
        Init
        :param uri: Redis connection URI
        :param default_length: length of sessions in seconds
        :return: None
        """
        self.__db = redis.from_url(uri)
        self.__session_length = default_length

    def create_session(self, user_id: str, subscription_id: str) -> Session:
        """
        Create a new login session
        :param user_id: User's ID
        :param subscription_id: Subscription ID
        :return: Session
        """
        session_id = str(uuid.uuid4())
        session_expiry = datetime.datetime.utcnow() + datetime.timedelta(seconds=self.__session_length)
        session = Session.create(session_id, session_expiry, user_id, subscription_id)
        self.__db.set(session_id, session.msgpack, ex=self.__session_length)
        return session

    def retrieve_session(self, session_id: str) -> Optional[Session]:
        """
        Retrieve and active session
        :param session_id: user's session ID
        :return: Session or None
        """
        if session := self.__db.get(session_id):
            return Session.msg_unpack(session)
