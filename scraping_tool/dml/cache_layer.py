import redis

REDIS_HOST = "localhost"
REDIS_PORT = 6379
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def cache_price(product_title: str, product_price: float):
    redis_client.set(product_title, product_price)

def get_cached_price(product_title: str) -> float:
    return float(redis_client.get(product_title))

def check_product_in_cache(product_title: str) -> bool:
    return redis_client.exists(product_title)