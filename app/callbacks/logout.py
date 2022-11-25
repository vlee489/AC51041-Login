from app.sessionManager import SessionManager
import ormsgpack
from pika import BasicProperties


def logout_callback(ch, method, props, body, session_manager: SessionManager):
    body: dict = ormsgpack.unpackb(body)
    response = {"state": "INVALID", "error": "UNKNOWN"}
    complete = False

    while not complete:
        if "session_id" not in body:
            response["error"] = "MISSING-FIELD"
            complete = True
            continue
        if not session_manager.remove_session(body["session_id"]):
            response["error"] = "NO-SESSION"
            complete = True
            continue
        else:
            response = {
                "state": "VALID",
            }
            complete = True

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=BasicProperties(correlation_id=props.correlation_id),
                     body=ormsgpack.packb(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

