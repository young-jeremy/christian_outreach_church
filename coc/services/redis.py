import redis
from django.conf import settings


def check_redis_connection():
    try:
        redis_instance = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0,
            socket_timeout=1
        )
        redis_instance.ping()
        return True
    except redis.ConnectionError:
        return False
