import random
import pytest
import allure
from datetime import datetime

from tests.utils.helpers import send_request
from tests.base.api.client_api import EndpointClient
from tests.test_endpoint.user_helpers import UserService
from tests.models.users import (
    GetAllUsersList,
    DateRangeRequestYearsMonth,
    CreateUserResponse,
    CreateUserData,
    AllPasswordAndId,
)


@pytest.mark.endpoint
@allure.feature("Users API")
@allure.story("End-to-End User registered")
@allure.description("Test retrieving the total user registered.")
class TestUser:
    @pytest.fixture
    def random_years_months(self, class_endpoint_client: EndpointClient, auth_token):
        with allure.step("Requesting total users registered"):
            response = send_request(
                UserService.get_all_users,
                class_endpoint_client,
                auth_token,
                schema=GetAllUsersList,
                validate_list=True,
            )

        creation_at = [user.creation_at for user in response]
        years = [date.year for date in creation_at]
        months = [date.month for date in creation_at]

        random_years = random.sample(years, min(10, len(years)))
        random_months = random.sample(months, min(10, len(months)))

        return random_years, random_months

    @allure.title("Get total users registered")
    @allure.description("Test retrieving the total number of users registered.")
    def test_get_total_users_registered(self, random_years_months):
        assert random_years_months, "Failed to retrieve random years and months."

    @allure.title("Get registration in month")
    @allure.description("Test registering a new user.")
    @pytest.mark.parametrize("_", range(3))
    def test_register_user(
        self, class_endpoint_client: EndpointClient, auth_token, random_years_months, _
    ):
        random_years, random_months = random_years_months

        for _ in range(10):
            year = random.choice(random_years)
            month = random.choice(random_months)

            with allure.step(
                f"Checking registration for year {year} and month {month}"
            ):
                send_request(
                    lambda client, token, data: UserService.get_users_in_month(
                        client, token, data["year"], data["month"]
                    ),
                    class_endpoint_client,
                    auth_token,
                    data=DateRangeRequestYearsMonth(year=year, month=month).dict(),
                )


@pytest.mark.endpoint
@allure.feature("Users API")
@allure.story("End-to-End User registered -> check time registered")
@allure.description(
    "Test retrieving the total user registered -> check time registered."
)
class TestUserAPI:
    @allure.title("Get total users registered -> check time registered")
    @allure.step("Create user with valid data")
    @allure.description(
        "Test retrieving the total number of users registered and checking the time registered."
    )
    def test_create_user_valid_data(
        self, class_endpoint_client: EndpointClient, auth_token
    ):
        # Step 1: Create user
        send_request(
            UserService.create_user,
            class_endpoint_client,
            auth_token,
            schema=CreateUserResponse,
            data=CreateUserData().dict(),
        )

        # Step 2: Extract user id from the response - get all id
        with allure.step("Requesting ID and passwords for all users"):
            response = send_request(
                UserService.get_all_id_and_password,
                class_endpoint_client,
                auth_token,
                schema=AllPasswordAndId,
                validate_list=True,
            )
        ids = [user.id for user in response]

        # Step 3: Update summary - "updated_at"
        with allure.step("Sending PATCH request to update user info"):
            send_request(
                lambda client, token, data: UserService.patch_user(
                    client, token, user_id=ids[-1], user_data=data
                ),
                class_endpoint_client,
                auth_token,
                data=CreateUserData().dict(),
            )

        # Step 4: Verify total summary is updated - "updated_at"
        with allure.step("Requesting user by ID"):
            send_request(
                UserService.get_user_endpoint,
                class_endpoint_client,
                auth_token,
                schema=GetAllUsersList,
                data=ids[-1],
            )

        # Step 5: Delete user - "deletion_status"
        with allure.step("Sending DELETE request to delete user"):
            send_request(
                UserService.delete_user,
                class_endpoint_client,
                auth_token,
                data=ids[-1],
            )


@allure.feature("Users API -> Negative tests searching data")
@allure.story("Negative Tests for Users API")
@allure.description(
    "Test retrieving the total user registered with negative scenarios."
)
class TestNegativeSearchData:
    @allure.title("Get users with invalid year and month")
    @allure.description(
        "Test retrieving users for an invalid year and month combination."
    )
    @pytest.mark.parametrize("repeat", range(5))
    @pytest.mark.parametrize("year, month", [(9999, 13), (1800, 0), (2050, 15)])
    def test_get_users_invalid_date(
        self, class_endpoint_client: EndpointClient, auth_token, year, month, repeat
    ):
        with allure.step(
            f"Checking registration for invalid year {year} and month {month}"
        ):
            send_request(
                lambda client, token, data: UserService.get_users_in_month(
                    client, token, data["year"], data["month"]
                ),
                class_endpoint_client,
                auth_token,
                data=DateRangeRequestYearsMonth(year=year, month=month).dict(),
                except_code=400,
            )

    @allure.title("Get users with future date")
    @pytest.mark.parametrize("repeat", range(5))
    @allure.description(
        "Test retrieving users for a future date where no registrations should exist."
    )
    def test_get_users_future_date(
        self, class_endpoint_client: EndpointClient, auth_token, repeat
    ):
        with allure.step(f"Checking registration for future year and month"):
            send_request(
                lambda client, token, data: UserService.get_users_in_month(
                    client, token, data["year"], data["month"]
                ),
                class_endpoint_client,
                auth_token,
                data=DateRangeRequestYearsMonth(
                    year=datetime.now().year + 10, month=random.randint(1, 12)
                ).dict(),
                except_code=400,
            )
