"""Модуль с тестами patch запросов - PartialUpdateBooking."""

from typing import Dict, Any
import json
import pytest
import requests
import allure   # type: ignore
import conftest
from helpers import body_id_data, allure_steps  # type: ignore


@allure.feature("PATCH - PartialUpdateBooking")
@allure.story("Обновление части параметров сущности")
@pytest.mark.positive
@pytest.mark.parametrize("param, first, last", [(0, "Peter", "Jackson"), (1, "Emma", "Star")])
def test_patch_part_fields(booker_api: conftest.ApiClient,
                           param: int, first: str, last: str) -> None:
    """Тестовая функция для проверки вызова patch запроса с передаваемым телом.
    Проверяются позитивные варианты через параметризацию -
    обновление значений "firstname", "lastname".
    Обращение напрямую к определенному id в урле.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param first: передаваемый в теле запроса firstname
    :param last: передаваемый в теле запроса lastname
    :param param: передаваемые индексы сущностей для определения их id
    """
    with allure.step(allure_steps.get_id_with_param(param)):
        id_to_do_request: str = body_id_data.get_id_of_entity(booker_api, param)

    with allure.step(f"Получаем все данные по id {id_to_do_request}"):
        get_request: requests.models.Response = booker_api.get(path=id_to_do_request)
        data_for_id: Dict[str, Any] = get_request.json()

    data: Dict[str, str] = {"firstname": "Peter", "lastname": last}

    with allure.step(allure_steps.send_patch_request(data, id_to_do_request)):
        response: requests.models.Response =\
            booker_api.patch(path=id_to_do_request, data=json.dumps(data))

    with allure.step(allure_steps.check_200_status_code()):
        assert response.status_code == 200, f"Код ответа - {response.status_code}"

    with allure.step(allure_steps.check_firstname(first)):
        assert response.json()["firstname"] == first, \
            f"Имя - '{response.json()['firstname']}'"

    with allure.step(allure_steps.check_lastname(last)):
        assert response.json()["lastname"] == last, \
            f"Фамилия - '{response.json()['lastname']}'"

    with allure.step(allure_steps.check_totalprice(data_for_id['totalprice'])):
        assert response.json()["totalprice"] == data_for_id["totalprice"], \
            f"Итоговая цена - '{response.json()['totalprice']}'"

    with allure.step(allure_steps.check_depositpaid(data_for_id['depositpaid'])):
        assert response.json()["depositpaid"] == data_for_id["depositpaid"], \
            f"Депозит - '{response.json()['depositpaid']}'"

    with allure.step(allure_steps.check_checkin(data_for_id['bookingdates']['checkin'])):
        assert response.json()["bookingdates"]["checkin"] == \
            data_for_id["bookingdates"]["checkin"], \
            f"Дата заезда - '{response.json()['bookingdates']['checkin']}'"

    with allure.step(allure_steps.check_checkout(data_for_id['bookingdates']['checkout'])):
        assert response.json()["bookingdates"]["checkout"] == \
            data_for_id["bookingdates"]["checkout"], \
            f"Дата выезда - '{response.json()['bookingdates']['checkout']}'"


@allure.feature("PATCH - PartialUpdateBooking")
@allure.story("Обновление всех параметров сущности")
@pytest.mark.positive
def test_patch_all_fields(booker_api: conftest.ApiClient) -> None:
    """Тестовая функция для проверки вызова patch запроса с передаваемым телом.
    Проверяется обновление всех полей сущности.
    Обращение напрямую к определенному id в урле.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    """
    data: Dict[str, Any] = body_id_data.return_dict()

    with allure.step(allure_steps.get_id()):
        id_to_do_request: str = body_id_data.get_id_of_entity(booker_api, -1)

    with allure.step(allure_steps.send_patch_request(data, id_to_do_request)):
        response: requests.models.Response = \
            booker_api.patch(path=id_to_do_request, data=json.dumps(data))

    with allure.step(allure_steps.check_200_status_code()):
        assert response.status_code == 200, f"Код ответа - {response.status_code}"

    with allure.step(allure_steps.check_firstname(data['firstname'])):
        assert response.json()["firstname"] == data['firstname'], \
            f"Имя - '{response.json()['firstname']}'"

    with allure.step(allure_steps.check_lastname(data['lastname'])):
        assert response.json()["lastname"] == data['lastname'], \
            f"Фамилия - '{response.json()['lastname']}'"

    with allure.step(allure_steps.check_totalprice(data['totalprice'])):
        assert response.json()["totalprice"] == data['totalprice'], \
            f"Итоговая цена - '{response.json()['totalprice']}'"

    with allure.step(allure_steps.check_depositpaid(data['depositpaid'])):
        assert response.json()["depositpaid"] == data['depositpaid'], \
            f"Депозит - '{response.json()['depositpaid']}'"

    with allure.step(allure_steps.check_checkin(data['bookingdates']['checkin'])):
        assert response.json()["bookingdates"]["checkin"] == \
               data['bookingdates']['checkin'], \
               f"Дата заезда - '{response.json()['bookingdates']['checkin']}'"

    with allure.step(allure_steps.check_checkout(data['bookingdates']['checkout'])):
        assert response.json()["bookingdates"]["checkout"] == \
               data['bookingdates']['checkout'], \
               f"Дата выезда - '{response.json()['bookingdates']['checkout']}'"

    with allure.step(allure_steps.check_addneeds(data['additionalneeds'])):
        assert response.json()["additionalneeds"] == data['additionalneeds'], \
               f"Пожелания - '{response.json()['additionalneeds']}'"


