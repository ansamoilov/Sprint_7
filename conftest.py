import pytest
import requests

from api_testing.methods.courier_methods import CourierMethods
from api_testing.data import CREATE_COURIER_URL, DELETE_COURIER_URL, LOGIN_COURIER_URL, CREATE_ORDER_URL, \
    GET_ORDER_TRACK_URL, ACCEPT_ORDER_URL
from api_testing.methods.order_methods import generate_order_payload


@pytest.fixture
def create_order_data():
    return generate_order_payload()


@pytest.fixture(scope='function')
def create_and_register_courier():
    courier_methods = CourierMethods()
    login, password, first_name = courier_methods.create_new_courier_credentials()
    response = requests.post(CREATE_COURIER_URL, json={
        "login": login,
        "password": password,
        "firstName": first_name
    })
    assert response.status_code == 201

    yield {
        "login": login,
        "password": password,
        "firstName": first_name,
    }

    login_response = requests.post(LOGIN_COURIER_URL, json={
        "login": login,
        "password": password
    })
    assert login_response.status_code == 200
    courier_id = login_response.json().get("id")
    assert courier_id is not None
    delete_courier_url = f'{DELETE_COURIER_URL}{courier_id}'
    delete_response = requests.delete(delete_courier_url, json={"id": courier_id})
    assert delete_response.status_code == 200


@pytest.fixture(scope='function')
def create_courier_and_order(create_order_data):
    courier_methods = CourierMethods()
    login, password, first_name = courier_methods.create_new_courier_credentials()
    response = requests.post(CREATE_COURIER_URL, json={
        "login": login,
        "password": password,
        "firstName": first_name
    })
    assert response.status_code == 201
    order_data = create_order_data
    response = requests.post(CREATE_ORDER_URL, json=order_data)
    assert response.status_code == 201
    track_id = response.json().get("track")
    response = requests.get(f"{GET_ORDER_TRACK_URL}?t={track_id}")
    assert response.status_code == 200
    order_info = response.json()
    order_id = order_info.get("order", {}).get("id")
    login_response = requests.post(LOGIN_COURIER_URL, json={
        "login": login,
        "password": password
    })
    assert login_response.status_code == 200
    courier_id = login_response.json().get("id")
    assert courier_id is not None
    nearest_station = order_data.get("metroStation")
    accept_response = requests.put(f"{ACCEPT_ORDER_URL}/{order_id}?courierId={courier_id}")
    assert accept_response.status_code == 200

    yield {
        "courier_id": courier_id,
        "order_id": order_id,
        "nearestStation": nearest_station,
    }

    delete_courier_url = f'{DELETE_COURIER_URL}{courier_id}'
    delete_response = requests.delete(delete_courier_url, json={"id": courier_id})
    assert delete_response.status_code == 200
    #здесь нет удаления заказа, потому что нет такой ручки
