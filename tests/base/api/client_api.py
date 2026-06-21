import allure
import copy

from httpx import Response

from tests.models.users import CreateUserData
from tests.models.authentication import AuthUser
from tests.utils.clients.http.client import APIClient
from tests.utils.constants.routes import APIRoutes


class EndpointClient(APIClient):

    @allure.step("Get auth token")
    def get_auth_token(self, payload: AuthUser) -> str:
        masked_payload = copy.deepcopy(payload.dict())
        masked_payload["password"] = "********"

        with allure.step(f"Sending auth request with payload: {masked_payload}"):
            response = self.client.post(APIRoutes.login_page, json=payload.dict())

        response.raise_for_status()
        token = response.json().get("access_token", "")

        masked_token = f"{token[:4]}{'*' * 10}{token[-4:]}" if token else "NO_TOKEN"
        with allure.step(f"Received token: {masked_token}"):
            pass

        return token

    @allure.step("Create user")
    def create_user(self, payload: CreateUserData) -> Response:
        masked_payload = copy.deepcopy(payload.dict())
        if "password" in masked_payload:
            masked_payload["password"] = "********"

        with allure.step(f"Creating user with payload: {masked_payload}"):
            response = self.client.post(APIRoutes.create_new_user, json=payload.dict())

        response.raise_for_status()
        return response.json()
