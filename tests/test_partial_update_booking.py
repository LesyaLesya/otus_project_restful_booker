""" Модуль с тестами patch запросов - PartialUpdateBooking. """


from typing import Dict, Any
import json
import pytest
import requests
import allure   # type: ignore
import conftest
import helpers


@allure.feature("PATCH - PartialUpdateBooking")
@allure.story("Обновление части параметров сущности")
@pytest.mark.all_tests
@pytest.mark.positive
@pytest.mark.parametrize("book_id, first, last", [("8", "Peter", "Jackson"), ("9", "Emma", "Star")])
def test_patch_part_fields(booker_api: conftest.ApiClient,
                           book_id: str, first: str, last: str) -> None:
    """
    Тестовая функция для проверки вызова patch запроса с передаваемым телом.
    Проверяются позитивные варианты через параметризацию -
    обновление значений "firstname", "lastname".
    Обращение напрямую к определенному id в урле.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param first: передаваемый в теле запроса firstname
    :param last: передаваемый в теле запроса lastname
    :param book_id: передаваемый id

    """
    with allure.step(f"Получаем все данные по id {book_id}"):
        get_request: requests.models.Response = booker_api.get(path=book_id)
        data_for_id: Dict[str, Any] = get_request.json()

    data: Dict[str, str] = {"firstname": first, "lastname": last}

    with allure.step(f"Отправляем patch запрос с data - {data}"):
        response: requests.models.Response =\
            booker_api.patch(path=book_id, data=json.dumps(data))

    with allure.step("Проверяем, что код ответа 200"):
        assert response.status_code == 200, f"Код ответа - {response.status_code}"

    with allure.step(f"Проверяем, что firstname - '{first}'"):
        assert response.json()["firstname"] == first, \
            f"Имя - '{response.json()['firstname']}'"

    with allure.step(f"Проверяем, что lastname - '{last}'"):
        assert response.json()["lastname"] == last, \
            f"Фамилия - '{response.json()['lastname']}'"

    with allure.step(f"Проверяем, что totalprice - '{data_for_id['totalprice']}'"):
        assert response.json()["totalprice"] == data_for_id["totalprice"], \
            f"Итоговая цена - '{response.json()['totalprice']}'"

    with allure.step(f"Проверяем, что depositpaid - '{data_for_id['depositpaid']}'"):
        assert response.json()["depositpaid"] == data_for_id["depositpaid"], \
            f"Депозит - '{response.json()['depositpaid']}'"

    with allure.step(f"Проверяем, что checkin - '{data_for_id['bookingdates']['checkin']}'"):
        assert response.json()["bookingdates"]["checkin"] == \
            data_for_id["bookingdates"]["checkin"], \
            f"Дата заезда - '{response.json()['bookingdates']['checkin']}'"

    with allure.step(f"Проверяем, что checkout - '{data_for_id['bookingdates']['checkout']}'"):
        assert response.json()["bookingdates"]["checkout"] == \
            data_for_id["bookingdates"]["checkout"], \
            f"Дата выезда - '{response.json()['bookingdates']['checkout']}'"


@allure.feature("PATCH - PartialUpdateBooking")
@allure.story("Обновление всех параметров сущности")
@pytest.mark.all_tests
@pytest.mark.positive
def test_patch_all_fields(booker_api: conftest.ApiClient) -> None:
    """
    Тестовая функция для проверки вызова patch запроса с передаваемым телом.
    Проверяется обновление всех полей сущности.
    Обращение напрямую к определенному id в урле.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient

    """
    data: Dict[str, Any] = helpers.return_dict()

    with allure.step(f"Отправляем patch запрос с data - {data}"):
        response: requests.models.Response = \
            booker_api.patch(path="5", data=json.dumps(data))

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
        assert response.json()["bookingdates"]["checkin"] == \
               data['bookingdates']['checkin'], \
               f"Дата заезда - '{response.json()['bookingdates']['checkin']}'"

    with allure.step(f"Проверяем, что checkout - '{data['bookingdates']['checkout']}'"):
        assert response.json()["bookingdates"]["checkout"] == \
               data['bookingdates']['checkout'], \
               f"Дата выезда - '{response.json()['bookingdates']['checkout']}'"

    with allure.step(f"Проверяем, что additionalneeds - '{data['additionalneeds']}'"):
        assert response.json()["additionalneeds"] == data['additionalneeds'], \
               f"Пожелания - '{response.json()['additionalneeds']}'"


