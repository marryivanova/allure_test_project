import typing as t

from tests.settings import base_settings
from tests.models.authentication import Authentication
from tests.utils.clients.http.client import HTTPClient
from tests.base.api.authentication_api import AuthenticationClient


def get_http_client(
    auth: t.Optional[Authentication] = None, base_url: str = base_settings.api_url
) -> HTTPClient:
    headers: dict[str, str] = {}

    if auth and auth.auth_token:
        headers["Authorization"] = f"Bearer {auth.auth_token}"

    client = HTTPClient(base_url=base_settings.api_url)
    authentication_client = AuthenticationClient(client=client)

    if auth and not auth.auth_token and auth.user:
        token = authentication_client.get_auth_token(auth.user)
        headers = {**headers, "Authorization": f"Token {token}"}

    client = HTTPClient(base_url=base_url, headers=headers, trust_env=True)
    return client
