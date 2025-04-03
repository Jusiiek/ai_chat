import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from ai_chat_api.middleware import (
    jwt_middleware,
    security_headers_middleware
)
from ai_chat_api.config import Config
from ai_chat_api.app_config import router
from ai_chat_api.cassandradb import DatabaseManager


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


def get_app_routers() -> None:
    app.include_router(router.get_auth_router())
    app.include_router(router.get_users_router())
    app.include_router(router.get_thread_router())
    app.include_router(router.get_chats_router())
    app.include_router(router.get_tasks_router())


@app.on_event("startup")
async def startup_event():
    db = DatabaseManager.get_instance()
    db.connect()

    get_app_routers()


@app.on_event("shutdown")
async def shutdown_event():
    db = DatabaseManager.get_instance()
    db.close()


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
