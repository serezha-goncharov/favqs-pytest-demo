from datetime import datetime

from pydantic import HttpUrl, EmailStr, Field, field_validator
from typing import Optional, Literal

from api.consts import Errors
from api.models import BaseSchema


class AccountDetails(BaseSchema):
    email: EmailStr
    private_favorites_count: int
    pro_expiration: Optional[datetime] = None


class LoggedInUser(BaseSchema):
    login: str
    pic_url: HttpUrl
    public_favorites_count: int
    following: int
    followers: int
    pro: Literal[None, True] = None
    account_details: Optional[AccountDetails] = None


class UserModel(BaseSchema):
    login: str = Field(min_length=1, max_length=20)
    email: EmailStr
    password: str = Field(min_length=5, max_length=120)


class NonExistentUser(BaseSchema):
    error_code: int
    message: str

    @field_validator("error_code")
    def validate_error_code(cls, error_code):
        if error_code != Errors.USER_NOT_FOUND.code:
            raise ValueError(f"Wrong error code: '{error_code}' vs '{Errors.USER_NOT_FOUND.code}'")
        return error_code

    @field_validator("message")
    def validate_message(cls, message):
        if message != Errors.USER_NOT_FOUND.message:
            raise ValueError(f"Wrong message: '{message}' vs '{Errors.USER_NOT_FOUND.message}'")
        return message


class CreatedUser(BaseSchema):
    user_token: str = Field(alias="User-Token")
    login: str
