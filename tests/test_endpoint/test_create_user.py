import random
import allure
import pytest

from http import HTTPStatus

from tests.utils.fakers import random_string
from tests.utils.helpers import send_request
from tests.base.api.client_api import EndpointClient
from tests.test_endpoint.test_enpoint import BaseTest
from tests.test_endpoint.user_helpers import UserService
from tests.fixtures.endpoint_client import class_endpoint_client
from tests.models.users import CreateUserData, CreateUserResponse
from tests.utils.assertions.base.solutions import assert_status_code


@pytest.mark.endpoint
@allure.feature("Users API")
@allure.story("Users CRUD Operations")
class TestCreateUser(BaseTest):

    @allure.title("Create User")
    @allure.description("Create a new user with valid data")
    @allure.step("Create user with valid data")
    def test_create_user_valid_data(
        self, class_endpoint_client: EndpointClient, auth_token
    ):
        send_request(
            UserService.create_user,
            class_endpoint_client,
            auth_token,
            schema=CreateUserResponse,
            data=CreateUserData().dict(),
        )

    @allure.title("Patch info user")
    @allure.description("Update user info with valid data")
    @allure.step("Update user data")
    def test_patch_user_info_valid_data(
        self, class_endpoint_client: EndpointClient, auth_token
    ):
        user_ids = UserService.get_all_users_list_id(class_endpoint_client, auth_token)
        last_user_id = user_ids[-1]

        with allure.step("Sending PATCH request to update user info"):
            send_request(
                lambda client, token, data: UserService.patch_user(
                    client, token, user_id=last_user_id, user_data=data
                ),
                class_endpoint_client,
                auth_token,
                data=CreateUserData().dict(),
            )

    @allure.title("Delete Last User")
    @allure.description("Delete the last created user from the list")
    @allure.step("Delete user")
    def test_delete_last_user(self, class_endpoint_client: EndpointClient, auth_token):
        user_ids = UserService.get_all_users_list_id(class_endpoint_client, auth_token)

        if user_ids:
            last_user_id = user_ids[-1]
            with allure.step("Sending DELETE request to delete user"):
                send_request(
                    UserService.delete_user,
                    class_endpoint_client,
                    auth_token,
                    data=last_user_id,
                )


@pytest.mark.endpoint
@allure.feature("Users API")
@allure.story("Users CRUD Operations -> negative data for create")
class TestCreateUserInvalidData:

    @pytest.mark.parametrize(
        "username, password, homedir, project, expected_status_code",
        [
            # Empty username
            ("", random_string(), "user_home", "TestProject", HTTPStatus.BAD_REQUEST),
            # Empty password
            (
                random_string(),
                "",
                random_string(),
                "TestProject",
                HTTPStatus.BAD_REQUEST,
            ),
            #
            (random_string(), "", "user_home", "TestProject", HTTPStatus.BAD_REQUEST),
            # Wrong type for password
            (
                random_string(),
                random_string(),
                "",
                "TestProject",
                HTTPStatus.BAD_REQUEST,
            ),
            # All the fields are empty
            ("", "", "", "", HTTPStatus.BAD_REQUEST),
        ],
    )
    @allure.title("Create User with Invalid Data")
    @allure.description("Test creating a new user with invalid data")
    @allure.step("Create user with invalid data")
    def test_create_user_invalid_data(
        self,
        class_endpoint_client: EndpointClient,
        username,
        password,
        homedir,
        project,
        expected_status_code,
        auth_token,
    ):
        with allure.step("Sending POST request to create user with invalid data"):
            send_request(
                UserService.create_user,
                class_endpoint_client,
                auth_token,
                data={
                    "username": username,
                    "password": password,
                    "homedir": homedir,
                    "project": project,
                },
                except_code=400,
            )


@pytest.mark.endpoint
@allure.feature("Users API")
@allure.story("Users CRUD Operations -> name conflict, this data already exists")
class TestCreateUserConflict(BaseTest):
    @allure.title("Create User with Existing Name")
    @allure.description("Test creating a new user with an existing name")
    @allure.step("Create user with existing name")
    def test_create_user_conflict(
        self, class_endpoint_client: EndpointClient, auth_token
    ):
        # 1. Get all users
        response = UserService.get_all_users(class_endpoint_client, auth_token)
        assert_status_code(response.status_code, HTTPStatus.OK)
        users_data = response.json()

        # 2. Select 6 user options
        existing_users = random.sample(users_data, 6)

        # 3. Trying to create a new user with data from an existing user
        for idx, user in enumerate(existing_users, 1):
            username = user["username"]
            homedir = user["homedir"]
            project = user["project"]
            password = "TestPassword123" * 3

            with allure.step(
                f"Attempting to create user with username: {username} (Attempt {idx})"
            ):
                # 4. Check that the status 409 (conflict) is returned
                send_request(
                    UserService.create_user,
                    class_endpoint_client,
                    auth_token,
                    data={
                        "username": username,
                        "password": password,
                        "homedir": homedir,
                        "project": project,
                    },
                    except_code=409,
                )


@pytest.mark.endpoint
@allure.feature("Users API")
@allure.story("Users CRUD Operations -> boundary value analysis")
class TestCreateUserBoundaryValues:
    @allure.title("Create User with Boundary Values")
    @allure.description("Test creating a new user with boundary values")
    @allure.step("Create user with boundary values")
    def test_create_user_boundary_values(
        self, class_endpoint_client: EndpointClient, auth_token
    ):
        # 1. Select random boundary values for username, password, homedir, and project = 255 ok
        with allure.step("Sending POST request to create user with boundary values"):

            send_request(
                UserService.create_user,
                class_endpoint_client,
                auth_token,
                schema=CreateUserResponse,
                data=CreateUserData(
                    username=random_string(1, 255),
                    password=random_string(1, 255),
                    homedir=random_string(1, 255),
                    project=random_string(1, 255),
                ).dict(),
            )

        # 2. Delete user with boundary values
        with allure.step("Deleting the created user"):
            user_ids = UserService.get_all_users_list_id(
                class_endpoint_client, auth_token
            )

            if user_ids:
                last_user_id = user_ids[-1]
                send_request(
                    UserService.delete_user,
                    class_endpoint_client,
                    auth_token,
                    data=last_user_id,
                )


@pytest.mark.endpoint
@allure.feature("Users API")
@allure.story("Users CRUD Operations -> negative data stack overflow")
class TestPatchUserInvalidData:
    @pytest.mark.parametrize(
        "username, password, homedir, project, expected, expected_status_code",
        [
            (
                random_string(1, 256) * 40,
                random_string(1, 256) * 20,
                random_string(1, 256) * 20,
                random_string(1, 256) * 20,
                False,
                422,
            ),
            (
                random_string(1, 256) * 40,
                random_string(1, 256) * 20,
                "user_home",
                "TestProject",
                False,
                422,
            ),
            (
                "username",
                "password",
                random_string(1, 256) * 20,
                random_string(1, 256) * 20,
                False,
                422,
            ),
        ],
        ids=["long_username", "long_username_homedir", "long_homedir_project"],
    )
    def test_patch_user_info_boundary_values(
        self,
        class_endpoint_client: EndpointClient,
        auth_token,
        username,
        password,
        homedir,
        project,
        expected,
        expected_status_code,
    ):
        # 1. Sending POST request to create user with invalid data (for boundary testing)
        with allure.step("Sending POST request to create user with invalid data"):
            send_request(
                UserService.create_user,
                class_endpoint_client,
                auth_token,
                data={
                    "username": username,
                    "password": password,
                    "homedir": homedir,
                    "project": project,
                },
                except_code=422,
            )
