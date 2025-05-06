import allure

from faker import Faker

from api.consts import StatusCodes, Messages
from tests.login.login_models import LoginResponse, LoginWithWrongCredsResponse
from utils.json_helper import format_json
from utils.validation_helper import validate_schema, validate_response_body, validate_status_code

fake = Faker()


@allure.story("POST /session")
class TestLogin:
    @allure.title("User login")
    def test_login(self, api_client_without_login, user):
        with allure.step("Send request"):
            response = api_client_without_login.login(login=user.login, password=user.password)
            allure.attach(
                body=response.url,
                name="URL",
                attachment_type=allure.attachment_type.TEXT,
            )
            allure.attach(
                body=format_json(response.json()),
                name="Response Body",
                attachment_type=allure.attachment_type.JSON,
            )
        with allure.step("Status code 200"):
            validate_status_code(actual_status_code=response.status_code, expected_status_code=StatusCodes.code_200)
        with allure.step("Schema validation"):
            validate_schema(actual_schema=response, expected_schema=LoginResponse)

    @allure.title("User login with wrong creds")
    def test_login_with_wrong_creds(self, api_client):
        with allure.step("Send request"):
            response = api_client.login(login=fake.user_name(), password=fake.password())
            allure.attach(
                body=response.url,
                name="URL",
                attachment_type=allure.attachment_type.TEXT,
            )
            allure.attach(
                body=format_json(response.json()),
                name="Response Body",
                attachment_type=allure.attachment_type.JSON,
            )
        with allure.step("Status code 200"):
            validate_status_code(actual_status_code=response.status_code, expected_status_code=StatusCodes.code_200)
        with allure.step("Schema validation"):
            validate_schema(actual_schema=response, expected_schema=LoginWithWrongCredsResponse)

    @allure.title("User login without Authorization header")
    def test_login_without_auth_header(self, api_client, user):
        with allure.step("Send request"):
            response = api_client.login(login=user.login, password=user.password, auth=False)
            allure.attach(
                body=response.url,
                name="URL",
                attachment_type=allure.attachment_type.TEXT,
            )
            allure.attach(
                body=response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.TEXT,
            )
        with allure.step("Status code 401"):
            validate_status_code(actual_status_code=response.status_code, expected_status_code=StatusCodes.code_401)
        with allure.step("Response body validation"):
            validate_response_body(actual_response=response.text, expected_response=Messages.RAW_401_MESSAGE)
