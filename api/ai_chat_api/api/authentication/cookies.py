from typing import Protocol

from fastapi.security import APIKeyCookie
from fastapi import Request, status

class Cookies(Protocol):
    scheme: APIKeyCookie
