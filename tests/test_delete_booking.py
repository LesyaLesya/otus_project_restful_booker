""" Модуль с тестами delete запросов - DeleteBooking. """


import pytest
import requests
import allure  # type: ignore
import conftest


@allure.feature("DELETE - DeleteBooking")
@allure.story("Удаление существующей сущности по id")
@pytest.mark.positive
@pytest.mark.parametrize("param", [-1, -2])
def test_delete_by_id_positive(booker_api: conftest.ApiClient,
                               param: int) -> None:
    """
    Тестовая функция для проверки вызова delete запроса.
    Проверяются позитивные варианты через параметризацию - существующие id.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param param: передаваемый в урле id - индекс сущности,
    полученный вызовом get запроса на получение всех сущностей

    """
    with allure.step("Получаем список всех сущностей"):
        get_all_ids: requests.models.Response = booker_api.get()

    with allure.step("Определяем id последних двух элементов в полученном спике"):
        id_to_delete: str = get_all_ids.json()[param]['bookingid']

    with allure.step(f"Отправляем delete запрос с id {id_to_delete}"):
        response: requests.models.Response = \
            booker_api.delete(path=id_to_delete)

    with allure.step("Проверяем, что код ответа 201"):
        assert response.status_code == 201, f"Код ответа - {response.status_code}"


@allure.feature("DELETE - DeleteBooking")
@allure.story("Удаление несуществующей сущности по id")
@pytest.mark.negative
@pytest.mark.parametrize("param", ["abc", "123112"])
def test_delete_by_id_negative(booker_api: conftest.ApiClient,
                               param: str) -> None:
    """
    Тестовая функция для проверки вызова delete запроса.
    Проверяются негативные варианты через параметризацию
    - несуществующие id.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param param: передаваемый в урле id

    """
    with allure.step(f"Отправляем delete запрос с id {param}"):
        response: requests.models.Response = booker_api.delete(path=param)

    with allure.step("Проверяем, что код ответа 405"):
        assert response.status_code == 405, f"Код ответа - {response.status_code}"
