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
                "id": 1,
                "name": "Buddy",
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

    @allure.title("Добавление нового питомца Doggie с полными данными")
    def test_add_pet_Doggie_with_full_data(self): # Название теста отражает его суть
        with allure.step("Подготовка данных для создания питомца Doggie с полными данными"):
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

        with allure.step("Отправка запроса на создание питомца Doggie с полными данными"):
            response = requests.post(url=f"{BASE_URL}/pet/", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и вадидации JSON-схемы питомца Doggie с полными данными"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе Doggie с полными данными"):
            assert response_json['id'] == payload['id'], "Id питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "Имя питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "Статус питомца не совпадает с ожидаемым"
            assert response_json['category'] == payload['category'], "Категория питомца не совпадает с ожидаемым"
            assert response_json['photoUrls'] == payload['photoUrls'], "PhotoUrls питомца не совпадает с ожидаемым"
            assert response_json['tags'] == payload['tags'], "Tags питомца не совпадает с ожидаемым"

    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответаи и данных питомца"):
            assert response.status_code == 200
            assert response.json()["id"] == pet_id

    @allure.title("Обновление данных существующего питомца")
    def test_update_existing_pet(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Подготовка данных для обновления питомца"):
            updated_payload = {
                "id": pet_id,
                "name": "Buddy Updated",
                "status": "sold"
            }

        with allure.step("Отправка запроса на обновление питомца"):
            response = requests.put(url=f"{BASE_URL}/pet/", json=updated_payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка обновленных данных питомца"):
            assert response_json['id'] == pet_id, "ID питомца не совпадает"
            assert response_json['name'] == updated_payload['name'], "Имя питомца не обновилось"
            assert response_json['status'] == updated_payload['status'], "Статус питомца не обновился"

    @allure.title("Удаление существующего питомца")
    def test_delete_existing_pet(self, create_pet):
        with allure.step("Получение ID созданного питомца из фикстуры"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на удаление питомца"):
            delete_response = requests.delete(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа DELETE-запроса"):
            assert delete_response.status_code == 200, "Питомец не был удален"

        with allure.step("Отправка GET-запроса для проверки удаления"):
            get_response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа GET-запроса"):
            assert get_response.status_code == 404, "Питомец не удалился"


