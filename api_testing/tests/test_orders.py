import pytest
import requests
import allure
from api_testing.data import CREATE_ORDER_URL, GET_ORDERS_URL


class TestOrder:
    @pytest.mark.parametrize("color, expected_status", [
        (["BLACK"], 201),
        (["GREY"], 201),
        (["BLACK", "GREY"], 201),
        ([], 201)
    ])
    @allure.title("Тест на успешное создание заказа")
    @allure.description("Проверяем, что заказ успешно создается с различными цветами")
    def test_create_order_success(self, create_order_data, color, expected_status):
        create_order_data["color"] = color
        response = requests.post(CREATE_ORDER_URL, json=create_order_data)
        assert response.status_code == expected_status and "track" in response.json()

    @pytest.mark.parametrize("params, expected_status", [
        ({"courierId": 1}, 200),
        ({"courierId": 1, "nearestStation": 4}, 200),
        ({"limit": 10, "page": 0}, 200),
        ({"limit": 10, "page": 0, "nearestStation": [110]}, 200),
    ])
    @allure.title("Тест на получение списка заказов")
    @allure.description("Проверяем, что можем получить список заказов с различными параметрами")
    def test_get_orders_list(self, create_courier_and_order, params, expected_status):
        courier_id = create_courier_and_order["courier_id"]
        nearest_station = create_courier_and_order["nearestStation"]
        params["courierId"] = courier_id
        if "nearestStation" in params:
            params["nearestStation"] = nearest_station
        response = requests.get(GET_ORDERS_URL, params=params)
        assert response.status_code == expected_status
        response_data = response.json()
        assert "orders" in response_data
