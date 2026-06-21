import allure
import pytest

from tests.settings import base_settings
from tests.models.authentication import AuthUser
from tests.base.api.client_api import EndpointClient


@pytest.fixture
def valid_payload():
    masked_username = "[REDACTED]" if base_settings.test_user.email else "[No username]"
    masked_password = (
        "[REDACTED]" if base_settings.test_user.password else "[No password]"
    )

    allure.attach(
        f"Using email: {masked_username}",
        name="Username",
        attachment_type=allure.attachment_type.TEXT,
    )
    allure.attach(
        f"Password: {masked_password}",
        name="Password",
        attachment_type=allure.attachment_type.TEXT,
    )

    return AuthUser(
        email=base_settings.test_user.email,
        password=base_settings.test_user.password,
    )


@pytest.fixture(scope="class")
def auth_token(class_endpoint_client: EndpointClient):
    auth_user = AuthUser(
        email=base_settings.test_user.email,
        password=base_settings.test_user.password,
    )

    token = class_endpoint_client.get_auth_token(auth_user)
    masked_token = "[REDACTED]" if token else "[No token]"

    allure.attach(
        f"Auth token: {masked_token}",
        name="Auth Token",
        attachment_type=allure.attachment_type.TEXT,
    )

    assert token, "Token should be successfully obtained."
    return token
