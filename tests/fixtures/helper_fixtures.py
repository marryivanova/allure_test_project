import pytest

from src.helpers.logging import CustomLogFilter, current_username


@pytest.fixture
def log_filter():
    return CustomLogFilter()


@pytest.fixture(autouse=True)
def reset_username():
    yield
    current_username.set(None)


@pytest.fixture(scope="class")
def id_password_dict_fixture():
    return {}
