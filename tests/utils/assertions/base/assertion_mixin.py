from typing import TypeVar

from tests.utils.assertions.base.assertion_base import AssertionBase
from tests.utils.assertions.base.assertion_types import AssertionTypes

t = TypeVar("t")


class AssertionMixin(AssertionBase):
    """
    A mixin class that provides assertion methods for testing.
    """

    def is_length(self, length: int):
        """
        Checks if the expected value has the specified length.

        Args:
            length (int): The expected length to check against.

        Raises:
            NotImplementedError: If the expected value doesn't have a length attribute.

        Returns:
            self: Returns the instance for method chaining.
        """
        step_name = f'Checking that "{self._description}" has {length} length'
        with self.step_provider(step_name):

            if not hasattr(self.expected, "__len__"):
                raise NotImplementedError(
                    f'The expected value "{self.expected}" {type(self.expected)} has no length attribute'
                )

            template = self._error_template(length, AssertionTypes.length)
            assert length == len(self.expected), template

        return self

    def to_be_equal(self, actual: t):
        """
        Checks if the expected value is equal to the actual value.

        Args:
            actual (T): The actual value to compare against the expected value.

        Returns:
            self: Returns the instance for method chaining.
        """
        step_name = f'Checking that "{self._description}" equals to "{self.expected}"'
        with self.step_provider(step_name):
            template = self._error_template(actual, AssertionTypes.equal)
            assert self.expected == actual, template

        return self

    def not_to_be_equal(self, actual: t):
        """
        Checks if the expected value is not equal to the actual value.

        Args:
            actual (T): The actual value to compare against the expected value.

        Returns:
            self: Returns the instance for method chaining.
        """
        step_name = (
            f'Checking that "{self._description}" not equals to "{self.expected}"'
        )
        with self.step_provider(step_name):
            template = self._error_template(actual, AssertionTypes.not_equal)
            assert self.expected != actual, template

        return self

    def in_(self, actual: t):
        """
        Checks if the expected value is in the actual value.

        Args:
            actual (T): The actual value to check if it contains the expected value.

        Returns:
            self: Returns the instance for method chaining.
        """
        step_name = f'Checking that "{self._description}" in "{self.expected}"'
        with self.step_provider(step_name):
            template = self._error_template(actual, AssertionTypes.in_)
            assert self.expected != actual, template

        return self
