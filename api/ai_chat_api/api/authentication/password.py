import secrets
from typing import Optional

from passlib.context import CryptContext


class PasswordHelper:
    def __init__(self, hashed_password: Optional[str] = None) -> None:
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        if hashed_password is None:
            self.hashed_password = self.hash_password(
                self.generate_random_password()
            )
        else:
            self.hashed_password = hashed_password

    def verify_password(
            self, password: str, hashed_password: str
    ) -> bool:
        return self.pwd_context.verify(
            password, hashed_password
        )

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def generate_random_password(self) -> str:
        return secrets.token_urlsafe(16)

    def get_hashed_password(self) -> str:
        """
        Returns the hashed password.

        returns
        --------
        hashed_password: str
        """
        return self.hashed_password
