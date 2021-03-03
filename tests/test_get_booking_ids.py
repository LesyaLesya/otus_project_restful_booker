"""Модуль с тестами get запросов - GetBookingIds."""

from typing import Dict
import pytest
import requests
import allure  # type: ignore
import conftest
from helpers import allure_steps, body_id_data  # type: ignore


@allure.feature("GET - GetBookingIds")
@allure.story("Получение списка всех сущностей")
@pytest.mark.positive
def test_get_all_bookings(booker_api: conftest.ApiClient) -> None:
    """Тестовая функция для проверки вызова get запроса.
    Проверяется получение всех сущностей.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    """
    with allure.step("Отправляем get запрос"):
        response: requests.models.Response = booker_api.get()

    with allure.step(allure_steps.check_200_status_code()):
        assert response.status_code == 200, f"Код ответа - {response.status_code}"

    with allure.step("Проверяем, что в ответе непустой список"):
        assert len(response.json()) != 0, "Нет ни одной сущности"


@allure.feature("GET - GetBookingIds")
@allure.story("Получение списка сущностей по существующему 'firstname'")
@pytest.mark.positive
@pytest.mark.parametrize("param", ["Anna", "Susan"])
def test_get_by_firstname_positive(booker_api: conftest.ApiClient,
                                   param: str) -> None:
    """Тестовая функция для проверки вызова get запроса с передаваемым в урле параметром.
    Проверяются позитивные варианты через параметризацию -
    для передачи параметра firstname в урле.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param param: передаваемый в урле параметр firstname
    """
    id_to_do_request = body_id_data.create_test_entity(booker_api)
    payload: Dict[str, str] = {"firstname": param}

    with allure.step(allure_steps.send_get_request_with_param(payload)):
        response: requests.models.Response = booker_api.get(params=payload)

    with allure.step(allure_steps.check_200_status_code()):
        assert response.status_code == 200, f"Код ответа - {response.status_code}"

    with allure.step(f"Проверяем, что у '{param}' есть бронь"):
        assert len(response.json()) != 0, f"У '{param}' нет брони"

    body_id_data.delete_test_entity(booker_api, id_to_do_request)


@allure.feature("GET - GetBookingIds")
@allure.story("Получение списка сущностей по несуществующему 'firstname'")
@pytest.mark.negative
@pytest.mark.parametrize("param", ["Тест", "13"])
def test_get_by_firstname_negative(booker_api: conftest.ApiClient,
                                   param: str) -> None:
    """Тестовая функция для проверки вызова get запроса с передаваемым в урле параметром.
    Проверяются негативные варианты через параметризацию -
    для передачи параметра firstname в урле -
    несуществующее имя.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param param: передаваемый в урле параметр firstname
    """
    payload: Dict[str, str] = {"firstname": param}

    with allure.step(allure_steps.send_get_request_with_param(payload)):
        response: requests.models.Response = booker_api.get(params=payload)

    with allure.step(allure_steps.check_200_status_code()):
        assert response.status_code == 200, f"Код ответа - {response.status_code}"

    with allure.step(f"Проверяем, что у '{param}' нет брони"):
        assert len(response.json()) == 0, f"У '{param}' есть бронь"


@allure.feature("GET - GetBookingIds")
@allure.story("Получение списка сущностей по существующему 'lastname'")
@pytest.mark.positive
@pytest.mark.parametrize("param", ["Chapman", "Brown"])
def test_get_by_lastname_positive(booker_api: conftest.ApiClient,
                                  param: str) -> None:
    """Тестовая функция для проверки вызова get запроса с передаваемым в урле параметром.
    Проверяются позитивные варианты через параметризацию -
    для передачи параметра lastname в урле.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param param: передаваемый в урле параметр lastname
    """
    id_to_do_request = body_id_data.create_test_entity(booker_api)
    payload: Dict[str, str] = {"lastname": param}

    with allure.step(allure_steps.send_get_request_with_param(payload)):
        response: requests.models.Response = booker_api.get(params=payload)

    with allure.step(allure_steps.check_200_status_code()):
        assert response.status_code == 200, f"Код ответа - {response.status_code}"

    with allure.step(f"Проверяем, что у '{param}' есть бронь"):
        assert len(response.json()) != 0, f"У '{param}' нет брони"

    body_id_data.delete_test_entity(booker_api, id_to_do_request)


