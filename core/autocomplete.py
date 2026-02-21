from core.redis_client import get_redis

def autocomplete(key:str, term:str, limit: int =10):
    if not term:
        return []
    
    redis = get_redis()
    if not redis:
        return []
    try:
        term= term.lower()
        return redis.zrangebylex(key, f"[{term}", f"[{term}\xff", start=0, num= limit)
    except Exception:
        return []