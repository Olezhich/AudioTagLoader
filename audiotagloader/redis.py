import redis
from .config import REDIS_PASSWORD


class RedisClient:
    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 6379,
        password: str = REDIS_PASSWORD,
        decode_responses: bool = False,
    ):
        self._client = redis.Redis(
            host=host,
            port=port,
            password=password,
            decode_responses=decode_responses,
            db=0,
            socket_connect_timeout=5,
        )

        print("REDIS PING:", self._client.ping())

    def get(self, key: str) -> bytes | None:
        return self._client.get(key)  # type: ignore

    def set(self, key: str, value: bytes) -> bool:
        return self._client.set(key, value)  # type: ignore


redis_client = RedisClient()
