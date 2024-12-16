import click
import asyncio
from functools import wraps


def coroutine(f):
    """takes an asynchronous function f as input."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.get_event_loop().run_until_complete(f(*args, **kwargs))

    return wrapper
