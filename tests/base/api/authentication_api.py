import pytest
import logging

from httpx import Response

from tests.settings import base_settings
from tests.models.authentication import AuthUser
from tests.utils.constants.routes import APIRoutes
from tests.utils.clients.http.client import APIClient


logger = logging.getLogger(__name__)


class AuthenticationClient(APIClient):
    def get_auth_token_api(self, payload: AuthUser) -> Response:
        return self.client.post(
            f"{base_settings.login_url}{APIRoutes.login_page}",
            json=payload.model_dump(),
        )

    def get_auth_token(self, payload: AuthUser) -> str:
        response = self.get_auth_token_api(payload)
        if response.status_code == 401:
            pytest.fail(f"Authentication failed: {response.json()}")
        return response.json().get("Bearer")
