import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings


project_root = Path(__file__).resolve().parents[1]
dotenv_path = project_root / ".env"
load_dotenv(dotenv_path=dotenv_path)


class TestUser(BaseModel):
    email: str
    password: str


class Settings(BaseSettings):
    base_url: str = os.getenv("BASE_URL", "")
    login_url: str = os.getenv("LOGIN_URL", "")

    test_user: TestUser = TestUser(
        email=os.getenv("TEST_USER_EMAIL", ""),
        password=os.getenv("TEST_USER_PASSWORD", ""),
    )

    @property
    def api_url(self) -> str:
        return f"{self.login_url}"

    def __repr__(self):
        return f"Settings(base_url='{self.base_url}', login_url='{self.login_url}', test_user={self.test_user})"


base_settings = Settings()
