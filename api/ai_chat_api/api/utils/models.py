from typing import Any
from typing import TypeVar
from pydantic import BaseModel


SCHEMA = TypeVar("SCHEMA", bound=BaseModel)


def model_dump(model: BaseModel, *args, **kwargs) -> dict:
    return model.model_dump(*args, **kwargs)


def model_validate(schema: type[SCHEMA], obj: Any, *args, **kwargs) -> SCHEMA:
    return schema.from_orm(obj)
