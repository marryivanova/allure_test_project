import random
import allure
import pytest
from pydantic import ValidationError
from datetime import datetime, timedelta


from tests.models.auth import AuthResponse
from tests.test_endpoint.user_helpers import BaseTest, UserService
from tests.base.api.client_api import EndpointClient
from tests.models.users import (
    TotalUserSummary,
    UniqueProject,
    GetAllUsersList,
    InactiveUsersEndpoint,
    AllPasswordAndId,
    DateRangeRequestYearsMonth,
    DateRangeRequestStartAndTime,
)
from tests.utils.fakers import generate_random_date_within_year
from tests.utils.helpers import send_request


@pytest.mark.endpoint
@allure.feature("Users API")
@allure.story("Users CRUD Operations")
class TestUsers(BaseTest):

    @allure.title("Retrieve authentication token")
    @allure.description(
        "Test obtaining an authentication token with valid user credentials."
    )
    def test_get_auth_token(self, auth_token):
        assert auth_token, "Token should be successfully obtained."

    @allure.title("Access protected route")
    @allure.description(
        "Test accessing a protected route with a valid authentication token."
    )
    def test_access_protected_route(
        self, class_endpoint_client: EndpointClient, auth_token
    ):
        with allure.step("Send request to access protected route"):
            send_request(
                UserService.get_protected_route,
                class_endpoint_client,
                auth_token,
                schema=AuthResponse,
            )

    @allure.title("Get users all count")
    @allure.description("Test retrieving the count of users from the database.")
    def test_get_user_count(self, class_endpoint_client: EndpointClient, auth_token):
        with allure.step("Requesting user count"):
            send_request(
                UserService.get_user_count,
                class_endpoint_client,
                auth_token,
                schema=int,
            )

    @allure.title("Get total summary")
    @allure.description("Test retrieving the total summary of users from the database.")
    def test_get_total_summary(self, class_endpoint_client: EndpointClient, auth_token):
        with allure.step("Requesting total summary of users"):
            send_request(
                UserService.get_total_summary,
                class_endpoint_client,
                auth_token,
                schema=TotalUserSummary,
            )

    @allure.title("Get all users")
    @allure.description("Test retrieving the list of all users.")
    def test_get_all_users(self, class_endpoint_client: EndpointClient, auth_token):
        with allure.step("Sending request to retrieve all users"):
            send_request(
                UserService.get_all_users,
                class_endpoint_client,
                auth_token,
                schema=GetAllUsersList,
                validate_list=True,
            )

    @allure.title("Get user by ID")
    @allure.description("Test retrieving the user by user_identifier.")
    def test_get_user_by_id(self, class_endpoint_client: EndpointClient, auth_token):
        user_id = self.test_get_all_id_and_passwords(class_endpoint_client, auth_token)
        with allure.step("Requesting user by ID"):
            send_request(
                UserService.get_user_endpoint,
                class_endpoint_client,
                auth_token,
                schema=GetAllUsersList,
                data=user_id,
            )

    @allure.title("Get unique all projects")
    @allure.description("Test retrieving the list of unique projects.")
    def test_get_unique_projects(
        self, class_endpoint_client: EndpointClient, auth_token
    ):
        with allure.step("Requesting unique projects list"):
            response_data = send_request(
                UserService.get_unique_projects,
                class_endpoint_client,
                auth_token,
                schema=UniqueProject,
                validate_list=True,
            )
        return random.choice(response_data)

    @allure.title("Get inactive users")
    @allure.description("Test retrieving the list of inactive users.")
    def test_get_inactive_users_point(
        self, class_endpoint_client: EndpointClient, auth_token
    ):
        with allure.step("Requesting inactive users list"):
            users = send_request(
                UserService.get_inactive_users_point,
                class_endpoint_client,
                auth_token,
                schema=GetAllUsersList,
                validate_list=True,
            )
        try:
            InactiveUsersEndpoint(users=users)
        except ValidationError as e:
            raise AssertionError(
                f"Response does not match the expected model GetAllUsersList: {e}"
            )

    @allure.title("Get all ID and passwords")
    @allure.description("Test retrieving the list of all ID and passwords.")
    def test_get_all_id_and_passwords(
        self, class_endpoint_client: EndpointClient, auth_token
    ):
        with allure.step("Requesting ID and passwords for all users"):
            response = send_request(
                UserService.get_all_id_and_password,
                class_endpoint_client,
                auth_token,
                schema=AllPasswordAndId,
                validate_list=True,
            )

        ids = [user.id for user in response]
        return random.choice(ids)

    @allure.title("Get ID and passwords for a specific user")
    @allure.description("Test retrieving the ID and password for a specific user.")
    def test_get_all_id_and_password_for_user(
        self, class_endpoint_client: EndpointClient, auth_token
    ):
        user_id = self.test_get_all_id_and_passwords(class_endpoint_client, auth_token)
        with allure.step("Requesting ID and password for a specific user"):
            send_request(
                UserService.get_all_id_and_password_for_user,
                class_endpoint_client,
                auth_token,
                schema=AllPasswordAndId,
                data=user_id,
            )

    @allure.title("Get user information for a specific by project")
    @allure.description("Test retrieving the user by project.")
    def test_get_user_by_project(
        self, class_endpoint_client: EndpointClient, auth_token
    ):
        project_name = self.test_get_unique_projects(class_endpoint_client, auth_token)

        with allure.step("Requesting user by project"):
            send_request(
                UserService.get_user_by_project,
                class_endpoint_client,
                auth_token,
                schema=GetAllUsersList,
                validate_list=True,
                data=project_name,
            )

    @allure.title("Get registered users in range")
    @allure.description("Test retrieving the registered users in a specific range.")
    def test_get_registered_users_in_range(
        self, class_endpoint_client: EndpointClient, auth_token
    ):
        with allure.step("Requesting registered users in a range"):
            send_request(
                lambda client, token, data: UserService.get_registered_users_in_range(
                    client, token, data["start_datetime"], data["end_datetime"]
                ),
                class_endpoint_client,
                auth_token,
                data=DateRangeRequestStartAndTime(
                    start_datetime=generate_random_date_within_year(),
                    end_datetime=(datetime.now() + timedelta(days=365)).isoformat(),
                ).dict(),
            )

    @allure.title("Get registration in month")
    @allure.description("Test registering a new user.")
    def test_register_user(self, class_endpoint_client: EndpointClient, auth_token):
        with allure.step(
            "Checking which users have registered for the current specified time period"
        ):
            send_request(
                lambda client, token, data: UserService.get_users_in_month(
                    client, token, data["year"], data["month"]
                ),
                class_endpoint_client,
                auth_token,
                data=DateRangeRequestYearsMonth(
                    year=datetime.now().year,
                    month=datetime.now().month,
                ).dict(),
            )

    @allure.title("Get zero users login endpoint")
    @allure.description("Test get list: zero users login endpoint.")
    def test_get_user_by_username(
        self, class_endpoint_client: EndpointClient, auth_token
    ):
        with allure.step("Requesting zero users login"):
            users = send_request(
                UserService.get_zero_count_user,
                class_endpoint_client,
                auth_token,
                schema=GetAllUsersList,
                validate_list=True,
            )
        try:
            InactiveUsersEndpoint(users=users)
        except ValidationError as e:
            raise AssertionError(
                f"Response JSON does not match the expected model GetAllUsersList: {e}"
            )

    @allure.title("Get successful users login endpoint")
    @allure.description("Test get list with successful users login.")
    def test_get_success_list_user(
        self, class_endpoint_client: EndpointClient, auth_token
    ):
        with allure.step("Requesting successful users login"):
            send_request(
                lambda client, token, data: UserService.get_success_login_user(
                    client, token, data["start_datetime"], data["end_datetime"]
                ),
                class_endpoint_client,
                auth_token,
                data=DateRangeRequestStartAndTime(
                    start_datetime=generate_random_date_within_year(),
                    end_datetime=(datetime.now() + timedelta(days=365)).isoformat(),
                ).dict(),
            )

    @allure.title("Get unsuccessful users login in range")
    @allure.description("Test get list with unsuccessful users login in range.")
    def test_get_unsuccessful_list_user(
        self, class_endpoint_client: EndpointClient, auth_token
    ):

        with allure.step("Requesting unsuccessful users login"):
            send_request(
                lambda client, token, data: UserService.get_failed_login_user(
                    client, token, data["start_datetime"], data["end_datetime"]
                ),
                class_endpoint_client,
                auth_token,
                data=DateRangeRequestStartAndTime(
                    start_datetime=generate_random_date_within_year(),
                    end_datetime=(datetime.now() + timedelta(days=365)).isoformat(),
                ).dict(),
            )
