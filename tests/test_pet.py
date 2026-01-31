import allure
import jsonschema
import requests
from .schemas.pet_schema import PET_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet deleted", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }
            response = requests.put(url=f"{BASE_URL}/pet/", json=payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 10,
                "name": "doggie",
                "status": "available"
            }

        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet/", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и вадидации JSON-схемы"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id'] == payload['id'], "Id питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "Имя питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "Статус питомца не совпадает с ожидаемым"

    @allure.title("Добавление нового питомца - test case #41")
    def test_add_pet(self):
        with allure.step("Подготовка данных для создания питомца - test case #41"):
            payload = {
                "id": 10,
                "name": "doggie",
                "status": "available",
                "category": {"id": 1,
                             "name": "Dogs"},
                "photoUrls": ["string"],
                "tags": [{"id": 0,
                          "name": "string"}]
            }

        with allure.step("Отправка запроса на создание питомца - test case #41"):
            response = requests.post(url=f"{BASE_URL}/pet/", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и вадидации JSON-схемы - test case #41"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе - test case #41"):
            assert response_json['id'] == payload['id'], "Id питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "Имя питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "Статус питомца не совпадает с ожидаемым"
            assert response_json['category'] == payload['category'], "Категория питомца не совпадает с ожидаемым"
            assert response_json['photoUrls'] == payload['photoUrls'], "PhotoUrls питомца не совпадает с ожидаемым"
            assert response_json['tags'] == payload['tags'], "Tags питомца не совпадает с ожидаемым"