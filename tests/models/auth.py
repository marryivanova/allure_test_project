import typing as t
from pydantic import BaseModel


class AuthResponse(BaseModel):
    message: str
    user_id: int
    username: str
    avatar_url: t.Optional[str]
    description: t.Optional[str]
    first_name: t.Optional[str]
    last_name: t.Optional[str]
    job_title: t.Optional[str]
    department: t.Optional[str]
    division: t.Optional[str]
    is_admin: bool
