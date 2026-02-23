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
            socket_connect_timeout=0.5,
            socket_timeout=0.5,
            retry_on_timeout=False,
        )
        try:
            self._connected = self._client.ping()
        except Exception:
            self._connected = False

    def get(self, key: str) -> bytes | None:
        try:
            if self._connected:
                return self._client.get(key)  # type: ignore
            return None
        except Exception:
            return None

    def set(self, key: str, value: bytes) -> bool:
        try:
            if self._connected:
                return self._client.set(key, value)  # type: ignore
            return False
        except Exception:
            return False


redis_client = RedisClient()
