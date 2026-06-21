from enum import Enum


class AssertionTypes(str, Enum):
    equal = "=="
    not_equal = "!="
    length = "is length"
    in_ = "is in"
