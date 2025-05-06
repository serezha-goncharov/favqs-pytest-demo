import os

import platform
import pytest
from faker import Faker

from api.client import FavqsApiClient
from settings import settings
from tests.users.user_models import UserModel

PYTHON_VERSION = platform.python_version()
fake = Faker()


def pytest_addoption(parser):
    parser.addoption(
        "--base-url",
        action="store",
        help="Overriding the base URL from configuration",
    )


@pytest.fixture(scope="session")
def base_url(request) -> str:
    return request.config.getoption("--base-url") or settings.BASE_URL


@pytest.fixture(scope="session", autouse=True)
def setup_environment_report(base_url: str) -> None:
    env_file = os.path.join("reports/json", "environment.properties")
    os.makedirs(os.path.dirname(env_file), exist_ok=True)

    with open(env_file, "w", encoding="utf-8") as f:
        f.write(f"base_url={base_url}\n")
        f.write("api_version=v2")
        f.write(f"python_version={PYTHON_VERSION}")


@pytest.fixture(scope="session")
def user(api_client) -> UserModel:
    user_model = UserModel(login=fake.user_name(), email=fake.email(), password=fake.password())
    api_client.create_user(login=user_model.login, email=user_model.email, password=user_model.password)
    api_client.logout()
    return user_model


@pytest.fixture(scope="session")
def api_client(base_url: str) -> FavqsApiClient:
    return FavqsApiClient(base_url=base_url)


@pytest.fixture(scope="class")
def auth_api_client(api_client: FavqsApiClient, user) -> FavqsApiClient:
    api_client.login(login=user.login, password=user.password)
    yield api_client
    api_client.logout()


@pytest.fixture(scope="module")
def api_client_without_login(api_client: FavqsApiClient) -> FavqsApiClient:
    yield api_client
    api_client.logout()


@pytest.fixture(scope="function")
def api_client_without_logout(api_client: FavqsApiClient, user) -> FavqsApiClient:
    api_client.login(login=user.login, password=user.password)
    yield api_client
