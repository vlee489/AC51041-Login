from app.sessionManager import SessionManager
from sqlalchemy.orm import Session
from app.models import User
from app.functions.packer import pack, unpack
import bcrypt
import pika
from bson import ObjectId


def signup_callback(ch, method, props, body, session: Session):
    body: dict = unpack(body)
    response = {"state": "INVALID"}
    complete = False

    # Check if reply_to is filled, if not we'll ignore message
    if not props.reply_to:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    while not complete:
        for field in ['email', 'password', 'first_name', 'last_name']:
            if field not in body:
                response["error"] = "MISSING-FIELD"
                complete = True
                continue
            if complete:
                continue
        if session.query(User).where(User.email == f"{body['email']}").first():
            response["error"] = "EMAIL-USED"
            complete = True
            continue
        else:
            salt = bcrypt.gensalt()
            pwd_hash = bcrypt.hashpw(bytes(body["password"], 'UTF-8'), salt)
            session.add(User(
                email=body['email'],
                first_name=body['first_name'],
                last_name=body['last_name'],
                password_hash=f"{pwd_hash.decode('UTF-8')}",
                oid=str(ObjectId())
            ))
            session.commit()
            response = {
                "state": "VALID",
            }
            complete = True

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=pack(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)
