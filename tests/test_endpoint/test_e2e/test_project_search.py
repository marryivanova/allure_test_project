import random
import pytest
import allure

from tests.utils.helpers import send_request
from tests.models.users import GetAllUsersList
from tests.base.api.client_api import EndpointClient
from tests.test_endpoint.user_helpers import UserService


@pytest.mark.endpoint
@allure.feature("Users API")
@allure.story("End-to-End User Management")
@allure.description(
    """
This test retrieves the total summary of users from the database. 
It ensures that the user list is correctly returned and validated 
against the expected schema.
"""
)
class TestUserAPI:

    @allure.title("Get total summary")
    @allure.description("Test retrieving the total summary of users from the database.")
    def test_get_total_summary(self, class_endpoint_client: EndpointClient, auth_token):
        with allure.step("Requesting total summary of users"):
            response_data = send_request(
                UserService.get_all_users,
                class_endpoint_client,
                auth_token,
                schema=GetAllUsersList,
                validate_list=True,
            )
            project_names = [user.project for user in response_data]
            return project_names

    @allure.title("Get user information for a specific project")
    @allure.description("Test retrieving the user by project.")
    @pytest.mark.parametrize("run", range(3))
    def test_get_user_by_project(
        self, class_endpoint_client: EndpointClient, auth_token, run
    ):
        project_names = self.test_get_total_summary(class_endpoint_client, auth_token)
        selected_projects = random.sample(project_names, 6)

        for project_name in selected_projects:
            with allure.step(
                f"Requesting user information for project: {project_name} (Run {run+1})"
            ):
                send_request(
                    UserService.get_user_by_project,
                    class_endpoint_client,
                    auth_token,
                    schema=GetAllUsersList,
                    validate_list=True,
                    data=project_name,
                )


@allure.feature("Users API -> Negative tests for search project")
@allure.story("Projects negative tests for search project")
class TestNegativeSearch:
    @allure.title("Search for non-existing project")
    @allure.description("Test searching for a non-existing project.")
    @pytest.mark.parametrize(
        "data",
        [
            "a" * 1000,
            "!@#$%^&*()_+",
            "/*-+=~^",
            "!!!@@@###",
            12,
        ],
    )
    def test_search_non_existing_project(
        self, class_endpoint_client: EndpointClient, auth_token, data
    ):
        with allure.step("Requesting user information for non-existing project"):
            send_request(
                UserService.get_user_by_project,
                class_endpoint_client,
                auth_token,
                schema=GetAllUsersList,
                validate_list=True,
                data=data,
                except_code=404,
            )
