"""Модуль с тестами get запросов - GetBooking."""

import pytest
import requests
import allure  # type: ignore
import conftest
from helpers import body_id_data, allure_steps  # type: ignore


@allure.feature("GET - GetBooking")
@allure.story("Получение существующей сущности по id")
@pytest.mark.positive
@pytest.mark.parametrize("param", [1, 2, 0])
def test_get_by_id_positive(booker_api: conftest.ApiClient,
                            param: int) -> None:
    """Тестовая функция для проверки вызова get запроса.
    Проверяются позитивные варианты для id через параметризацию.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param param: передаваемые индексы сущностей для определения их id
    """
    with allure.step(allure_steps.get_id_with_param(param)):
        id_to_do_request: str = body_id_data.get_id_of_entity(booker_api, param)

    with allure.step(allure_steps.send_get_request(id_to_do_request)):
        response: requests.models.Response = booker_api.get(path=id_to_do_request)

    with allure.step(allure_steps.check_200_status_code()):
        assert response.status_code == 200, f"Код ответа - {response.status_code}"

    with allure.step(f"Проверяем длину тела ответа сущности с id {id_to_do_request}"):
        assert len(response.json()) != 0, "Такой сущности не существует"


@allure.feature("GET - GetBooking")
@allure.story("Получение несуществующей сущности по id")
@pytest.mark.negative
@pytest.mark.parametrize("param", ["10000", "hello", "0"])
def test_get_by_id_negative(booker_api: conftest.ApiClient,
                            param: str) -> None:
    """Тестовая функция для проверки вызова get запроса.
    Проверяются негативные варианты для id через параметризацию -
    несуществующий id.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param param: передаваемые в урле id сущностей
    """
    with allure.step(allure_steps.send_get_request(param)):
        response: requests.models.Response = booker_api.get(path=param)

    with allure.step(allure_steps.check_404_status_code()):
        assert response.status_code == 404, f"Код ответа - {response.status_code}"

    with allure.step("Проверяем, что текст ответа - Not found"):
        assert response.text == "Not Found", f"Текст ответа  - '{response.text}'"
