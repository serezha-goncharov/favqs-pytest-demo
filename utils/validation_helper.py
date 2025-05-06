from pydantic import ValidationError
from requests import Response

from api.models import BaseSchema


class SchemaValidationError(AssertionError):
    """Custom exception for schema validation errors"""

    pass


class ResponseBodyValidationError(AssertionError):
    """Custom exception for response body validation errors"""

    pass


def validate_schema(actual_schema: Response, expected_schema: type[BaseSchema]) -> BaseSchema:
    try:
        return expected_schema.model_validate(actual_schema.json())
    except ValidationError as error:
        raise SchemaValidationError(f"Schema validation failed\n{error}")


def validate_response_body(actual_response: str, expected_response: str) -> None:
    try:
        assert expected_response == actual_response
    except ValidationError as error:
        raise ResponseBodyValidationError(f"Schema validation failed\n{error}")
