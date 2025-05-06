import allure

from faker import Faker

from api.consts import StatusCodes, Messages
from tests.logout.logout_models import LogoutResponse, LogoutWithoutUserTokenResponse
from utils.json_helper import format_json
from utils.validation_helper import validate_schema, validate_response_body, validate_status_code

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
            validate_status_code(actual_status_code=response.status_code, expected_status_code=StatusCodes.code_200)
        with allure.step("Schema validation"):
            validate_schema(actual_schema=response, expected_schema=LogoutResponse)

    @allure.title("User logout without user token")
    def test_logout_without_user_token(self, api_client):
        response = api_client.logout()
        allure.attach(
            body=format_json(response.json()),
            name="Response Body",
            attachment_type=allure.attachment_type.JSON,
        )
        with allure.step("Status code 200"):
            validate_status_code(actual_status_code=response.status_code, expected_status_code=StatusCodes.code_200)
        with allure.step("Schema validation"):
            validate_schema(actual_schema=response, expected_schema=LogoutWithoutUserTokenResponse)

    @allure.title("User logout without Authorization header")
    def test_logout_without_auth_header(self, api_client, user):
        response = api_client.logout(auth=False)
        allure.attach(
            body=response.text,
            name="Response Body",
            attachment_type=allure.attachment_type.TEXT,
        )
        with allure.step("Status code 401"):
            validate_status_code(actual_status_code=response.status_code, expected_status_code=StatusCodes.code_401)
        with allure.step("Response body validation"):
            validate_response_body(actual_response=response.text, expected_response=Messages.RAW_401_MESSAGE)
