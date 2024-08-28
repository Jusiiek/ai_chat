import uvicorn
from fastapi import FastAPI

from ai_chat_api.config import Config


def create_app() -> FastAPI:
    app = FastAPI()

    return app


app = create_app()


if __name__ == '__main__':
    uvicorn.run(
        app,
        host=Config.HOST,
        port=Config.PORT
    )
