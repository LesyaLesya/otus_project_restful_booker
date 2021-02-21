""" Модуль с тестами put запросов - UpdateBooking """


from typing import Dict, Any
import json
import pytest
import requests
import allure   # type: ignore
import conftest
import helpers


@allure.feature("PUT - UpdateBooking")
@allure.story("Обновление всех параметров сущности")
@pytest.mark.all_tests
@pytest.mark.positive
def test_put_all_fields(booker_api: conftest.ApiClient) -> None:
    """
    Тестовая функция для проверки вызова put запроса с передаваемым телом.
    Проверяется обновление всех значений.
    Обращение напрямую к определенному id в урле.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient

    """
    data: Dict[str, Any] = helpers.return_dict()

    with allure.step(f"Отправляем put запрос с телом - {data}"):
        response: requests.models.Response =\
            booker_api.put(path="7", data=json.dumps(data))

    with allure.step("Проверяем, что код ответа 200"):
        assert response.status_code == 200, f"Код ответа - {response.status_code}"

    with allure.step(f"Проверяем, что firstname - '{data['firstname']}'"):
        assert response.json()["firstname"] == data['firstname'], \
            f"Имя - '{response.json()['firstname']}'"

    with allure.step(f"Проверяем, что lastname - '{data['lastname']}'"):
        assert response.json()["lastname"] == data['lastname'], \
            f"Фамилия - '{response.json()['lastname']}'"

    with allure.step(f"Проверяем, что totalprice - '{data['totalprice']}'"):
        assert response.json()["totalprice"] == data['totalprice'], \
            f"Итоговая цена - '{response.json()['totalprice']}'"

    with allure.step(f"Проверяем, что depositpaid - '{data['depositpaid']}'"):
        assert response.json()["depositpaid"] == data['depositpaid'], \
            f"Депозит - '{response.json()['depositpaid']}'"

    with allure.step(f"Проверяем, что checkin - '{data['bookingdates']['checkin']}'"):
        assert response.json()["bookingdates"]["checkin"] ==\
               data['bookingdates']['checkin'], \
               f"Дата заезда - '{response.json()['bookingdates']['checkin']}'"

    with allure.step(f"Проверяем, что checkout - '{data['bookingdates']['checkout']}'"):
        assert response.json()["bookingdates"]["checkout"] == \
               data['bookingdates']['checkout'], \
               f"Дата выезда - '{response.json()['bookingdates']['checkout']}'"

    with allure.step(f"Проверяем, что additionalneeds - '{data['additionalneeds']}'"):
        assert response.json()["additionalneeds"] == \
               data['additionalneeds'], \
               f"Депозит - '{response.json()['additionalneeds']}'"


@allure.feature("PUT - UpdateBooking")
@allure.story("Обновление части параметров сущности")
@pytest.mark.all_tests
@pytest.mark.negative
@pytest.mark.parametrize("data", [{"firstname": "John", "lastname": "Smith"}, {}])
def test_put_not_all_fields(booker_api: conftest.ApiClient,
                            data: Dict[str, str]) -> None:
    """
    Тестовая функция для проверки вызова put запроса с передаваемым телом.
    Негативная проверка передачи в теле части значений / пустого тела.
    Обращение напрямую к определенному id в урле.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param data: передаваемое тело запроса

    """
    with allure.step(f"Отправляем put запрос с телом - {data}"):
        response: requests.models.Response =\
            booker_api.put(path="5", data=json.dumps(data))

    with allure.step("Проверяем, что код ответа 400"):
        assert response.status_code == 400, f"Код ответа - {response.status_code}"


@allure.feature("PUT - UpdateBooking")
@allure.story("Обновление параметров несуществующей сущности")
@pytest.mark.all_tests
@pytest.mark.negative
@pytest.mark.parametrize("param", ["321342", "&*&^(&", "0"])
def test_put_invalid_id(booker_api: conftest.ApiClient,
                        param: str) -> None:
    """
    Тестовая функция для проверки вызова put запроса с передаваемым телом.
    Негативная проверка обращение к несуществующему урлу.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param param: передаваемый в урле id

    """
    data: Dict[str, Any] = helpers.return_dict()

    with allure.step(f"Отправляем put запрос с id {param}"):
        response: requests.models.Response =\
            booker_api.put(path=param, data=json.dumps(data))

    with allure.step("Проверяем, что код ответа 405"):
        assert response.status_code == 405, f"Код ответа - {response.status_code}"
