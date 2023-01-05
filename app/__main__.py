from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
from app.sessionManager import SessionManager
from app.functions.env import EnvVars
import pika

from app.callbacks import *

env_vars = EnvVars()  # Load in environment variables
engine = create_engine(env_vars.db_uri)  # Create SQL engine
Base.metadata.create_all(engine)  # Creates DB struct if it doesn't exist
db_session = sessionmaker(autocommit=False, autoflush=True, bind=engine)  # Creates session maker for SQL
session_manager = SessionManager(env_vars.redis_uri)  # Create Login Session management
# Message Broker--------
connection = pika.BlockingConnection(pika.connection.URLParameters(env_vars.mq_uri))  # Connect to message broker
channel = connection.channel()  # creates connection channel
# Define Queues and consumer
channel.queue_declare(queue="login")  # Declare Queue
channel.basic_consume(queue="login", on_message_callback=lambda ch, method, properties, body:
                      login_callback(ch, method, properties, body, db_session(), session_manager))

channel.queue_declare(queue="session")  # Declare Queue
channel.basic_consume(queue="session", on_message_callback=lambda ch, method, properties, body:
                      session_callback(ch, method, properties, body, session_manager))

channel.queue_declare(queue="user")  # Declare Queue
channel.basic_consume(queue="user", on_message_callback=lambda ch, method, properties, body:
                      user_callback(ch, method, properties, body, db_session()))

channel.queue_declare(queue="logout")  # Declare Queue
channel.basic_consume(queue="logout", on_message_callback=lambda ch, method, properties, body:
                      logout_callback(ch, method, properties, body, session_manager))

channel.queue_declare(queue="signup")  # Declare Queue
channel.basic_consume(queue="signup", on_message_callback=lambda ch, method, properties, body:
                      signup_callback(ch, method, properties, body, db_session()))
# Start application consumer
channel.start_consuming()
connection.close()
