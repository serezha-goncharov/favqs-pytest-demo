import allure

from faker import Faker

from api.consts import StatusCodes, Messages
from tests.users.user_models import GetUserResponse, GetNonExistentUserResponse, CreateUserResponse
from utils.json import format_json

fake = Faker()


@allure.story("GET /api/users/:login")
class TestGetUsers:
    @allure.title("Get user")
    def test_get_user(self, auth_api_client, user):
        response = auth_api_client.get_user(login=user.login)
        allure.attach(
            body=format_json(response.json()),
            name="Response Body",
            attachment_type=allure.attachment_type.JSON,
        )
        with allure.step("Status code 200"):
            assert response.status_code == StatusCodes.code_200
        with allure.step("Schema validation"):
            auth_api_client.validate_schema(response=response, model=GetUserResponse)

    @allure.title("Get non-existent user")
    def test_get_non_existent_user(self, auth_api_client):
        response = auth_api_client.get_user(login=fake.user_name())
        allure.attach(
            body=format_json(response.json()),
            name="Response Body",
            attachment_type=allure.attachment_type.JSON,
        )
        with allure.step("Status code 404"):
            assert response.status_code == StatusCodes.code_404
        with allure.step("Schema validation"):
            auth_api_client.validate_schema(response=response, model=GetNonExistentUserResponse)

    @allure.title("Get user without Authorization header")
    def test_get_user_without_auth_header(self, auth_api_client, user):
        response = auth_api_client.get_user(login=user.login, auth=False)
        allure.attach(
            body=response.text,
            name="Response Body",
            attachment_type=allure.attachment_type.TEXT,
        )
        with allure.step("Status code 401"):
            assert response.status_code == StatusCodes.code_401
        with allure.step("Schema validation"):
            assert response.text == Messages.RAW_401_MESSAGE


@allure.story("POST /users")
class TestCreateUsers:
    @allure.title("Create user")
    def test_create_user(self, api_client_without_login):
        response = api_client_without_login.create_user(login=fake.user_name(), email=fake.email(), password=fake.password())
        allure.attach(
            body=format_json(response.json()),
            name="Response Body",
            attachment_type=allure.attachment_type.JSON,
        )
        with allure.step("Status code 200"):
            assert response.status_code == StatusCodes.code_200
        with allure.step("Schema validation"):
            api_client_without_login.validate_schema(response=response, model=CreateUserResponse)

    @allure.title("Create user without Authorization header")
    def test_create_user_without_auth_header(self, api_client_without_login):
        response = api_client_without_login.create_user(
            login=fake.user_name(),
            email=fake.email(),
            password=fake.password(),
            auth=False,
        )
        allure.attach(
            body=response.text,
            name="Response Body",
            attachment_type=allure.attachment_type.TEXT,
        )
        with allure.step("Status code 401"):
            assert response.status_code == StatusCodes.code_401
        with allure.step("Schema validation"):
            assert response.text == Messages.RAW_401_MESSAGE
