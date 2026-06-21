from typing import Type

import allure
from jsonschema import validate
from pydantic import BaseModel


@allure.step("Validating schema")
def validate_schema(instance: dict, schema_model: Type[BaseModel]) -> None:
    schema = schema_model.schema()
    validate(instance=instance, schema=schema)