@allure.feature("GET - GetBookingIds")
@allure.story("Получение списка сущностей по несуществующему 'lastname'")
@pytest.mark.negative
@pytest.mark.parametrize("param", ["0", "'$$@*:;"])
def test_get_by_lastname_negative(booker_api: conftest.ApiClient,
                                  param: str) -> None:
    """Тестовая функция для проверки вызова get запроса с передаваемым в урле параметром.
    Проверяются негативные варианты через параметризацию -
    для передачи параметра lastname в урле - несуществующая фамилия.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param param: передаваемый в урле параметр lastname
    """
    payload: Dict[str, str] = {"lastname": param}

    with allure.step(allure_steps.send_get_request_with_param(payload)):
        response: requests.models.Response = booker_api.get(params=payload)

    with allure.step(allure_steps.check_200_status_code()):
        assert response.status_code == 200, f"Код ответа - {response.status_code}"

    with allure.step(f"Проверяем, что у '{param}' нет брони"):
        assert len(response.json()) == 0, f"У '{param}' есть бронь"


@allure.feature("GET - GetBookingIds")
@allure.story("Получение списка сущностей по существующим 'firstname' и 'lastname'")
@pytest.mark.positive
@pytest.mark.parametrize("first, last", [("Anna", "Chapman"), ("Susan", "Brown")])
def test_get_by_fullname_positive(booker_api: conftest.ApiClient,
                                  first: str, last: str) -> None:
    """Тестовая функция для проверки вызова get запроса с передаваемым в урле 2 параметрами.
    Проверяются позитивные варианты через параметризацию -
    для передачи параметров firstname и lastname в урле.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param first: передаваемый в урле параметр firstname
    :param last: передаваемый в урле параметр lastname
    """
    id_to_do_request = body_id_data.create_test_entity(booker_api)
    payload: Dict[str, str] = {"firstname": first, "lastname": last}

    with allure.step(allure_steps.send_get_request_with_param(payload)):
        response: requests.models.Response = booker_api.get(params=payload)

    with allure.step(allure_steps.check_200_status_code()):
        assert response.status_code == 200, f"Код ответа - {response.status_code}"

    with allure.step(f"Проверяем, что у '{first} {last}' есть бронь"):
        assert len(response.json()) != 0, f"У '{first} {last}' нет брони"

    body_id_data.delete_test_entity(booker_api, id_to_do_request)


@allure.feature("GET - GetBookingIds")
@allure.story("Получение списка сущностей по несуществующим 'firstname' и 'lastname'")
@pytest.mark.negative
@pytest.mark.parametrize("first, last", [("Eric", "0"), ("Test", "Jones")])
def test_get_by_fullname_negative(booker_api: conftest.ApiClient,
                                  first: str, last: str) -> None:
    """Тестовая функция для проверки вызова get запроса с передаваемым в урле 2 параметрами.
    Проверяются негативные варианты через параметризацию -
    для передачи параметров firstname и lastname в урле -
    несуществующие сочетания имени и фамилиии.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param first: передаваемый в урле параметр firstname
    :param last: передаваемый в урле параметр lastname
    """
    payload: Dict[str, str] = {"firstname": first, "lastname": last}

    with allure.step(allure_steps.send_get_request_with_param(payload)):
        response: requests.models.Response = booker_api.get(params=payload)

    with allure.step(allure_steps.check_200_status_code()):
        assert response.status_code == 200, f"Код ответа - {response.status_code}"

    with allure.step(f"Проверяем, что у '{first} {last}' нет брони"):
        assert len(response.json()) == 0, f"У '{first} {last}' есть бронь"
