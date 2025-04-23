from pydantic import EmailStr, Field, field_validator

from api.consts import Errors, Messages
from api.models import BaseSchema


class LoginResponse(BaseSchema):
    user_token: str = Field(alias="User-Token")
    login: str
    email: EmailStr


class LoginWithWrongCredsResponse(BaseSchema):
    error_code: int
    message: str

    @field_validator("error_code")
    def validate_error_code(cls, error_code):
        if error_code != Errors.INVALID_LOGIN_OR_PASSWORD.code:
            raise ValueError(f"Wrong error code: '{error_code}' vs '{Errors.INVALID_LOGIN_OR_PASSWORD.code}'")
        return error_code

    @field_validator("message")
    def validate_message(cls, message):
        if message != Errors.INVALID_LOGIN_OR_PASSWORD.message:
            raise ValueError(f"Wrong message: '{message}' vs '{Errors.INVALID_LOGIN_OR_PASSWORD.message}'")
        return message
