import pytest
import requests
import allure
from api_testing.data import CREATE_COURIER_URL, LOGIN_COURIER_URL
from api_testing.methods.courier_methods import CourierMethods


class TestCourierCreation:

    @allure.title("Тест на успешное создание курьера")
    @allure.description("Проверяем, что курьер успешно создается с валидными данными")
    def test_create_courier_successful(self):
        courier_methods = CourierMethods()
        login, password, first_name = courier_methods.create_new_courier_credentials()
        response = requests.post(CREATE_COURIER_URL, json={
            "login": login,
            "password": password,
            "firstName": first_name
        })
        assert response.status_code == 201 and response.json() == {"ok": True}

    @allure.title("Тест на создание дублирующегося курьера")
    @allure.description("Проверяем, что при попытке создать курьера с существующим логином возвращается ошибка")
    def test_create_duplicate_courier(self, create_and_register_courier):
        login = create_and_register_courier["login"]
        password = create_and_register_courier["password"]
        first_name = create_and_register_courier["firstName"]
        response_duplicate = requests.post(CREATE_COURIER_URL, json={
            "login": login,
            "password": password,
            "firstName": first_name
        })
        assert response_duplicate.status_code == 409 and response_duplicate.json() == {
            "code": 409,
            "message": "Этот логин уже используется. Попробуйте другой."
        }

    @pytest.mark.parametrize("payload, expected_status, expected_response", [
        ({"password": "1234", "firstName": "saske"}, 400,
         {"code": 400, "message": "Недостаточно данных для создания учетной записи"}),
        ({"login": "ninja", "firstName": "saske"}, 400,
         {"code": 400, "message": "Недостаточно данных для создания учетной записи"})
    ])
    @allure.title("Тест на создание курьера с отсутствующими обязательными полями")
    @allure.description("Проверяем, что при отсутствии обязательных полей возвращается ошибка")
    def test_create_courier_missing_required_fields(self, payload, expected_status, expected_response):
        response = requests.post(CREATE_COURIER_URL, json=payload)
        assert response.status_code == expected_status and response.json() == expected_response

    @allure.title("Тест на успешный логин курьера")
    @allure.description("Проверяем, что курьер может успешно войти в систему с правильными учетными данными")
    def test_courier_success_login(self, create_and_register_courier):
        login = create_and_register_courier["login"]
        password = create_and_register_courier["password"]
        payload = {
            "login": login,
            "password": password
        }
        response = requests.post(LOGIN_COURIER_URL, json=payload)
        response_json = response.json()
        assert response.status_code == 200 and "id" in response_json

    @pytest.mark.parametrize("payload, expected_status, expected_message", [
        ({"login": "ninja", "password": ""}, 400, "Недостаточно данных для входа"),
        ({"login": "", "password": "1234"}, 400, "Недостаточно данных для входа")
    ])
    @allure.title("Тест на логин с отсутствующими обязательными полями")
    @allure.description("Проверяем, что при отсутствии обязательных полей для логина возвращается ошибка")
    def test_login_missing_required_fields(self, payload, expected_status, expected_message):
        response = requests.post(LOGIN_COURIER_URL, json=payload)
        response_json = response.json()
        assert response.status_code == expected_status and response_json['message'] == expected_message

    @pytest.mark.parametrize("login, password, expected_status, expected_message", [
        ("valid_login", "wrong_password", 404, "Учетная запись не найдена"),
        ("invalid_login", "valid_password", 404, "Учетная запись не найдена")
    ])
    @allure.title("Тест на логин с некорректными учетными данными")
    @allure.description("Проверяем, что при вводе некорректных учетных данных возвращается ошибка")
    def test_login_with_invalid_credentials(self, create_and_register_courier, login, password, expected_status,
                                            expected_message):
        valid_login = create_and_register_courier["login"]
        valid_password = create_and_register_courier["password"]

        payload = {
            "login": valid_login if login == "valid_login" else login,
            "password": valid_password if password == "valid_password" else password
        }
        response = requests.post(LOGIN_COURIER_URL, json=payload)
        response_json = response.json()
        assert response.status_code == expected_status and response_json.get('message')
