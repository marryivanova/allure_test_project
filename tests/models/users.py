import random
import typing as t
from datetime import datetime

from tests.utils.fakers import random_string
from pydantic import BaseModel, Field, field_validator, RootModel


class TotalUserSummary(BaseModel):
    total: int
    error: int
    banned: int


class GetAllUsersList(BaseModel):
    id: int
    username: str
    homedir: str
    project: str
    creation_at: datetime
    updated_at: datetime
    last_login: t.Optional[datetime]
    login_count: int
    last_err_login: t.Optional[datetime]
    err_login_count: int
    last_ip: t.Optional[str]
    is_active: bool


class InactiveUsersEndpoint(BaseModel):
    users: t.List[GetAllUsersList]


class UniqueProject(BaseModel):
    projects: t.List[str]


class AllPasswordAndId(BaseModel):
    id: int
    password: str


class DateRangeRequestStartAndTime(BaseModel):
    start_datetime: str | datetime
    end_datetime: str | datetime


class DateRangeRequestYearsMonth(BaseModel):
    year: int | str | datetime
    month: int | str | datetime


class CreateUserData(BaseModel):
    username: str = Field(default_factory=random_string)
    password: str = Field(default_factory=random_string)
    homedir: str = Field(default_factory=random_string)
    project: str = Field(default_factory=random_string)


class CreateUserResponse(BaseModel):
    message: str = Field(
        ..., description="The response message after creating the user"
    )


class DeleteResponse(RootModel[dict[str, str]]):
    pass


class UpdateUserInfo(BaseModel):
    user_id: int = Field(default_factory=lambda: random.randint(250, 290))
    username: str = Field(default_factory=random_string)
    password: str = Field(default_factory=random_string)
    homedir: str = Field(default_factory=random_string)
    project: str = Field(default_factory=random_string)
    is_active: bool = Field(
        default_factory=lambda: random.choice([True, False]), alias="is_active"
    )

    class Config:
        json_encoders = {bool: lambda v: "true" if v else "false"}

    def dict(self, **kwargs):
        result = super().dict(**kwargs)
        result["is_active"] = "true" if result["is_active"] else "false"
        return result


class DateTimeRangeModel(BaseModel):
    start_datetime: str
    end_datetime: str

    @field_validator("start_datetime", "end_datetime")
    def validate_datetime_format(cls, value):
        try:
            datetime.fromisoformat(value)
        except ValueError:
            raise ValueError(
                f"Invalid datetime format. Expected 'YYYY-MM-DDTHH:MM:SS+/-HH:MM:SS', got {value}"
            )
        return value
