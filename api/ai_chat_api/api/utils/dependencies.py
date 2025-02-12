from collections.abc import AsyncGenerator, AsyncIterator, Coroutine, Generator
from typing import Callable, TypeVar, Union

from ai_chat_api.api.managers.user import UserManager


RETURN_TYPE = TypeVar("RETURN_TYPE")


"""
    It's require to get yields instances.
"""


DependencyCallable = Callable[
    ...,
    Union[
        RETURN_TYPE,
        Coroutine[None, None, RETURN_TYPE],
        AsyncGenerator[RETURN_TYPE, None],
        Generator[RETURN_TYPE, None, None],
        AsyncIterator[RETURN_TYPE],
    ],
]


UserManagerDependency = DependencyCallable[UserManager]
