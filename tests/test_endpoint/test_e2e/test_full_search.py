import random
import allure
import pytest

from tests.utils.helpers import send_request
from tests.base.api.client_api import EndpointClient
from tests.test_endpoint.user_helpers import UserService
from tests.models.users import GetAllUsersList, AllPasswordAndId


@allure.feature("Users API")
@allure.story("End-to-End User Management")
@allure.description(
    """
    This test suite validates the functionality of the User API. It performs an end-to-end check 
    of user management operations, focusing on retrieving user credentials, ensuring the ID matches 
    the corresponding password, and validating the response structure against the expected schema.

    Steps:
    1. Retrieve all user credentials.
    2. Check that each user’s ID matches the correct password.
    3. Perform 10 random checks to ensure ID-password pairs are valid.
    4. Validate that the response structure conforms to the expected schema.
    6. Check that the invalid id
    """
)
class TestUserCredentials:

    @allure.title("Check user credentials and ID-password matching")
    @allure.description(
        "Test the user credentials to ensure the ID matches the password."
    )
    @pytest.mark.parametrize("repeat", range(5))
    def test_check_user_credentials_and_password(
        self, class_endpoint_client: EndpointClient, auth_token, repeat
    ):
        # Step 1: Get all user credentials
        with allure.step("Requesting all user credentials"):
            response_get_data = send_request(
                UserService.get_all_id_and_password,
                class_endpoint_client,
                auth_token,
                schema=AllPasswordAndId,
                validate_list=True,
            )
            user_ids = [user.id for user in response_get_data]
            user_passwords = {user.id: user.password for user in response_get_data}
            assert len(user_ids) == len(user_passwords)

        # Step 2: Validate that ID matches password for random users
        with allure.step("Checking ID-password match for random users"):
            for _ in range(10):
                random_user_id = random.choice(user_ids)
                user_credentials_response = send_request(
                    UserService.get_all_id_and_password_for_user,
                    class_endpoint_client,
                    auth_token,
                    schema=AllPasswordAndId,
                    data=random_user_id,
                )
                assert user_credentials_response.id == random_user_id
                assert (
                    user_credentials_response.password == user_passwords[random_user_id]
                )

    @allure.title("Validate schema of user credentials response")
    @allure.description(
        "Validate the schema of the response to ensure the structure is correct."
    )
    @pytest.mark.parametrize("repeat", range(5))
    def test_validate_user_credentials_schema(
        self, class_endpoint_client: EndpointClient, auth_token, repeat
    ):
        # Step 1: Get all user credentials
        with allure.step("Requesting all user credentials for schema validation"):
            send_request(
                UserService.get_all_id_and_password,
                class_endpoint_client,
                auth_token,
                schema=AllPasswordAndId,
                validate_list=True,
            )

    @allure.title("Check user credentials and ID-password matching with invalid IDs")
    @allure.description(
        "Test the user credentials API with invalid IDs and passwords to ensure proper error handling."
    )
    def test_check_invalid_user_credentials_and_password(
        self, class_endpoint_client: EndpointClient, auth_token
    ):
        invalid_user_ids = [i for i in range(800, 900)]
        with allure.step("Checking ID-password match for invalid users"):
            for user_id in invalid_user_ids:
                send_request(
                    UserService.get_all_id_and_password_for_user,
                    class_endpoint_client,
                    auth_token,
                    data=user_id,
                    except_code=404,
                )


@allure.feature("Users API")
@allure.story("User Retrieval by Identifier")
class TestUserIdentifier:
    """
    Test suite for verifying user retrieval using the 'user_identifier' parameter.

    This test ensures that the API correctly returns user details when queried with valid user identifiers.
    The test fetches a list of all users, randomly selects 10 user identifiers,
    and then requests user details for each of them individually.
    """

    @allure.title("Check user retrieval by user_identifier")
    @allure.description(
        "Fetch a list of users, select 10 random usernames, and request each user by user_identifier. "
        "Ensure that the API correctly returns user details with a 200 OK response."
    )
    @pytest.mark.parametrize("repeat", range(5))
    def test_get_user_by_identifier(self, class_endpoint_client, auth_token, repeat):
        """
        Test retrieving users by their user_identifier using random selection.

        Steps:
        1. Fetch the list of all users.
        2. Extract usernames from the response.
        3. Randomly select 10 usernames.
        4. Request user details for each selected username.
        5. Verify that the response status code is HTTP 200 OK.
        """
        # Step 1: Obtain an authentication token
        with allure.step("Requesting list of users"):
            # Step 2: Fetch all users from the API
            response = send_request(
                UserService.get_all_users,
                class_endpoint_client,
                auth_token,
                schema=GetAllUsersList,
                validate_list=True,
            )

            # Step 3: Extract usernames from the response
            usernames = [user.username for user in response]

        # Step 4: Select 10 random usernames
        random_usernames = random.sample(usernames, min(10, len(usernames)))

        for username in random_usernames:
            with allure.step(f"Requesting user by user_identifier: {username}"):
                # Step 5: Request user details by user_identifier
                send_request(
                    UserService.get_user_endpoint,
                    class_endpoint_client,
                    auth_token,
                    data=username,
                )
                # Step 6: Attach response details to Allure report for debugging
                allure.attach(
                    str(response),
                    name=f"Response for user_identifier: {username}",
                    attachment_type=allure.attachment_type.TEXT,
                )


