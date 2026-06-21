import pytest
import allure
from datetime import datetime
from tests.utils.fakers import generate_random_time_data
from src.helpers.date_utils import parse_and_normalize_datetimes


@allure.epic("Date Utilities")
@allure.feature("parse_and_normalize_datetimes")
@allure.story("Validation of datetime parsing and normalization")
@pytest.mark.parametrize(
    "start_datetime, end_datetime, expected_difference_hours",
    generate_random_time_data(10),
)
def test_parse_and_normalize_datatimes(
    start_datetime, end_datetime, expected_difference_hours
):
    with allure.step("Call the function with provided datetimes"):
        result = parse_and_normalize_datetimes(start_datetime, end_datetime)

    with allure.step("Validate the result type and structure"):
        assert isinstance(result, tuple), "Result should be a tuple"
        assert len(result) == 2, "Result tuple should contain exactly 2 elements"
        assert all(
            isinstance(dt, datetime) for dt in result
        ), "Both elements should be datetime instances"

    with allure.step("Validate timezone normalization"):
        assert result[0].tzinfo is None, "Start datetime should be timezone-naive"
        assert result[1].tzinfo is None, "End datetime should be timezone-naive"

    with allure.step("Validate the chronological order of datetimes"):
        assert (
            result[0] < result[1]
        ), "Start datetime should be earlier than end datetime"
