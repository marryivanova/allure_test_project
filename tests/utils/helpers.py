import json
import allure
from http import HTTPStatus
from pydantic import ValidationError


from tests.utils.assertions.base.solutions import assert_status_code


def extract_json(response):
    try:
        return response.json()
    except ValueError:
        raise ValueError(f"Response content is not valid JSON: {response.text}")


def attach_json_data(name, data):
    """Attach JSON data to the allure report."""
    allure.attach(
        json.dumps(data, indent=2, ensure_ascii=False),
        name=name,
        attachment_type=allure.attachment_type.JSON,
    )


def validate_status_code(response, expected_status=HTTPStatus.OK):
    """Validate the status code of the response."""
    if response.status_code != expected_status:
        allure.attach(
            response.text,
            name=f"Response for status code {expected_status}",
            attachment_type=allure.attachment_type.TEXT,
        )
    else:
        assert_status_code(response.status_code, expected_status)


def validate_json_response(response):
    """Extract JSON from the response and ensure it's not None."""
    json_data = extract_json(response)
    assert json_data is not None, "Response must contain JSON."
    return json_data


def validate_data_schema(json_data, schema, validate_list=False):
    """Validate the response data against the given schema."""
    if schema == int:
        assert isinstance(json_data, int), f"Expected int, but got {type(json_data)}"
        return json_data

    if schema:
        try:
            if validate_list:
                return [
                    schema(**item) if isinstance(item, dict) else item
                    for item in json_data
                ]
            return schema(**json_data)
        except ValidationError as e:
            allure.attach(
                str(e),
                name="Validation Error",
                attachment_type=allure.attachment_type.TEXT,
            )
            raise AssertionError(
                f"Response does not match the expected schema {schema}: {e}"
            )


def send_request(
    request_func,
    client,
    token,
    schema=None,
    validate_list=False,
    data=None,
    except_code=False,
):
    """
    Universal method for sending a request and validating the response.

    :param request_func: The function that makes the request.
    :param client: The EndpointClient instance.
    :param token: Authentication token.
    :param schema: Pydantic model for validating the response (optional).
    :param validate_list: True if a list of objects is expected (optional).
    :param data: Additional data to send with the request (optional).
    :param except_code: Expected status code (optional).
    :return: JSON response.
    """
    with allure.step(f"Sending request: {request_func.__name__}"):
        if data:
            attach_json_data("Request Data", data)
            response = request_func(client, token, data)
        else:
            response = request_func(client, token)

    with allure.step("Checking status code"):
        if except_code:
            assert (
                response.status_code == except_code
            ), f"Expected status code {except_code}, but got {response.status_code}"
        validate_status_code(response)

    json_data = validate_json_response(response)

    with allure.step("Attaching response data"):
        attach_json_data("Response Data", json_data)

    return validate_data_schema(json_data, schema, validate_list)
