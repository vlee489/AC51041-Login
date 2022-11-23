"""Loads environment vars"""
import os


class EnvVars:
    @staticmethod
    def get_with_default(key, default):
        return os.environ.get(key, default)

    @staticmethod
    def get_required(key):
        if value := os.environ.get(key, None):
            return value
        else:
            raise EnvironmentError(f"Required value {key} not found!")

    def __init__(self):
        self.debug = self.get_with_default("DEBUG", None)
        self.redis_uri = self.get_with_default("REDIS", "redis://redis:6379")
        self.db_uri = self.get_required("DBURI")
        self.mq_uri = self.get_with_default("MQURI", "amqp://localhost:5672")

