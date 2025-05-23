import allure

from faker import Faker

from api.consts import StatusCodes, Messages
from tests.users.user_models import LoggedInUser, NonExistentUser, CreatedUser
from utils.json_helper import format_json
from utils.validation_helper import validate_response_body, validate_schema, validate_status_code

fake = Faker()


@allure.story("GET /api/users/:login")
class TestGetUsers:
    @allure.title("Get user")
    def test_get_user(self, auth_api_client, user):
        with allure.step("Send request"):
            response = auth_api_client.get_user(login=user.login)
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
            validate_schema(actual_schema=response, expected_schema=LoggedInUser)

    @allure.title("Get non-existent user")
    def test_get_non_existent_user(self, auth_api_client):
        with allure.step("Send request"):
            response = auth_api_client.get_user(login=fake.user_name())
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
        with allure.step("Status code 404"):
            validate_status_code(actual_status_code=response.status_code, expected_status_code=StatusCodes.code_404)
        with allure.step("Schema validation"):
            validate_schema(actual_schema=response, expected_schema=NonExistentUser)

    @allure.title("Get user without Authorization header")
    def test_get_user_without_auth_header(self, auth_api_client, user):
        with allure.step("Send request"):
            response = auth_api_client.get_user(login=user.login, auth=False)
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


@allure.story("POST /users")
class TestCreateUsers:
    @allure.title("Create user")
    def test_create_user(self, api_client_without_login):
        with allure.step("Send request"):
            response = api_client_without_login.create_user(login=fake.user_name(), email=fake.email(), password=fake.password())
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
            validate_schema(actual_schema=response, expected_schema=CreatedUser)

    @allure.title("Create user without Authorization header")
    def test_create_user_without_auth_header(self, api_client_without_login):
        with allure.step("Send request"):
            response = api_client_without_login.create_user(
                login=fake.user_name(),
                email=fake.email(),
                password=fake.password(),
                auth=False,
            )
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
