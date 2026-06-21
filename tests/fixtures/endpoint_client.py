import allure
import pytest

from tests.settings import base_settings
from tests.utils.helpers import send_request
from tests.models.users import GetAllUsersList
from tests.base.api.client_api import EndpointClient
from tests.test_endpoint.user_helpers import UserService
from tests.utils.clients.http.builder import get_http_client
from tests.models.authentication import Authentication, AuthUser


@pytest.fixture(scope="class")
def class_endpoint_client() -> EndpointClient:
    auth_user = AuthUser(
        username=base_settings.test_user.email,
        password=base_settings.test_user.password,
    )

    auth = Authentication()

    temp_client = get_http_client()
    temp_endpoint_client = EndpointClient(client=temp_client)
    auth.auth_token = temp_endpoint_client.get_auth_token(auth_user)

    masked_username = "[REDACTED]" if auth_user.username else "[No username]"
    masked_token = "[REDACTED]" if auth.auth_token else "[No token]"

    allure.attach(
        f"Using username: {masked_username}",
        name="Username",
        attachment_type=allure.attachment_type.TEXT,
    )
    allure.attach(
        f"Auth token: {masked_token}",
        name="Auth Token",
        attachment_type=allure.attachment_type.TEXT,
    )

    client = get_http_client(auth=auth)

    return EndpointClient(client=client)


@pytest.fixture(scope="class")
def users_data(class_endpoint_client: EndpointClient, auth_token):
    with allure.step("Fetching all users before tests"):
        response = send_request(
            UserService.get_all_users,
            class_endpoint_client,
            auth_token,
            schema=GetAllUsersList,
            validate_list=True,
        )
        users = response if isinstance(response, list) else []
        return {
            "user_ids": [user.id for user in users],
            "user_identifiers": [
                user.username for user in users
            ],  # Accessing the 'username' attribute
            "project_names": [
                user.project for user in users
            ],  # Accessing the 'project' attribute
            "user_creation_dates": [
                user.creation_at for user in users
            ],  # Accessing the 'creation_at' attribute
            "user_updated_dates": [
                user.updated_at for user in users
            ],  # Accessing the 'updated_at' attribute
            "last_logins": [
                user.last_login for user in users
            ],  # Accessing the 'last_login' attribute
            "login_counts": [
                user.login_count for user in users
            ],  # Accessing the 'login_count' attribute
            "last_err_logins": [
                user.last_err_login for user in users
            ],  # Accessing 'last_err_login'
            "err_login_counts": [
                user.err_login_count for user in users
            ],  # Accessing 'err_login_count'
            "last_ips": [user.last_ip for user in users],  # Accessing 'last_ip'
            "is_active": [user.is_active for user in users],  # Accessing 'is_active'
        }
