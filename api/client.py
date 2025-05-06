import requests

from copy import deepcopy
from requests import Response
from settings import settings
from api.consts import HttpMethods, Endpoints


class BaseApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/vnd.favqs.v2+json",
            }
        )

    def send_request(self, method: str, endpoint: str, auth: bool = True, **kwargs) -> Response:
        # Сохраняем оригинальные заголовки сессии
        original_headers = deepcopy(self.session.headers)

        try:
            if auth:
                self.session.headers.update({"Authorization": f"Token token={settings.API_KEY.get_secret_value()}"})

            return self.session.request(method=method, url=f"{self.base_url}/{endpoint}", **kwargs)
        finally:
            # Восстанавливаем оригинальные заголовки
            self.session.headers.clear()
            self.session.headers.update(original_headers)


class SessionMethods(BaseApiClient):
    """Методы для работы с сессиями"""

    def login(self, login: str, password: str, auth: bool = True):
        response = self.send_request(
            method=HttpMethods.POST,
            endpoint=Endpoints.session,
            auth=auth,
            json={"user": {"login": login, "password": password}},
        )
        if auth:
            self.session.headers.update({"User-Token": response.json().get("User-Token")})
        return response

    def logout(self, auth: bool = True):
        return self.send_request(
            method=HttpMethods.DELETE,
            endpoint=Endpoints.session,
            auth=auth,
        )


class QuotesMethods(BaseApiClient):
    """Методы для работы с цитатами"""

    def get_quotes(self, auth: bool = True, **params):
        return self.send_request(
            method=HttpMethods.GET,
            endpoint=Endpoints.quotes,
            auth=auth,
            params=params,
        )

    def get_quote_by_id(self, quote_id: int, auth: bool = True):
        return self.send_request(
            method=HttpMethods.GET,
            endpoint=f"{Endpoints.quotes}/{quote_id}",
            auth=auth,
        )

    def create_quote(self, author: str, body: str, auth: bool = True):
        return self.send_request(
            method=HttpMethods.POST,
            endpoint=Endpoints.quotes,
            auth=auth,
            json={
                "quote": {
                    "author": author,
                    "body": body,
                }
            },
        )


class UsersMethods(BaseApiClient):
    """Методы для работы с пользователями"""

    def create_user(self, login: str, email: str, password: str, auth: bool = True):
        return self.send_request(
            method=HttpMethods.POST,
            endpoint=Endpoints.users,
            auth=auth,
            json={"user": {"login": login, "email": email, "password": password}},
        )

    def get_user(self, login: str, auth: bool = True):
        return self.send_request(
            method=HttpMethods.GET,
            endpoint=f"{Endpoints.users}/{login}",
            auth=auth,
        )


class FavqsApiClient(
    SessionMethods,
    QuotesMethods,
    UsersMethods,
):
    """Финальный клиент, объединяющий все методы"""

    def __init__(self, base_url):
        super().__init__(base_url)
