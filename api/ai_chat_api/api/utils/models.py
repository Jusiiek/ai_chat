from typing import Any
from pydantic import BaseModel


def model_dump(model: BaseModel, *args, **kwargs) -> dict:
    return model.model_dump(*args, **kwargs)


def model_validate(schema: BaseModel, obj: Any, *args, **kwargs) -> BaseModel:
    return schema.from_orm(obj)
