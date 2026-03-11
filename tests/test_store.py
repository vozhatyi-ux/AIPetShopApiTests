import allure
import jsonschema
import requests
from tests.schemas.order_schema import ORDER_SCHEMA, INVENTORY_SCHEMA
#from tests.schemas.order_schema import INVENTORY_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Store")
class TestStore:
    @allure.title("Размещение заказа (POST /store/order)")
    def test_place_an_order_for_a_pet(self):
        with allure.step("Подготовка данных для размещения заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }

        with allure.step("Отправка запроса на размещение заказа"):
            response = requests.post(url=f"{BASE_URL}/store/order", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и вадидации JSON-схемы"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, ORDER_SCHEMA)

        with allure.step("Проверка параметров заказа в ответе"):
            assert response_json['id'] == payload['id'], "Id заказа не совпадает с ожидаемым"
            assert response_json['petId'] == payload['petId'], "Id питомца не совпадает с ожидаемым"
            assert response_json['quantity'] == payload['quantity'], "Количество заказа не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "Статус заказа не совпадает с ожидаемым"
            assert response_json['complete'] == payload['complete'], "Завершение заказа не совпадает с ожидаемым"

    @allure.title("Получение информации о заказе по ID (GET /store/order/{order_id})")
    def test_find_purchase_order_by_id(self, create_order):
        with allure.step("Получение ID созданного заказа"):
            order_id = create_order["id"]
            response = requests.get(url=f"{BASE_URL}/store/order/{order_id}")
            response_json = response.json()

        with allure.step("Проверка статуса ответа и Id ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response_json['id'] == order_id, "Id ответа не совпал с ожидаемым"

    @allure.title("Удаление заказа по ID (DELETE /store/order/{order_id})")
    def test_delete_purchase_order_by_id(self, create_order):
        with allure.step("Отправка запроса на удаление заказа по ID"):
            order_id = create_order["id"]
            response = requests.delete(url=f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка, что заказа больше не существует"):
            get_response = requests.get(url=f"{BASE_URL}/store/order/{order_id}")
            assert get_response.status_code == 404, "Код ответа не совпал с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем заказе (GET /store/order/{order_id})")
    def test_find_non_existent_purchase_order_by_id(self):
        with allure.step("Отправка запроса с несуществующим заказом"):
            order_id = 9999
            response = requests.get(url=f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа и формата данных"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

    @allure.title("Получение инвентаря магазина (GET /store/inventory)")
    def test_get_inventory(self):
        with allure.step("Отправка запроса на получение инвентаря"):
            response = requests.get(url=f"{BASE_URL}/store/inventory")
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидации формата ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, INVENTORY_SCHEMA)
