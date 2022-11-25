from sqlalchemy.orm import Session
import ormsgpack
from pika import BasicProperties

from app.models import User


def user_callback(ch, method, props, body, session: Session):
    body: dict = ormsgpack.unpackb(body)
    response = {"state": "INVALID", "error": "UNKNOWN"}
    complete = False

    while not complete:
        if "user_id" not in body:
            response["error"] = "MISSING-FIELD"
            complete = True
            continue
        if not (user := session.query(User).where(User.id == f"{body['user_id']}").first()):
            response["error"] = "NO-USER"
            complete = True
            continue
        else:
            response = {
                "state": "VALID",
                "user": user.response
            }
            complete = True

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=BasicProperties(correlation_id=props.correlation_id),
                     body=ormsgpack.packb(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

