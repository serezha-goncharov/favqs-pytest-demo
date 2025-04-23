from dataclasses import dataclass
from enum import Enum


class Messages(str, Enum):
    RAW_401_MESSAGE = "HTTP Token: Access denied.\n"
    LOGOUT_MESSAGE = "User logged out."


@dataclass(frozen=True)
class Error:
    code: int
    message: str


class Errors(Enum):
    INVALID_LOGIN_OR_PASSWORD = Error(code=21, message="Invalid login or password.")
    USER_SESSION_NOT_FOUND = Error(code=20, message="User session not found.")
    USER_NOT_FOUND = Error(code=30, message="User not found.")

    @property
    def code(self) -> int:
        return self.value.code

    @property
    def message(self) -> str:
        return self.value.message


class StatusCodes(int, Enum):
    code_200 = 200
    code_401 = 401
    code_404 = 404


class HttpMethods(str, Enum):
    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"


class Endpoints(str, Enum):
    session: str = "session"
    quotes: str = "quotes"
    users: str = "users"
