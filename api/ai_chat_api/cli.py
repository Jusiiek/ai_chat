import click
import asyncio
from functools import wraps

from ai_chat_api.cassandradb import DatabaseManager
from ai_chat_api.api.utils.fixtures import inject_fixtures


def coroutine(f):
    """takes an asynchronous function f as input."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.get_event_loop().run_until_complete(f(*args, **kwargs))

    return wrapper


@click.group()
def cli():
    """This is a management script for ai_chat_api."""


@cli.command()
@coroutine
async def init_db():
    """
    Inits database for ai_chat_api.
    """
    db = DatabaseManager.get_instance()
    db.connect()

    db.drop_db()
    db.create_db()

    await inject_fixtures()

    db.close()


if __name__ == "__main__":
    cli()