@allure.feature("Users API")
@allure.story("Full cycle of checks for obtaining user ID and password")
class TestSearchUserByPasswordId:
    """
    The test checks whether the data passed in the request is valid with respect to the id and password.

    1. Query with user list - get random ids
    2. send the request and check that the id has a password.
    3. send a request by id and see that there is a password and it matches the list from the second request.
    """

    @staticmethod
    def generate_random_id_dict(user_list, count=10):
        random_users = random.sample(user_list, min(count, len(user_list)))
        return {user.id: f"{user.id}" for user in random_users}

    @allure.title("Get all users")
    @allure.description("Test retrieving the list of all users.")
    def test_get_all_users(
        self, class_endpoint_client, auth_token, id_password_dict_fixture
    ):
        with allure.step("Sending request to retrieve all users"):
            response = send_request(
                UserService.get_all_users,
                class_endpoint_client,
                auth_token,
                schema=GetAllUsersList,
                validate_list=True,
            )

        id_password_dict_fixture.update(
            self.generate_random_id_dict(response, count=10)
        )
        allure.attach(
            str(id_password_dict_fixture), name="Generated ID-Password Dictionary"
        )

    @allure.title("Get all ID and passwords")
    @allure.description("Test retrieving the list of all ID and passwords.")
    def test_get_all_id_and_passwords(
        self, class_endpoint_client, auth_token, id_password_dict_fixture
    ):
        with allure.step("Requesting ID and passwords for all users"):
            response = send_request(
                UserService.get_all_id_and_password,
                class_endpoint_client,
                auth_token,
                schema=AllPasswordAndId,
                validate_list=True,
            )

        response_dict = {user.id: user.password for user in response}
        allure.attach(str(response_dict), name="Received ID-Password Data")

        with allure.step("Validating received data with generated dictionary"):
            assert (
                id_password_dict_fixture
            ), "id_password_dict_fixture is empty. Ensure test_get_all_users runs before this test."
            for user_id, password in id_password_dict_fixture.items():
                assert (
                    user_id in response_dict
                ), f"User ID {user_id} not found in response"

    @allure.title("Test get user info")
    @allure.description("Test retrieving user info by ID.")
    @pytest.mark.parametrize("repeat", range(10))
    def test_get_user_info(
        self, class_endpoint_client, auth_token, id_password_dict_fixture, repeat
    ):
        with allure.step("Randomly selecting user IDs"):
            random_user_ids = random.sample(
                list(id_password_dict_fixture.keys()),
                min(5, len(id_password_dict_fixture)),
            )
            for user_id in random_user_ids:
                with allure.step(f"Requesting user info for user ID: {user_id}"):
                    send_request(
                        UserService.get_all_id_and_password_for_user,
                        class_endpoint_client,
                        auth_token,
                        schema=AllPasswordAndId,
                        data=user_id,
                    )


@allure.feature("Users API -> get zero login user")
@allure.story("Сheck the list of unlogged users ")
class TestZeroLoginUser:
    """
    The test checks whether the list of zero-logged users is correct.
    The test fetches a list of all users, and then checks that all users have 'last_login' as null,
    'login_count' as 0, and 'err_login_count' as 0.
    """

    @allure.title("Get zero login users")
    @allure.description("Test retrieving the list of zero-logged users.")
    def test_get_zero_login_users(self, class_endpoint_client, auth_token):
        with allure.step("Requesting zero users login"):
            users = send_request(
                UserService.get_zero_count_user,
                class_endpoint_client,
                auth_token,
                schema=GetAllUsersList,
                validate_list=True,
            )

        with allure.step("Check if all users have 'last_login' as null"):
            for user in users:
                assert (
                    user.last_login is None
                ), f"User {user.username} has a non-null 'last_login'"

        with allure.step("Check if all users have 'login_count' == 0"):
            for user in users:
                assert (
                    user.login_count == 0
                ), f"User {user.username} has a null 'login_count'"

        with allure.step("Check if all users have 'err_login_count' == 0"):
            for user in users:
                assert (
                    user.err_login_count == 0
                ), f"User {user.username} has a null 'err_login_count'"
