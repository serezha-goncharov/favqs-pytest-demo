import allure

from faker import Faker

from api.consts import StatusCodes, Messages
from tests.logout.logout_models import LogoutResponse, LogoutWithoutUserTokenResponse
from utils.json import format_json

fake = Faker()


@allure.story("DELETE /session")
class TestLogout:
    @allure.title("User logout")
    def test_logout(self, api_client_without_logout, user):
        response = api_client_without_logout.logout()
        allure.attach(
            body=format_json(response.json()),
            name="Response Body",
            attachment_type=allure.attachment_type.JSON,
        )
        with allure.step("Status code 200"):
            assert response.status_code == StatusCodes.code_200
        with allure.step("Schema validation"):
            api_client_without_logout.validate_schema(response=response, model=LogoutResponse)

    @allure.title("User logout without user token")
    def test_logout_without_user_token(self, api_client):
        response = api_client.logout()
        allure.attach(
            body=format_json(response.json()),
            name="Response Body",
            attachment_type=allure.attachment_type.JSON,
        )
        with allure.step("Status code 200"):
            assert response.status_code == StatusCodes.code_200
        with allure.step("Schema validation"):
            api_client.validate_schema(response=response, model=LogoutWithoutUserTokenResponse)

    @allure.title("User logout without Authorization header")
    def test_logout_without_auth_header(self, api_client, user):
        response = api_client.logout(auth=False)
        allure.attach(
            body=response.text,
            name="Response Body",
            attachment_type=allure.attachment_type.TEXT,
        )
        with allure.step("Status code 401"):
            assert response.status_code == StatusCodes.code_401
        with allure.step("Schema validation"):
            assert response.text == Messages.RAW_401_MESSAGE
