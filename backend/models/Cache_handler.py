from backend.services import cache_services


class Cache_handler:
    def __init__(self):
        self.redis_connection = cache_services.get_redis_connection()

    def cache_something(self, key: str, to_cache: dict, heartbeat_interval: int) -> None:
        if self.redis_connection.exists(key):
            time_left_to_live = self.redis_connection.ttl(key)
            self.redis_connection.delete(key)
            self.redis_connection.hset(key, mapping=to_cache) 
            self.redis_connection.expire(key, time_left_to_live) # type: ignore
        else:
            self.redis_connection.hset(key, mapping=to_cache)
            self.redis_connection.expire(key, heartbeat_interval)

    def check_key_presence(self, key: str) -> bool:
        if self.redis_connection.exists(key):
            return True
        else:
            return False
        
    def set_key_time_to_live(self, key: str, time: int) -> None:
        self.redis_connection.expire(key, time)

    def get_key_value(self, key: str) -> dict:
        return self.redis_connection.hgetall(key) # type: ignore
