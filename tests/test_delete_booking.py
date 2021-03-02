"""Модуль с тестами delete запросов - DeleteBooking."""

import pytest
import requests
import allure  # type: ignore
import conftest
from helpers import body_id_data, allure_steps  # type: ignore


@allure.feature("DELETE - DeleteBooking")
@allure.story("Удаление существующей сущности по id")
@pytest.mark.positive
def test_delete_by_id_positive(booker_api: conftest.ApiClient) -> None:
    """Тестовая функция для проверки вызова delete запроса.
    Проверяются позитивные варианты через параметризацию - существующие id.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    """
    id_to_do_request: str = body_id_data.create_test_entity(booker_api)

    with allure.step(allure_steps.send_delete_request(id_to_do_request)):
        response: requests.models.Response = \
            booker_api.delete(path=id_to_do_request)

    with allure.step(allure_steps.check_201_status_code()):
        assert response.status_code == 201, f"Код ответа - {response.status_code}"


@allure.feature("DELETE - DeleteBooking")
@allure.story("Удаление несуществующей сущности по id")
@pytest.mark.negative
@pytest.mark.parametrize("param", ["abc", "123112"])
def test_delete_by_id_negative(booker_api: conftest.ApiClient,
                               param: str) -> None:
    """Тестовая функция для проверки вызова delete запроса.
    Проверяются негативные варианты через параметризацию
    - несуществующие id.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param param: передаваемый в урле id
    """
    with allure.step(allure_steps.send_delete_request(param)):
        response: requests.models.Response = booker_api.delete(path=param)

    with allure.step(allure_steps.check_405_status_code()):
        assert response.status_code == 405, f"Код ответа - {response.status_code}"
