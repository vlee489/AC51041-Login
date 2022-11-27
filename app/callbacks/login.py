from app.sessionManager import SessionManager
from sqlalchemy.orm import Session
from app.models import User
from app.functions.packer import pack, unpack
import bcrypt
import pika


def login_callback(ch, method, props, body, session: Session, session_manager: SessionManager):
    body: dict = unpack(body)
    response = {"state": "INVALID"}
    complete = False

    # Check if reply_to is filled, if not we'll ignore message
    if not props.reply_to:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    while not complete:
        if ("email" not in body) or ("password" not in body):
            response["error"] = "MISSING-FIELD"
            complete = True
            continue
        if not (user := session.query(User).where(User.email == f"{body['email']}").first()):
            response["error"] = "NO-USER"
            complete = True
            continue
        if not bcrypt.checkpw(body["password"].encode(), user.password_hash.encode()):
            response["error"] = "PASSWORD"
            complete = True
            continue
        else:
            session = session_manager.create_session(user.id, user.oid, None)
            response = {
                "state": "VALID",
                "login": {
                    "session": session.session_id,
                    "expiry": session.session_expiry
                }
            }
            complete = True

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=pack(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)
