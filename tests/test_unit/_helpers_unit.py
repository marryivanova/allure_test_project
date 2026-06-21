import allure

from collections import ChainMap
from tests.utils.fakers import random_string


def _generate_long_project(length: int = 256) -> str:
    return "a" * length


def _validate_user_output(user_output, expected_data):
    for key in expected_data:
        assert getattr(user_output, key) == expected_data[key], f"{key} mismatch"


def _generate_user_data(**overrides):
    defaults = dict(
        username=random_string(),
        password=random_string(),
        homedir=random_string(),
        project=random_string(),
    )
    return dict(ChainMap(overrides, defaults))


def attach_user_data(user_data, name="User Data"):
    with allure.step(f"Attaching {name} dictionary"):
        allure.attach(
            str(user_data),
            name=name,
            attachment_type=allure.attachment_type.JSON,
        )


def attach_user_data_dict(user_data, name="User Data"):
    with allure.step(f"Attaching {name} dictionary"):
        allure.attach(
            str(user_data.__dict__),
            name="User Object",
            attachment_type=allure.attachment_type.JSON,
        )
