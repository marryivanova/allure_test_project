import json

import allure
from http import HTTPStatus
from requests import Response
from datetime import datetime

from tests.settings import base_settings
from tests.base.api.client_api import EndpointClient
from tests.utils.constants.routes import APIRoutes


class BaseTest:
    @staticmethod
    def get_headers(auth_token) -> dict:
        return {"Authorization": f"Bearer {auth_token}"}


# Methods for working with tests
class UserService:

    @staticmethod
    @allure.step("Get all users")
    def get_all_users(class_endpoint_client: EndpointClient, token: str):
        with allure.step("Sending GET request to retrieve all users"):
            response = class_endpoint_client.client.get(
                f"{base_settings.base_url}{APIRoutes.user_all}",
                headers=BaseTest.get_headers(token),
            )
        if response.status_code == HTTPStatus.OK:
            users_data = response.json()
            user_ids = [user["id"] for user in users_data if "id" in user]
            return user_ids
        else:
            response.raise_for_status()

    @staticmethod
    @allure.step("Access protected route")
    def get_protected_route(client: EndpointClient, token: str) -> Response:
        response = client.client.get(
            f"{base_settings.base_url}{APIRoutes.auth}",
            headers=BaseTest.get_headers(token),
        )
        return response

    @staticmethod
    @allure.step("Get user count")
    def get_user_count(client: EndpointClient, token: str) -> Response:
        response = client.client.get(
            f"{base_settings.base_url}{APIRoutes.count}",
            headers=BaseTest.get_headers(token),
        )
        return response

    @staticmethod
    @allure.step("Get total summary of users")
    def get_total_summary(client: EndpointClient, token: str) -> Response:
        response = client.client.get(
            f"{base_settings.base_url}{APIRoutes.total}",
            headers=BaseTest.get_headers(token),
        )
        return response

    @staticmethod
    @allure.step("Get all users")
    def get_all_users(client: EndpointClient, token: str) -> Response:
        response = client.client.get(
            f"{base_settings.base_url}{APIRoutes.user_all}",
            headers=BaseTest.get_headers(token),
        )
        return response

    @staticmethod
    @allure.step("Get unique projects")
    def get_unique_projects(client: EndpointClient, token: str) -> Response:
        response = client.client.get(
            f"{base_settings.base_url}{APIRoutes.projects_all}",
            headers=BaseTest.get_headers(token),
        )
        return response

    @staticmethod
    @allure.step("Get inactive users point")
    def get_inactive_users_point(client: EndpointClient, token: str):
        response = client.client.get(
            f"{base_settings.base_url}{APIRoutes.inactive}",
            headers=BaseTest.get_headers(token),
        )
        return response

    @staticmethod
    @allure.step("Get all user credentials")
    def get_all_id_and_password(client: EndpointClient, token: str):
        response = client.client.get(
            f"{base_settings.base_url}{APIRoutes.user_credentials}",
            headers=BaseTest.get_headers(token),
        )
        return response

    @staticmethod
    @allure.step("Get user credentials for specific user")
    def get_all_id_and_password_for_user(
        client: EndpointClient, token: str, user_id: int
    ):
        response = client.client.get(
            f"{base_settings.base_url}{APIRoutes.user_credentials}/{user_id}",
            headers=BaseTest.get_headers(token),
        )
        return response

    @staticmethod
    @allure.step("Get user by ID")
    def get_user_endpoint(client: EndpointClient, token: str, user_id: int | str):
        response = client.client.get(
            f"{base_settings.base_url}{APIRoutes.create_new_user}{user_id}",
            headers=BaseTest.get_headers(token),
        )
        return response

    @staticmethod
    @allure.step("Get user by project")
    def get_user_by_project(client: EndpointClient, token: str, project_name: str):
        response = client.client.get(
            f"{base_settings.base_url}{APIRoutes.projects}/{project_name}",
            headers=BaseTest.get_headers(token),
        )
        return response

    @staticmethod
    @allure.step("Get register user in range")
    def get_registered_users_in_range(
        client: EndpointClient, token: str, start_datetime: str, end_datetime: datetime
    ):
        params = {"start_datetime": start_datetime, "end_datetime": end_datetime}

        response = client.client.get(
            f"{base_settings.base_url}{APIRoutes.register}",
            headers=BaseTest.get_headers(token),
            params=params,
        )
        return response

    @staticmethod
    @allure.step("Get register user in Month")
    def get_users_in_month(client: EndpointClient, token: str, year, month):
        response = client.client.get(
            f"{base_settings.base_url}{APIRoutes.user_by_month}{year}/{month}",
            headers=BaseTest.get_headers(token),
        )
        return response

    @staticmethod
    @allure.step("Get zero count login user endpoint")
    def get_zero_count_user(client: EndpointClient, token: str):
        response = client.client.get(
            f"{base_settings.base_url}{APIRoutes.zero_login}",
            headers=BaseTest.get_headers(token),
        )
        return response

    @staticmethod
    @allure.step("Get success login user endpoint")
    def get_success_login_user(
        client: EndpointClient, token: str, start_datetime: str, end_datetime: datetime
    ):
        response = client.client.get(
            f"{base_settings.base_url}{APIRoutes.success_login}",
            headers=BaseTest.get_headers(token),
            params=json.dumps(
                dict(start_datetime=start_datetime, end_datetime=end_datetime)
            ),
        )
        return response

    @staticmethod
    @allure.step("Get failed login user endpoint")
    def get_failed_login_user(
        client: EndpointClient, token: str, start_datetime: str, end_datetime: datetime
    ):
        response = client.client.get(
            f"{base_settings.base_url}{APIRoutes.fail_login}",
            headers=BaseTest.get_headers(token),
            params=json.dumps(
                dict(start_datetime=start_datetime, end_datetime=end_datetime)
            ),
        )
        return response

    @staticmethod
    @allure.step("Get all users")
    def get_all_users(class_endpoint_client: EndpointClient, token: str):
        with allure.step("Sending GET request to retrieve all users"):
            response = class_endpoint_client.client.get(
                f"{base_settings.base_url}{APIRoutes.user_all}",
                headers=BaseTest.get_headers(token),
            )
            return response

    @staticmethod
    @allure.step("Get all users")
    def get_all_users_list_id(class_endpoint_client: EndpointClient, token: str):
        with allure.step("Sending GET request to retrieve all users"):
            response = class_endpoint_client.client.get(
                f"{base_settings.base_url}{APIRoutes.user_all}",
                headers=BaseTest.get_headers(token),
            )

        if response.status_code != 200:
            raise AssertionError(
                f"Request failed with status code {response.status_code}"
            )
        users_data = response.json()
        user_ids = [user["id"] for user in users_data if "id" in user]
        return user_ids

    @staticmethod
    @allure.step("Create user")
    def create_user(client: EndpointClient, token: str, json: dict):
        response = client.client.post(
            f"{base_settings.base_url}{APIRoutes.create_new_user}",
            headers=BaseTest.get_headers(token),
            json=json,
        )
        return response

    @staticmethod
    @allure.step("Patch info user")
    def patch_user(client: EndpointClient, token: str, user_id: int, user_data: dict):
        response = client.client.patch(
            f"{base_settings.base_url}{APIRoutes.create_new_user}{user_id}",
            headers={**BaseTest.get_headers(token), **user_data},
        )
        return response

    @staticmethod
    @allure.step("Delete user")
    def delete_user(client: EndpointClient, token: str, user_id: int):
        response = client.client.delete(
            f"{base_settings.base_url}/user/{user_id}",
            headers=BaseTest.get_headers(token),
        )
        return response
