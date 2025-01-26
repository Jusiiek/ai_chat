from pydantic import BaseModel


def model_dump(model: BaseModel, *args, **kwargs) -> dict:
    return model.model_dump(*args, **kwargs)
