"""Модуль с тестами post запросов - CreateBooking."""

from typing import Union, Dict, Any
import json
import pytest
import requests
import allure   # type: ignore
import conftest
from helpers import allure_steps, body_id_data


@allure.feature("POST - CreateBooking")
@allure.story("Создание сущности - позитивная проверка 'firstname'")
@pytest.mark.positive
@pytest.mark.parametrize("param", ["Susan", "Maria-Elena", "Имя Имя", ""])
def test_post_firstname_positive(booker_api: conftest.ApiClient,
                                 param: str) -> None:
    """Тестовая функция для проверки вызова post запроса.
    Проверяются позитивные варианты для "firstname" через параметризацию.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param param: передаваемые в теле запроса варианты для "firstname"
    """

    data: Dict[str, Any] = body_id_data.return_dict_with_firstname(param)

    with allure.step(f"Отправляем post запрос с firstname - '{param}'"):
        response: requests.models.Response = booker_api.post(data=json.dumps(data))

    with allure.step(allure_steps.check_200_status_code()):
        assert response.status_code == 200, f"Код ответа - {response.status_code}"

    with allure.step(f"Проверяем, что firstname - '{param}'"):
        assert response.json()["booking"]["firstname"] == param, \
            f"Имя -  '{response.json()['booking']['firstname']}'"


@allure.feature("POST - CreateBooking")
@allure.story("Создание сущности - негативная проверка 'firstname'")
@pytest.mark.negative
@pytest.mark.parametrize("param", [123, True])
def test_post_firstname_negative(booker_api: conftest.ApiClient,
                                 param: Union[int, bool]) -> None:
    """Тестовая функция для проверки вызова post запроса.
    Проверяются негативные варианты для "firstname" через параметризацию -
    число, булево значение.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param param: передаваемые в теле запроса варианты для "firstname"
    """
    data: Dict[str, Any] = body_id_data.return_dict_with_firstname(param)

    with allure.step(f"Отправляем post запрос с firstname - '{param}'"):
        response: requests.models.Response = booker_api.post(data=json.dumps(data))

    with allure.step(allure_steps.check_500_status_code()):
        assert response.status_code == 500, f"Код ответа - {response.status_code}"


@allure.feature("POST - CreateBooking")
@allure.story("Создание сущности - проверка 'lastname'")
@pytest.mark.positive
@pytest.mark.parametrize("param", ["Иванов", "Brown", "W", "Last-name", ""])
def test_post_lastname(booker_api: conftest.ApiClient,
                       param: str) -> None:
    """Тестовая функция для проверки вызова post запроса.
    Проверяются позитивные варианты для "lastname" через параметризацию.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param param: передаваемые в теле запроса варианты для "lastname"
    """
    data: Dict[str, Any] = body_id_data.return_dict_with_lastname(param)

    with allure.step(f"Отправляем post запрос с lastname - '{param}'"):
        response: requests.models.Response = booker_api.post(data=json.dumps(data))

    with allure.step(allure_steps.check_200_status_code()):
        assert response.status_code == 200, f"Код ответа - {response.status_code}"

    with allure.step(f"Проверяем, что lastname - '{param}'"):
        assert response.json()["booking"]["lastname"] == param, \
            f"Фамилия - '{response.json()['booking']['lastname']}'"


@allure.feature("POST - CreateBooking")
@allure.story("Создание сущности - проверка 'totalprice'")
@pytest.mark.positive
@pytest.mark.parametrize("param", [123, 1, 566778])
def test_post_totalprice(booker_api: conftest.ApiClient,
                         param: int) -> None:
    """Тестовая функция для проверки вызова post запроса.
    Проверяются позитивные варианты для "totalprice" через параметризацию.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param param: передаваемые в теле запроса варианты для "totalprice"
    """
    data: Dict[str, Any] = body_id_data.return_dict_with_totalprice(param)

    with allure.step(f"Отправляем post запрос с totalprice - '{param}'"):
        response: requests.models.Response = booker_api.post(data=json.dumps(data))

    with allure.step(allure_steps.check_200_status_code()):
        assert response.status_code == 200, f"Код ответа - {response.status_code}"

    with allure.step(f"Проверяем, что totalprice - '{param}'"):
        assert response.json()["booking"]["totalprice"] == param, \
            f"Общая сумма - '{response.json()['booking']['totalprice']}'"


@allure.feature("POST - CreateBooking")
@allure.story("Создание сущности - проверка 'depositpaid'")
@pytest.mark.positive
@pytest.mark.parametrize("param", [True, False])
def test_post_depositpaid(booker_api: conftest.ApiClient,
                          param: bool) -> None:
    """Тестовая функция для проверки вызова post запроса.
    Проверяются позитивные варианты для "depositpaid" через параметризацию.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param param: передаваемые в теле запроса варианты для "depositpaid"
    """
    data: Dict[str, Any] = body_id_data.return_dict_with_depositpaid(param)

    with allure.step(f"Отправляем post запрос с depositpaid - '{param}'"):
        response: requests.models.Response = booker_api.post(data=json.dumps(data))

    with allure.step(allure_steps.check_200_status_code()):
        assert response.status_code == 200, f"Код ответа - {response.status_code}"

    with allure.step(f"Проверяем, что depositpaid - '{param}'"):
        assert response.json()["booking"]["depositpaid"] == param, \
            f"Статус внесения депозита - '{response.json()['booking']['depositpaid']}'"


