import allure

from faker import Faker

from api.consts import StatusCodes, Messages
from tests.login.login_models import LoginResponse, LoginWithWrongCredsResponse
from utils.json import format_json

fake = Faker()


@allure.story("POST /session")
class TestLogin:
    @allure.title("User login")
    def test_login(self, api_client_without_login, user):
        response = api_client_without_login.login(login=user.login, password=user.password)
        allure.attach(
            body=format_json(response.json()),
            name="Response Body",
            attachment_type=allure.attachment_type.JSON,
        )
        with allure.step("Status code 200"):
            assert response.status_code == StatusCodes.code_200
        with allure.step("Schema validation"):
            assert api_client_without_login.validate_schema(response=response, model=LoginResponse)

    @allure.title("User login with wrong creds")
    def test_login_with_wrong_creds(self, api_client):
        response = api_client.login(login=fake.user_name(), password=fake.password())
        allure.attach(
            body=format_json(response.json()),
            name="Response Body",
            attachment_type=allure.attachment_type.JSON,
        )
        with allure.step("Status code 200"):
            assert response.status_code == StatusCodes.code_200
        with allure.step("Schema validation"):
            assert api_client.validate_schema(response=response, model=LoginWithWrongCredsResponse)

    @allure.title("User login without Authorization header")
    def test_login_without_auth_header(self, api_client, user):
        response = api_client.login(login=user.login, password=user.password, auth=False)
        allure.attach(
            body=response.text,
            name="Response Body",
            attachment_type=allure.attachment_type.TEXT,
        )
        with allure.step("Status code 401"):
            assert response.status_code == StatusCodes.code_401
        with allure.step("Schema validation"):
            assert response.text == Messages.RAW_401_MESSAGE
