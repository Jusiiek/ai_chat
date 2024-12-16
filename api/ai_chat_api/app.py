import uvicorn
from fastapi import FastAPI

from ai_chat_api.config import Config
from ai_chat_api.cassandradb import CassandraConnection


def create_app() -> FastAPI:
    """
    Creates FastAPI application.
    """
    # TODO add middlewares
    app = FastAPI()

    return app


app = create_app()
cassandra_connection = CassandraConnection()


@app.on_event("startup")
def startup_event():
    cassandra_connection.create_cassandra_connection()


def run_dev_server():
    uvicorn.run(
        "ai_chat_api.app:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=True,
        workers=2,
    )


if __name__ == '__main__':
    run_dev_server()
