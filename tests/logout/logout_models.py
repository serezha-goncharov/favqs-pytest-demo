from pydantic import EmailStr, Field, field_validator

from api.consts import Errors, Messages
from api.models import BaseSchema


class LogoutResponse(BaseSchema):
    message: str

    @field_validator("message")
    def validate_error_code(cls, message):
        if message != Messages.LOGOUT_MESSAGE:
            raise ValueError(f"Wrong message: '{message}' vs '{Messages.LOGOUT_MESSAGE}'")
        return message


class MissedUserTokenResponse(BaseSchema):
    error_code: int
    message: str

    @field_validator("error_code")
    def validate_error_code(cls, error_code):
        if error_code != Errors.USER_SESSION_NOT_FOUND.code:
            raise ValueError(f"Wrong error code: '{error_code}' vs '{Errors.USER_SESSION_NOT_FOUND.code}'")
        return error_code

    @field_validator("message")
    def validate_message(cls, message):
        if message != Errors.USER_SESSION_NOT_FOUND.message:
            raise ValueError(f"Wrong message: '{message}' vs '{Errors.USER_SESSION_NOT_FOUND.message}'")
        return message
