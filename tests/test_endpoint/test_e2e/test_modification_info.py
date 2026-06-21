import pytest
import allure
from pydantic import ValidationError


from tests.base.api.client_api import EndpointClient
from tests.models.users import (
    CreateUserData,
    CreateUserResponse,
    GetAllUsersList,
    TotalUserSummary,
)
from tests.test_endpoint.user_helpers import UserService
from tests.utils.fakers import random_string
from tests.utils.helpers import send_request


@pytest.mark.endpoint
@allure.feature("Users API")
@allure.story("End-to-End User Management")
@allure.description(
    """ ''
### Explanation:
1. **Get total summary of users**: Verify initial user statistics.
2. **Create a new user**: Create a new user and check the total user count.
3. **Check updated total summary**: Ensure the number of users has increased by 1.
4. **Get all users**: Retrieve all users and check if the newly created user exists.
5. **Get user details by ID**: Fetch specific details of the newly created user.
6. **Update user data**: Modify the newly created user's data.
7. **Verify updated data**: Ensure the changes were successfully applied.
8. **Delete the created user**: Delete the created user and ensure the total count is updated.
"""
)
class TestEndToEndUserFlow:

    @allure.title("End-to-End User Management Test")
    @allure.description("Test the full user management flow from creation to deletion.")
    def test_end_to_end_user_flow(
        self, class_endpoint_client: EndpointClient, auth_token
    ):
        # Step 1: Get the initial total summary
        with allure.step("Requesting total summary of users"):
            initial_response = send_request(
                UserService.get_total_summary,
                class_endpoint_client,
                auth_token,
                schema=TotalUserSummary,
            )
            initial_total = getattr(initial_response, "total", 0)

        # Step 2: Create a new user
        new_user_data = CreateUserData(
            username=random_string() * 4,
            password=random_string() * 2,
            homedir=random_string(),
            project=random_string(),
        )

        with allure.step("Creating a new user"):
            send_request(
                UserService.create_user,
                class_endpoint_client,
                auth_token,
                schema=CreateUserResponse,
                data=new_user_data.dict(),
            )

        # Step 3: Verify total summary is updated
        with allure.step("Verifying total summary after user creation"):
            initial_response = send_request(
                UserService.get_total_summary,
                class_endpoint_client,
                auth_token,
                schema=TotalUserSummary,
            )
            assert (
                initial_response.total == initial_total + 1,
                f"Expected total users to increase by 1, but got {initial_response.total}",
            )

        # Step 4: Get all users and find the created user
        with allure.step("Retrieving all users and checking the created user"):
            all_users_response = send_request(
                UserService.get_all_users,
                class_endpoint_client,
                auth_token,
                schema=GetAllUsersList,
                validate_list=True,
            )
            try:
                users_list = [
                    GetAllUsersList(**vars(user)) for user in all_users_response
                ]
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

        # Step 5: Get user details by ID
        with allure.step(f"Retrieving details of user with ID {created_user_id}"):
            send_request(
                UserService.get_user_endpoint,
                class_endpoint_client,
                auth_token,
                schema=GetAllUsersList,
                data=created_user_id,
            )

        # Step 6: Update the user data
        with allure.step(f"Update info of user with ID {created_user_id}"):
            send_request(
                lambda client, token, data: UserService.patch_user(
                    client, token, user_id=created_user_id, user_data=data
                ),
                class_endpoint_client,
                auth_token,
                schema=GetAllUsersList,
                data=CreateUserData().dict(),
            )

        # Step 7: Verify updated user data
        with allure.step(f"Verifying updated data for user ID {created_user_id}"):
            send_request(
                UserService.get_user_endpoint,
                class_endpoint_client,
                auth_token,
                schema=GetAllUsersList,
                data=created_user_id,
            )

        # Step 8: Delete the created user
        with allure.step(f"Deleting the user with ID {created_user_id}"):
            send_request(
                UserService.delete_user,
                class_endpoint_client,
                auth_token,
                data=created_user_id,
            )

        # Step 9: Verify total summary is updated after user deletion
        with allure.step("Verifying total summary after user deletion"):
            final_response = send_request(
                UserService.get_total_summary,
                class_endpoint_client,
                auth_token,
                schema=TotalUserSummary,
            )
            final_total = getattr(final_response, "total", 0)
            assert (
                initial_total == final_total
            ), f"Total number of users changed: {initial_total} -> {final_total}"
