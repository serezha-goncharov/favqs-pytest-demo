from pydantic import ValidationError
from requests import Response

from api.models import BaseSchema


class SchemaValidationError(AssertionError):
    """Custom exception for schema validation errors"""

    pass


class ResponseBodyError(AssertionError):
    """Custom exception for response body validation errors"""

    pass


class StatusCodeError(AssertionError):
    """Custom exception for status code validation errors"""

    pass


def validate_schema(actual_schema: Response, expected_schema: type[BaseSchema]) -> BaseSchema:
    try:
        return expected_schema.model_validate(actual_schema.json())
    except ValidationError as error:
        raise SchemaValidationError(f"Schema validation failed\n{error}")


def validate_response_body(actual_response: str, expected_response: str) -> None:
    try:
        assert actual_response == expected_response
    except AssertionError:
        raise ResponseBodyError(f"Response body validation failed: expected {expected_response}, got {actual_response}")


def validate_status_code(actual_status_code: int, expected_status_code: int) -> None:
    try:
        assert actual_status_code == expected_status_code
    except AssertionError:
        raise StatusCodeError(f"Status code validation failed: expected {expected_status_code}, got {actual_status_code}")
