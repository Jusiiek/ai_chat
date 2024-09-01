import uvicorn
from fastapi import FastAPI

from ai_chat_api.config import Config
from ai_chat_api.cassandradb import CassandraConnection


def create_app() -> FastAPI:
    """
    Creates FastAPI application.
    """
    app = FastAPI()

    return app


app = create_app()


@app.on_event("startup")
def startup_event():
    connector = CassandraConnection()
    connector.create_cassandra_connection()


if __name__ == '__main__':
    uvicorn.run(
        app,
        host=Config.HOST,
        port=Config.PORT,
        reload=True,
    )
