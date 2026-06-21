from typing import TypeVar

import allure

from tests.utils.assertions.base.assertion_mixin import AssertionMixin

t = TypeVar("t")


def expect(expected: t) -> AssertionMixin:
    assertion = AssertionMixin(expected=expected)
    assertion.step_provider = allure.step

    return assertion
