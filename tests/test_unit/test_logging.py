import pytest
import allure
import logging
from fastapi import HTTPException
from src.helpers.logging import log_and_raise_exception, current_username


@allure.feature("Logging Filter")
@allure.story("Filter Username")
@allure.description("Test log filter with different usernames, including edge cases.")
@pytest.mark.parametrize(
    "initial_username, expected_username",
    [
        (None, "anonymous"),
        ("test_user", "test_user"),
        ("", "anonymous"),
        ("123", "123"),
        ("!@#$%", "!@#$%"),
    ],
)
def test_filter_username(log_filter, initial_username, expected_username):
    with allure.step("Create a log record"):
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Test message",
            args=(),
            exc_info=None,
        )

    with allure.step(
        f"Set current username to '{initial_username}'"
        if initial_username
        else "No username set"
    ):
        if initial_username is not None:
            from src.helpers.logging import current_username

            current_username.set(initial_username)

    with allure.step("Apply log filter"):
        log_filter.filter(record)

    with allure.step(f"Verify that username is '{expected_username}'"):
        assert record.username == expected_username


@allure.feature("Logging Filter")
@allure.story("Filter Anonymous Username")
@allure.description(
    "Test that the logging filter assigns 'anonymous' to the username field when no username is set."
)
def test_filter_anonymous_username(log_filter):
    with allure.step("Create a log record"):
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Test message",
            args=(),
            exc_info=None,
        )

    with allure.step("Apply log filter"):
        log_filter.filter(record)

    with allure.step("Verify that username is 'anonymous'"):
        assert record.username == "anonymous"


@allure.feature("Logging Filter")
@allure.story("Set Current Username")
@allure.description(
    "Test that the logging filter correctly assigns the current username."
)
def test_filter_set_current_username(log_filter):
    with allure.step("Create a log record"):
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Test message",
            args=(),
            exc_info=None,
        )

    with allure.step("Set current username"):
        current_username.set("test_user")

    with allure.step("Apply log filter"):
        log_filter.filter(record)

    with allure.step("Verify that username is 'test_user'"):
        assert record.username == "test_user"


@allure.feature("Logging Filter")
@allure.story("Different Log Levels")
@allure.description(
    "Test that the logging filter applies correctly across different log levels."
)
def test_filter_different_log_levels(log_filter):
    log_levels = [
        logging.INFO,
        logging.DEBUG,
        logging.ERROR,
        logging.WARNING,
        logging.CRITICAL,
    ]

    with allure.step("Test log levels with default anonymous username"):
        for level in log_levels:
            record = logging.LogRecord(
                name="test",
                level=level,
                pathname="",
                lineno=0,
                msg="Test message",
                args=(),
                exc_info=None,
            )
            log_filter.filter(record)
            assert record.username == "anonymous"

    with allure.step("Set current username"):
        current_username.set("test_user")

    with allure.step("Test log levels with set username"):
        for level in log_levels:
            record = logging.LogRecord(
                name="test",
                level=level,
                pathname="",
                lineno=0,
                msg="Test message",
                args=(),
                exc_info=None,
            )
            log_filter.filter(record)
            assert record.username == "test_user"


@allure.feature("Logging and Exception Handling")
@allure.story("Raise Exception with Logging")
@allure.description("Test that exceptions are logged and raised correctly.")
def test_log_and_raise_exception(caplog):
    with pytest.raises(HTTPException) as http_exception:
        with allure.step("Capture logs at ERROR level"):
            with caplog.at_level(logging.ERROR, logger=__name__):
                log_and_raise_exception(ValueError("Test error"), 400, "Test message")

    with allure.step("Verify log entry and exception"):
        assert len(caplog.records) == 1
        assert caplog.records[0].getMessage() == "Test message"
        assert http_exception.value.status_code == 400
        assert http_exception.value.detail == "Test message"


@allure.feature("Logging and Exception Handling")
@allure.story("Different Exception Types")
@allure.description(
    "Test logging and raising exceptions with different exception types."
)
def test_log_and_raise_exception_different_exceptions(caplog):
    exceptions = [
        (ValueError("Value error"), 400, "Value error occurred"),
        (TypeError("Type error"), 500, "Type error occurred"),
        (KeyError("Key error"), 404, "Key error occurred"),
    ]

    for exc, status_code, message in exceptions:
        with pytest.raises(HTTPException) as http_exception:
            with allure.step(f"Capture logs for {exc.__class__.__name__}"):
                with caplog.at_level(logging.ERROR, logger=__name__):
                    log_and_raise_exception(exc, status_code, message)

        with allure.step("Verify exception details"):
            assert http_exception.value.status_code == status_code
            assert http_exception.value.detail == message
