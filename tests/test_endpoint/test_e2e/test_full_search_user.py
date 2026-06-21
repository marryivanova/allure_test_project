import pytest
import random
import allure

from tests.utils.fakers import random_string
from tests.utils.helpers import send_request
from tests.models.users import GetAllUsersList
from tests.base.api.client_api import EndpointClient
from tests.test_endpoint.user_helpers import UserService


@pytest.mark.flaky(reruns=3, reruns_delay=5)
@allure.feature("Users API")
@allure.story("Complex User Search with Various Parameters")
class TestComplexSearch:

    @allure.title("Get user by project")
    @allure.description("Test retrieving users by project name.")
    @pytest.mark.parametrize("repeat", range(10))
    def test_get_user_by_project(
        self, class_endpoint_client: EndpointClient, auth_token, users_data, repeat
    ):
        random_projects = random.sample(
            users_data["project_names"], min(10, len(users_data["project_names"]))
        )
        for project_name in random_projects:
            with allure.step(f"Requesting users by project: {project_name}"):
                send_request(
                    UserService.get_user_by_project,
                    class_endpoint_client,
                    auth_token,
                    schema=GetAllUsersList,
                    validate_list=True,
                    data=project_name,
                )

    @allure.title("Get user by ID")
    @allure.description("Test retrieving the user by user_identifier.")
    @pytest.mark.parametrize("repeat", range(10))
    def test_get_user_by_id(
        self, class_endpoint_client: EndpointClient, auth_token, users_data, repeat
    ):
        user_id = random.sample(
            users_data["user_ids"], min(10, len(users_data["user_ids"]))
        )
        for user_id in user_id:
            with allure.step(f"Requesting user by ID {user_id}"):
                send_request(
                    UserService.get_user_endpoint,
                    class_endpoint_client,
                    auth_token,
                    schema=GetAllUsersList,
                    data=user_id,
                )

    @allure.title("Get user by username")
    @allure.description("Test retrieving the user by username.")
    @pytest.mark.parametrize("repeat", range(10))
    def test_get_user_by_username(
        self, class_endpoint_client: EndpointClient, auth_token, users_data, repeat
    ):
        random_usernames = random.sample(
            users_data["user_identifiers"], min(10, len(users_data["user_identifiers"]))
        )
        for username in random_usernames:
            with allure.step(f"Requesting user by username: {username}"):
                send_request(
                    UserService.get_user_endpoint,
                    class_endpoint_client,
                    auth_token,
                    schema=GetAllUsersList,
                    data=username,
                )

    @allure.title("Get user by project")
    @allure.description(
        "Test retrieving users by project name and verifying 'default' project user count."
    )
    @pytest.mark.parametrize("repeat", range(10))
    def test_get_user_by_project(
        self, class_endpoint_client: EndpointClient, auth_token, users_data, repeat
    ):
        with allure.step("Retrieving all users and locating the created user"):
            all_users_response = send_request(
                UserService.get_all_users,
                class_endpoint_client,
                auth_token,
                schema=GetAllUsersList,
                validate_list=True,
            )
            users_list = [GetAllUsersList(**vars(user)) for user in all_users_response]
            default_project_users = [user for user in users_list if user.project]
            default_project_user_count = len(default_project_users)
            random_projects = random.sample(
                users_data["project_names"], min(10, len(users_data["project_names"]))
            )
            for project_name in random_projects:
                with allure.step(f"Requesting users by project: {project_name}"):
                    response = send_request(
                        UserService.get_user_by_project,
                        class_endpoint_client,
                        auth_token,
                        schema=GetAllUsersList,
                        validate_list=True,
                        data=project_name,
                    )
                    assert any(
                        user.project == project_name for user in response
                    ), f"No users found in project '{project_name}'."
                    assert (
                        len(response) <= default_project_user_count
                    ), f"Too many users found in project '{project_name}'."


@allure.feature("Users API -> Compare the length")
@allure.story("Compare the length of the list and the actual number ")
class TestLenListFull:
    """
    Test the length of the list returned by the get_all_users endpoint
    and the actual number of users registered.
    """

    @allure.title("Get all users")
    @allure.description("Test retrieving the total number of users registered.")
    def test_get_all_users(self, class_endpoint_client: EndpointClient, auth_token):
        with allure.step("Requesting user count"):
            count = send_request(
                UserService.get_user_count,
                class_endpoint_client,
                auth_token,
                schema=int,
            )

        with allure.step("Requesting all users"):
            response = send_request(
                UserService.get_all_users,
                class_endpoint_client,
                auth_token,
                schema=GetAllUsersList,
                validate_list=True,
            )
            assert len(response) == count


@allure.feature("Users API -> Negative tests for search project")
@allure.story("Projects negative tests for search project")
class TestNegativeSearch:

    @allure.title("Search with invalid project ID")
    @allure.description("Test searching with an invalid project ID (not numeric).")
    @pytest.mark.parametrize(
        "data",
        [
            random_string(),
            " ",
            -123,
            "1 OR 1=1",
            "DROP TABLE users; --",
        ],
    )
    def test_search_invalid_project_id(
        self, class_endpoint_client: EndpointClient, auth_token, data
    ):
        with allure.step(f"Requesting user information with invalid project ID {data}"):
            send_request(
                UserService.get_user_by_project,
                class_endpoint_client,
                auth_token,
                schema=GetAllUsersList,
                validate_list=True,
                data=data,
                except_code=404,
            )

    @allure.title("Search with invalid username")
    @allure.description("Test searching with a non-existing username.")
    @pytest.mark.parametrize(
        "data",
        [random_string(), " ", "admin' OR 1=1"],
    )
    def test_search_invalid_username(
        self, class_endpoint_client: EndpointClient, auth_token, data
    ):
        with allure.step(f"Requesting user by username: {data}"):
            send_request(
                UserService.get_user_endpoint,
                class_endpoint_client,
                auth_token,
                data=data,
                except_code=404,
            )
