import typing as t
from pydantic import BaseModel, Field

from tests.settings import base_settings


class AuthUser(BaseModel):
    username: str = Field(default=base_settings.test_user.email)
    password: str = Field(default=base_settings.test_user.password)

    @classmethod
    def create_with_defaults(cls):
        return cls(
            username=base_settings.test_user.email,
            password=base_settings.test_user.password,
        )


class Authentication(BaseModel):
    auth_token: t.Optional[t.Union[str, AuthUser]] = None

    def get_user_or_token(self):
        if self.auth_token is None:
            return AuthUser(
                username=base_settings.test_user.email,
                password=base_settings.test_user.password,
            )
        return self.auth_token
