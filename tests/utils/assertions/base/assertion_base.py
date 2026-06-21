from contextlib import contextmanager
from typing import Callable, ContextManager, TypeVar

from tests.utils.assertions.base.assertion_types import AssertionTypes

t = TypeVar("t")
StepProvider = Callable[[str], ContextManager]


@contextmanager
def default_step_provider(step: str):
    yield


class AssertionBase:
    """
    A base class for creating assertion objects.

    This class provides a foundation for building custom assertion objects
    with configurable descriptions and step providers.
    """

    def __init__(self, expected: t) -> None:
        """
        Initialize an AssertionBase object.

        Args:
            expected (T): The expected value for the assertion.
        """
        self.expected = expected
        self._description: str | None = None
        self._step_provider: StepProvider = default_step_provider

    def _error_template(self, actual: t, method: AssertionTypes):
        """
        Generate an error message template for failed assertions.

        Args:
            actual (T): The actual value that didn't meet the assertion.
            method (AssertionTypes): The type of assertion that failed.

        Returns:
            str: A formatted error message string.
        """
        return f"""
        Checking: {self._description}
        Expected: {self.expected} {type(self.expected)}
        Actual: {actual} {type(actual)}

        Expression: assert {self.expected} {method} {actual}
        """

    def set_description(self, description: str):
        """
        Set a description for the assertion.

        Args:
            description (str): A string describing the assertion.

        Returns:
            AssertionBase: The current instance for method chaining.
        """
        self._description = description
        return self

    @property
    def step_provider(self) -> StepProvider:
        """
        Get the current step provider.

        Returns:
            StepProvider: The current step provider function.
        """
        return self._step_provider

    @step_provider.setter
    def step_provider(self, provider: StepProvider):
        """
        Set a new step provider.

        Args:
            provider (StepProvider): A new step provider function to be used.
        """
        self._step_provider = provider
