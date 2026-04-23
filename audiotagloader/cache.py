import hashlib
import json
from typing import Any, Callable, get_args
from functools import wraps

from pydantic import BaseModel

from .redis import redis_client

import typer

UPDATE_CACHE = False


def hash_key(func_name: str, args: tuple, kwargs: dict) -> str:
    key_dump = {
        "func": func_name,
        "args": args[1:],
        "kwargs": kwargs,
    }

    print(json.dumps(key_dump, indent=4, sort_keys=True, default=str))

    key_string = json.dumps(key_dump, sort_keys=True, default=str)
    key_hash = hashlib.md5(key_string.encode()).hexdigest()

    return f"cache:{func_name}:{key_hash}"


def cache(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        return_type: type = func.__annotations__.get("return")  # type: ignore

        key = hash_key(func.__name__, args, kwargs)
        print("HASH KEY:", key)
        if not UPDATE_CACHE:
            try:
                data = redis_client.get(key)

                if data is not None:
                    typer.secho(
                        "Load from Redis cache", fg=typer.colors.GREEN, bold=True
                    )
                    if issubclass(return_type, BaseModel):
                        return return_type.model_validate_json(data.decode())
                    else:
                        arg_type = get_args(return_type)
                        current_type = arg_type[0]
                        return [
                            current_type.model_validate(item)
                            for item in json.loads(data.decode())
                        ]

            except Exception as e:
                raise e

        res = func(*args, **kwargs)
        typer.secho("Load from Discogs api", fg=typer.colors.YELLOW, bold=True)

        try:
            serialized = "null"
            if res is not None and issubclass(return_type, BaseModel):
                serialized = res.model_dump_json()
            elif res is not None:
                arg_type = get_args(return_type)
                current_type = arg_type[0]
                serialized = json.dumps([item.model_dump() for item in res])

            redis_client.set(key, serialized.encode())

            typer.secho("Dump to Redis cache", fg=typer.colors.GREEN, bold=True)
        except Exception as e:
            raise e

        return res

    return wrapper