@allure.feature("POST - CreateBooking")
@allure.story("Создание сущности - позитивная проверка 'checkin'")
@pytest.mark.positive
@pytest.mark.parametrize("param", ["1900-11-11", "2021-02-11", "2030-06-01"])
def test_post_checkin_positive(booker_api: conftest.ApiClient,
                               param: str) -> None:
    """Тестовая функция для проверки вызова post запроса.
    Проверяются позитивные варианты для "checkin" через параметризацию.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param param: передаваемые в теле запроса варианты для "checkin"
    """
    data: Dict[str, Any] = body_id_data.return_dict_with_chekin(param)

    with allure.step(f"Отправляем post запрос с checkin - '{param}'"):
        response: requests.models.Response = booker_api.post(data=json.dumps(data))

    with allure.step(allure_steps.check_200_status_code()):
        assert response.status_code == 200, f"Код ответа - {response.status_code}"

    with allure.step(f"Проверяем, что checkin - '{param}'"):
        assert response.json()["booking"]["bookingdates"]["checkin"] == param, \
            f"Дата заезда - '{response.json()['booking']['bookingdates']['checkin']}'"


@allure.feature("POST - CreateBooking")
@allure.story("Создание сущности - негативная проверка 'checkin'")
@pytest.mark.negative
@pytest.mark.parametrize("param", ["00-00-00", "tests", " "])
def test_post_checkin_negative(booker_api: conftest.ApiClient,
                               param: str) -> None:
    """Тестовая функция для проверки вызова post запроса.
    Проверяются негативные варианты для "checkin" через параметризацию -
    неправильный формат даты / не дата.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param param: передаваемые в теле запроса варианты для "checkin"
    """
    data: Dict[str, Any] = body_id_data.return_dict_with_chekin(param)

    with allure.step(f"Отправляем post запрос с checkin - '{param}'"):
        response: requests.models.Response = booker_api.post(data=json.dumps(data))

    with allure.step(allure_steps.check_200_status_code()):
        assert response.status_code == 200, f"Код ответа - {response.status_code}"

    with allure.step("Проверяем, что текст ответа - Invalid date"):
        assert response.text == "Invalid date", f"Текст ответа - '{response.text}'"


@allure.feature("POST - CreateBooking")
@allure.story("Создание сущности - позитивная проверка 'checkout'")
@pytest.mark.positive
@pytest.mark.parametrize("param", ["1871-01-01", "2021-02-11", "2041-12-31"])
def test_post_checkout(booker_api: conftest.ApiClient,
                       param: str) -> None:
    """Тестовая функция для проверки вызова post запроса.
    Проверяются позитивные варианты для "checkout" через параметризацию.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param param: передаваемые в теле запроса варианты для "checkout"
    """
    data: Dict[str, Any] = body_id_data.return_dict_with_chekout(param)

    with allure.step(f"Отправляем post запрос с checkout - '{param}'"):
        response: requests.models.Response = booker_api.post(data=json.dumps(data))

    with allure.step(allure_steps.check_200_status_code()):
        assert response.status_code == 200, f"Код ответа - {response.status_code}"

    with allure.step(f"Проверяем, что checkout - '{param}'"):
        assert response.json()["booking"]["bookingdates"]["checkout"] == param, \
            f"Дата выезда - '{response.json()['booking']['bookingdates']['checkout']}'"


@allure.feature("POST - CreateBooking")
@allure.story("Создание сущности - проверка 'additionalneeds'")
@pytest.mark.positive
@pytest.mark.parametrize("param", ["что-то", "dinner, breakfast", ""])
def test_post_additionalneeds(booker_api: conftest.ApiClient,
                              param: str) -> None:
    """Тестовая функция для проверки вызова post запроса.
    Проверяются позитивные варианты для "additionalneeds" через параметризацию.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param param: передаваемые в теле запроса варианты для "additionalneeds"
    """
    data: Dict[str, Any] = body_id_data.return_dict_with_addneeds(param)

    with allure.step(f"Отправляем post запрос с additionalneeds - '{param}'"):
        response: requests.models.Response = booker_api.post(data=json.dumps(data))

    with allure.step(allure_steps.check_200_status_code()):
        assert response.status_code == 200, f"Код ответа - {response.status_code}"

    with allure.step(f"Проверяем, что additionalneeds - '{param}'"):
        assert response.json()["booking"]["additionalneeds"] == param, \
            f"Дополнительные пожелания - '{response.json()['booking']['additionalneeds']}'"


@allure.feature("POST - CreateBooking")
@allure.story("Создание сущности с пустым телом запроса")
@pytest.mark.negative
def test_post_empty_body(booker_api: conftest.ApiClient) -> None:
    """Тестовая функция для проверки вызова post запроса.
    Проверяется передача пустого тела запроса.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    """

    with allure.step("Отправляем post запрос с пустым телом запроса"):
        response: requests.models.Response = booker_api.post(data={})

    with allure.step(allure_steps.check_500_status_code()):
        assert response.status_code == 500, f"Код ответа - {response.status_code}"
