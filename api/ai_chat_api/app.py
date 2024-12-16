import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from ai_chat_api.middleware import (
    jwt_middleware,
    security_headers_middleware
)
from ai_chat_api.config import Config
from ai_chat_api.cassandradb import CassandraConnection


def create_app() -> FastAPI:
    """
    Creates FastAPI application.
    """
    app = FastAPI()

    origins = [Config.WEB_HOST]
    app.middleware("http")(jwt_middleware)
    app.middleware("http")(security_headers_middleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

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
