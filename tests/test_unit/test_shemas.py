import random
import allure
import pytest
from pydantic import ValidationError

from src.api.schemas import (
    UserInput,
    UserOutput,
    UserCredentialOutput,
    UserSpecificCredentialOutput,
    UserUpdate,
)
from tests.test_unit._helpers_unit import (
    _generate_user_data,
    _generate_long_project,
    attach_user_data,
    attach_user_data_dict,
)
from tests.utils.fakers import random_string, generator_datatime_format


@allure.epic("Schemas validate User Input")
@allure.feature("Schemas for database")
@allure.story("Validation of schemas")
@pytest.mark.parametrize("valid_name", ["username", "password", "homedir", "project"])
@pytest.mark.parametrize("repeat", range(5))
def test_user_input_valid(valid_name, repeat):
    with allure.step("Start generating random user data for testing"):
        user_data = _generate_user_data(**{valid_name: random_string()})
        attach_user_data(user_data, name="User Data User Input")

        with allure.step(f"Validate data for username: {user_data['username']}"):
            user_input = UserInput(**user_data)
            for field in list(user_data.keys()):
                with allure.step(f"Checking field: {field}"):
                    assert (
                        getattr(user_input, field) == user_data[field]
                    ), f"{field} mismatch"


@pytest.mark.parametrize("field_name", ["username", "password", "homedir", "project"])
@pytest.mark.parametrize("repeat", range(5))
def test_user_input_max_length(field_name, repeat):
    with allure.step(f"Start testing max length validation for field: {field_name}"):
        user_data = _generate_user_data(**{field_name: _generate_long_project()})
        attach_user_data(user_data, name="User Data max length")
        with allure.step(f"Attempt to validate data with long string for {field_name}"):
            with pytest.raises(ValidationError) as exc_info:
                UserInput(**user_data)

            assert "String should have at most 255 characters" in str(exc_info.value)


@pytest.mark.parametrize("invalid_username", [random.randint(100, 1000)])
@pytest.mark.parametrize("repeat", range(5))
def test_user_input_invalid(invalid_username, repeat):
    with allure.step("Start testing invalid username validation"):
        user_data = {
            "username": random.randint(100, 1000),
            "password": random_string(),
            "homedir": random_string(),
            "project": random_string(),
        }
        attach_user_data(user_data, name="User input invalid data")
        with allure.step("Attempt to validate user data with invalid username"):
            with pytest.raises(ValidationError) as exc_info:
                UserInput(**user_data)

            assert "username" in str(exc_info.value.errors())


@allure.epic("Schemas validate User Output")
@allure.feature("Schemas for database")
@allure.story("Validation of schemas")
@pytest.mark.parametrize("repeat", range(5))
def test_create_user_output_with_all_fields(repeat):
    user_data = {
        "id": random.randint(1, 1000),
        "username": random_string(),
        "homedir": random_string(),
        "project": random_string(),
        "creation_at": generator_datatime_format(),
        "updated_at": generator_datatime_format(),
        "last_login": generator_datatime_format(),
        "login_count": random.randint(0, 10),
        "last_err_login": generator_datatime_format(),
        "err_login_count": random.randint(0, 10),
        "last_ip": f"192.168.1.{random.randint(1, 255)}",
        "is_active": random.choice([True, False]),
    }
    attach_user_data(user_data, name="User Data Output")
    with allure.step("Creating UserOutput object from the dictionary"):
        user_output = UserOutput(**user_data)
        attach_user_data_dict(UserOutput, name="User Object")

        for field in ["id", "username", "homedir", "project"]:
            with allure.step(f"Checking field: {field}"):
                assert (
                    getattr(user_output, field) == user_data[field]
                ), f"{field} mismatch"


@pytest.mark.parametrize("repeat", range(5))
def test_user_output_optional_fields(repeat):
    UserOutput(
        id=random.randint(1, 1000),
        username=random_string(),
        homedir=random_string(),
        project=random.choice([random_string(), None]),
        creation_at=generator_datatime_format(),
        updated_at=generator_datatime_format(),
        last_login=(
            generator_datatime_format() if random.choice([True, False]) else None
        ),
        login_count=random.randint(0, 10),
        last_err_login=(
            generator_datatime_format() if random.choice([True, False]) else None
        ),
        err_login_count=(random.randint(0, 10) if random.choice([True, False]) else 0),
        last_ip=f"192.168.1.{random.randint(1, 255)}",
        is_active=random.choice([True, False]),
    )
    attach_user_data_dict(UserOutput, name="User Object")


@pytest.mark.parametrize("repeat", range(5))
def test_negative_data(repeat):
    with allure.step("Testing negative data"):
        with pytest.raises(ValidationError) as exc_info:
            UserOutput(
                id=random_string(),  # invalid data int != str
                username=random_string(),
                homedir=random_string(),
                project=random_string(),
                creation_at=generator_datatime_format(),
                updated_at=generator_datatime_format(),
                last_login=generator_datatime_format(),
                login_count=random.randint(1, 1000),
                last_err_login=generator_datatime_format(),
                err_login_count=random.randint(1, 1000),
                last_ip=f"192.168.1.{random.randint(1, 255)}",
                is_active=random.choice([True, False]),
            )
            attach_user_data_dict(UserOutput, name="User Object negative data")
            assert "id" in str(exc_info.value.errors())


@allure.epic("Schemas validate User Credential Output")
@allure.feature("Schemas for database")
@allure.story("Validation of schemas")
@pytest.mark.parametrize("repeat", range(5))
def test_validate_user_credential_input(repeat):
    with allure.step("Testing User Credential Output"):
        UserCredentialOutput(id=random.randint(1, 1000), password=random_string())

    with allure.step("Testing User Credential Output with invalid ID"):
        with pytest.raises(ValidationError) as exc_info:
            UserCredentialOutput(id=random_string(), password=random_string())
            assert "id" in str(exc_info.value.errors())


def test_validate_user_credential_output():
    with allure.step("Testing User Credential"):
        UserSpecificCredentialOutput(
            id=random.randint(1, 1000), password=random_string()
        )

    with allure.step("Testing User Credential with invalid ID"):
        with pytest.raises(ValidationError) as exc_info:
            UserSpecificCredentialOutput(id=random_string(), password=random_string())
            assert "id" in str(exc_info.value.errors())


@allure.epic("Schemas validate User Update")
@allure.feature("Schemas for database")
@allure.story("Validation of schemas")
@pytest.mark.parametrize("repeat", range(5))
def test_validate_user_update(repeat):
    with allure.step("Testing User Update"):
        UserUpdate(
            username=random_string(),
            homedir=random_string(),
            project=random_string(),
            is_active=random.choice([True, False]),
        )
        attach_user_data_dict(UserUpdate, name="User Object user update")

    with allure.step("Testing User Update with invalid username"):
        with pytest.raises(ValidationError) as exc_info:
            UserUpdate(
                username=random.randint(100, 1000),
                homedir=random_string(),
                project=random_string(),
                is_active=random.choice([True, False]),
            )
            attach_user_data_dict(UserUpdate, name="User Object invalid username")
            assert "username" in str(exc_info.value.errors())

    with allure.step("Testing User Update can keep it not"):
        UserUpdate(
            username=None,
            homedir=None,
            project=random_string(),
            is_active=None,
        )
        attach_user_data_dict(UserUpdate, name="User Object data id None")
