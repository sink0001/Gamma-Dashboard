from flask import current_app
import redis


def get_redis_connection():
    host = current_app.config["REDIS_HOST"]
    port = current_app.config["REDIS_PORT"]
    redis_connection = redis.Redis(host=host, port=port, decode_responses=True)
    return redis_connection