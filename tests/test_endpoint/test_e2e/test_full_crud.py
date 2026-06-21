import random
import allure
import pytest
from pydantic import ValidationError

from tests.models.users import (
    TotalUserSummary,
    CreateUserData,
    CreateUserResponse,
    GetAllUsersList,
    DeleteResponse,
)
from tests.test_endpoint.user_helpers import UserService
from tests.utils.fakers import random_string
from tests.utils.helpers import send_request


@pytest.mark.endpoint
@allure.feature("Users API")
@allure.story("End-to-End User Management")
@allure.description(
    """
### Explanation:
**Preliminary state (Get total summary):**
- Get the current state of the total number of users.
- Save total.

**Create new user:**
- Create a user with specific data (e.g. username, homedir, project).

**Checking the updated state:**
- After creation, check if the number of users has increased by 1.

**Getting a list of all users:**
- Looking for the created user in the list of users.
- Compare the data (e.g. username, homedir).

**Getting user information by ID:**
- Use the ID of the created user to query its detailed information.

**Deleting a created user:**
- Delete a user by its ID.

**Checking the final status:**
- Verify that the number of users has returned to the initial value.
"""
)
class TestEndToEndUserFlow:

    @allure.title("E2E User Management Test")
    @allure.description(
        "End-to-end test covering user summary, creation, retrieval, and deletion."
    )
    def test_e2e_user_flow(self, class_endpoint_client, auth_token):
        # Step 1: Get initial total summary
        with allure.step("Requesting initial total summary of users"):
            initial_response = send_request(
                UserService.get_total_summary,
                class_endpoint_client,
                auth_token,
                schema=TotalUserSummary,
            )

        # Step 2: Create a new user
        with allure.step("Creating a new user"):
            new_user_data = CreateUserData(
                username=random_string() * 3,
                password=random_string() * 3,
                homedir=random_string(),
                project=random_string(),
            )
            send_request(
                UserService.create_user,
                class_endpoint_client,
                auth_token,
                schema=CreateUserResponse,
                data=new_user_data.dict(),
            )

        # Step 3: Verify total summary updated
        with allure.step("Verifying total summary is updated"):
            updated_summary = send_request(
                UserService.get_total_summary,
                class_endpoint_client,
                auth_token,
                schema=TotalUserSummary,
            )
            total = getattr(initial_response, "total", 0)

        assert (
            updated_summary.total == total + 1,
            f"Expected total users to increase by 1, but got {updated_summary.total}",
        )

        # Step 4: Get all users and find the created one
        with allure.step("Retrieving all users and locating the created user"):
            all_users_response = send_request(
                UserService.get_all_users,
                class_endpoint_client,
                auth_token,
                schema=GetAllUsersList,
                validate_list=True,
            )
        try:
            users_list = [GetAllUsersList(**vars(user)) for user in all_users_response]
        except ValidationError as e:
            pytest.fail(f"Invalid response data for users list: {e}")

        matched_user = next(
            (
                user
                for user in users_list
                if user.username == new_user_data.username
                and user.homedir == new_user_data.homedir
            ),
            None,
        )
        created_user_id = matched_user.id

        # Step 5: Retrieve specific user by ID
        with allure.step(f"Retrieving user by ID: {created_user_id}"):
            user_by_id_response = send_request(
                UserService.get_user_endpoint,
                class_endpoint_client,
                auth_token,
                schema=GetAllUsersList,
                data=created_user_id,
            )
            assert (
                user_by_id_response.username == new_user_data.username
            ), f"Username does not match. Expected: {new_user_data.username}, got: {user_by_id_response.username}"
            assert (
                user_by_id_response.homedir == new_user_data.homedir
            ), f"Home directory does not match. Expected: {new_user_data.homedir}, got: {user_by_id_response.homedir}"

        # Step 6: Delete the created user
        with allure.step("Deleting the created user"):
            send_request(
                UserService.delete_user,
                class_endpoint_client,
                auth_token,
                data=created_user_id,
            )

        # Step 7: Verify total summary updated after deletion
        with allure.step("Verifying total summary after deletion"):
            final_response = send_request(
                UserService.get_total_summary,
                class_endpoint_client,
                auth_token,
                schema=TotalUserSummary,
            )
        assert (
            final_response.total == total,
            f"Expected total users to revert to {total}, but got {final_response.total}",
        )


@allure.feature("Users API -> negative case")
@allure.story("Negative case")
class TestNegativeCrud:
    @allure.title("Negative CRUD Test")
    @pytest.mark.parametrize("repeat", range(2))
    @allure.description("Test scenarios for invalid user operations.")
    @pytest.mark.parametrize(
        "data",
        [random.randint(-10000, -4000), random.randint(4000, 10000)],
    )
    def test_negative_delete(self, class_endpoint_client, auth_token, data, repeat):
        with allure.step("Sending DELETE request to delete user"):
            send_request(
                UserService.delete_user,
                class_endpoint_client,
                auth_token,
                schema=DeleteResponse,
                data=data,
                except_code=404,
            )
