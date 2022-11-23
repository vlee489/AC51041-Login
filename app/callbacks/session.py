from app.sessionManager import SessionManager
from sqlalchemy.orm import Session
import ormsgpack
from pika import BasicProperties


def session_callback(ch, method, props, body, session: Session, session_manager: SessionManager):
    body: dict = ormsgpack.unpackb(body)
    response = {"state": "INVALID"}
    complete = False

    # Check if reply_to is filled, if not we'll ignore message
    if not props.reply_to:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    while not complete:
        if "session_id" not in body:
            response["error"] = "MISSING-FIELD"
            complete = True
            continue
        if not (user_session := session_manager.retrieve_session(body['session_id'])):
            response["error"] = "NO-SESSION"
            complete = True
            continue
        else:

            response = {
                "state": "VALID",
                "session": user_session.dict
            }
            complete = True

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=BasicProperties(correlation_id=props.correlation_id),
                     body=ormsgpack.packb(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)