@allure.feature("PATCH - PartialUpdateBooking")
@allure.story("Обновление сущности передачей пустого тела")
@pytest.mark.positive
@pytest.mark.parametrize("param", [-1, 1])
def test_patch_empty_body(booker_api: conftest.ApiClient,
                          param: int) -> None:
    """Тестовая функция для проверки вызова patch запроса с передаваемым телом.
    Проверяется передача пустого тела.
    Обращение напрямую к определенному id в урле.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param param: передаваемые индексы сущностей для определения их id
    """
    with allure.step(allure_steps.get_id_with_param(param)):
        id_to_do_request: str = body_id_data.get_id_of_entity(booker_api, param)

    with allure.step(f"Получаем все данные по id {id_to_do_request}"):
        get_request: requests.models.Response = booker_api.get(path=id_to_do_request)
        data_for_id: Dict[str, Any] = get_request.json()

    with allure.step(f"Отправляем patch запрос с пустым телом и id {id_to_do_request}"):
        response: requests.models.Response = booker_api.patch(path=id_to_do_request, data={})

    with allure.step(allure_steps.check_200_status_code()):
        assert response.status_code == 200, f"Код ответа - {response.status_code}"

    with allure.step(allure_steps.check_firstname(data_for_id['firstname'])):
        assert response.json()["firstname"] == data_for_id["firstname"], \
            f"Имя - '{response.json()['firstname']}'"

    with allure.step(allure_steps.check_lastname(data_for_id['lastname'])):
        assert response.json()["lastname"] == data_for_id["lastname"], \
            f"Фамилия - '{response.json()['lastname']}'"

    with allure.step(allure_steps.check_totalprice(data_for_id['totalprice'])):
        assert response.json()["totalprice"] == data_for_id["totalprice"], \
            f"Итоговая цена - '{response.json()['totalprice']}'"

    with allure.step(allure_steps.check_depositpaid(data_for_id['depositpaid'])):
        assert response.json()["depositpaid"] == data_for_id["depositpaid"], \
            f"Депозит - '{response.json()['depositpaid']}'"

    with allure.step(allure_steps.check_checkin(data_for_id['bookingdates']['checkin'])):
        assert response.json()["bookingdates"]["checkin"] == \
            data_for_id["bookingdates"]["checkin"], \
            f"Дата заезда - '{response.json()['bookingdates']['checkin']}'"

    with allure.step(allure_steps.check_checkout(data_for_id['bookingdates']['checkout'])):
        assert response.json()["bookingdates"]["checkout"] == \
            data_for_id["bookingdates"]["checkout"], \
            f"Дата выезда - '{response.json()['bookingdates']['checkout']}'"


@allure.feature("PATCH - PartialUpdateBooking")
@allure.story("Обновление параметров несуществующей сущности")
@pytest.mark.negative
@pytest.mark.parametrize("param", ["213123", "tests"])
def test_patch_invalid_id(booker_api: conftest.ApiClient,
                          param: str) -> None:
    """Тестовая функция для проверки вызова patch запроса с передаваемым телом.
    Проверяются негативные варианты через параметризацию -
    обращение к несуществующему id в урле.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param param: передеваемый в урле id
    """
    data: Dict[str, Any] = body_id_data.return_dict()

    with allure.step(f"Отправляем patch запрос с id {param}"):
        response: requests.models.Response =\
            booker_api.patch(path=param, data=json.dumps(data))

    with allure.step(allure_steps.check_405_status_code()):
        assert response.status_code == 405, f"Код ответа - {response.status_code}"
