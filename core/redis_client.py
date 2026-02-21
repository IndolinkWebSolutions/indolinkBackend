import redis

from django.conf import settings

def get_redis():
    try:
        r =redis.Redis.from_url(
            settings.REDIS_URL,
            decode_responses = True,
            socket_connect_timeout = 1
        )
        r.ping()
        return r
    except Exception:
        return None
  