@allure.feature("PATCH - PartialUpdateBooking")
@allure.story("Обновление сущности передачей пустого тела")
@pytest.mark.all_tests
@pytest.mark.positive
@pytest.mark.parametrize("book_id", ["5", "26"])
def test_patch_empty_body(booker_api: conftest.ApiClient,
                          book_id: str) -> None:
    """
    Тестовая функция для проверки вызова patch запроса с передаваемым телом.
    Проверяется передача пустого тела.
    Обращение напрямую к определенному id в урле.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param book_id: передаваемый в урле id

    """
    with allure.step(f"Получаем все данные по id {book_id}"):
        get_request: requests.models.Response = booker_api.get(path=book_id)
        data_for_id: Dict[str, Any] = get_request.json()

    with allure.step("Отправляем patch запрос с пустым телом"):
        response: requests.models.Response = booker_api.patch(path=book_id, data={})

    with allure.step("Проверяем, что код ответа 200"):
        assert response.status_code == 200, f"Код ответа - {response.status_code}"

    with allure.step(f"Проверяем, что firstname - '{data_for_id['firstname']}'"):
        assert response.json()["firstname"] == data_for_id["firstname"], \
            f"Имя - '{response.json()['firstname']}'"

    with allure.step(f"Проверяем, что lastname - '{data_for_id['lastname']}'"):
        assert response.json()["lastname"] == data_for_id["lastname"], \
            f"Фамилия - '{response.json()['lastname']}'"

    with allure.step(f"Проверяем, что totalprice - '{data_for_id['totalprice']}'"):
        assert response.json()["totalprice"] == data_for_id["totalprice"], \
            f"Итоговая цена - '{response.json()['totalprice']}'"

    with allure.step(f"Проверяем, что depositpaid - '{data_for_id['depositpaid']}'"):
        assert response.json()["depositpaid"] == data_for_id["depositpaid"], \
            f"Депозит - '{response.json()['depositpaid']}'"

    with allure.step(f"Проверяем, что checkin - "
                     f"'{data_for_id['bookingdates']['checkin']}'"):
        assert response.json()["bookingdates"]["checkin"] == \
            data_for_id["bookingdates"]["checkin"], \
            f"Дата заезда - '{response.json()['bookingdates']['checkin']}'"

    with allure.step(f"Проверяем, что checkout - "
                     f"'{data_for_id['bookingdates']['checkout']}'"):
        assert response.json()["bookingdates"]["checkout"] == \
            data_for_id["bookingdates"]["checkout"], \
            f"Дата выезда - '{response.json()['bookingdates']['checkout']}'"


@allure.feature("PATCH - PartialUpdateBooking")
@allure.story("Обновление параметров несуществующей сущности")
@pytest.mark.all_tests
@pytest.mark.negative
@pytest.mark.parametrize("param", ["213123", "tests"])
def test_patch_invalid_id(booker_api: conftest.ApiClient,
                          param: str) -> None:
    """
    Тестовая функция для проверки вызова patch запроса с передаваемым телом.
    Проверяются негативные варианты через параметризацию -
    обращение к несуществующему id в урле.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param param: передеваемый в урле id

    """
    data: Dict[str, Any] = helpers.return_dict()

    with allure.step(f"Отправляем patch запрос с id {param}"):
        response: requests.models.Response =\
            booker_api.patch(path=param, data=json.dumps(data))

    with allure.step("Проверяем, что код ответа 405"):
        assert response.status_code == 405, f"Код ответа - {response.status_code}"
