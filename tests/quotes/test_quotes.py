import allure
import pytest

from api.consts import StatusCodes, Messages
from tests.quotes.quotes_models import QuotesResponse, Quote
from faker import Faker

from utils.json_helper import format_json

fake = Faker()


@allure.story("GET /quotes")
class TestGetQuotes:
    @allure.title("Get quotes")
    @pytest.mark.parametrize(
        "type_param,filter_param",
        (("user", "microfonchek"), ("tag", "wisdom"), ("author", "Mark Twain")),
    )
    def test_get_quotes(self, auth_api_client, type_param, filter_param):
        response = auth_api_client.get_quotes(type=type_param, filter=filter_param)
        allure.attach(
            body=format_json(response.json()),
            name="Response Body",
            attachment_type=allure.attachment_type.JSON,
        )

        with allure.step("Status code 200"):
            assert response.status_code == StatusCodes.code_200
        with allure.step("Schema validation"):
            auth_api_client.validate_schema(response=response, model=QuotesResponse)

    @allure.title("Get quotes without Authorization header")
    def test_get_quotes_without_auth_header(self, api_client):
        response = api_client.get_quotes(auth=False)
        allure.attach(
            body=response.text,
            name="Response Body",
            attachment_type=allure.attachment_type.TEXT,
        )
        with allure.step("Status code 401"):
            assert response.status_code == StatusCodes.code_401
        with allure.step("Schema validation"):
            assert response.text == Messages.RAW_401_MESSAGE


@allure.story("POST /quotes")
class TestPostQuotes:
    @allure.title("Create quotes for user")
    def test_create_quote(self, auth_api_client):
        response = auth_api_client.create_quote(author=fake.name(), body=fake.catch_phrase())
        allure.attach(
            body=format_json(response.json()),
            name="Response Body",
            attachment_type=allure.attachment_type.JSON,
        )
        with allure.step("Status code 200"):
            assert response.status_code == StatusCodes.code_200
        with allure.step("Schema validation"):
            auth_api_client.validate_schema(response=response, model=Quote)

    @allure.title("Create quotes for user without Authorization header")
    def test_create_quote_without_auth_header(self, auth_api_client):
        response = auth_api_client.create_quote(author=fake.name(), body=fake.catch_phrase(), auth=False)
        allure.attach(
            body=response.text,
            name="Response Body",
            attachment_type=allure.attachment_type.TEXT,
        )
        with allure.step("Status code 401"):
            assert response.status_code == StatusCodes.code_401
        with allure.step("Schema validation"):
            assert response.text == Messages.RAW_401_MESSAGE
