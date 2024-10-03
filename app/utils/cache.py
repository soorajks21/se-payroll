import json
import redis
from app.core.config import settings

redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, decode_responses=True)

def cache_set(key: str, value: dict, ttl: int = 3600):
    redis_client.setex(key, ttl, json.dumps(value))

def cache_get(key: str):
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None