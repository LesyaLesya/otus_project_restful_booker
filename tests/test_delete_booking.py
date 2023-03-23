"""Модуль с тестами delete запросов - DeleteBooking."""


import allure
import pytest

from helpers.urls_helper import Paths


@pytest.mark.delete_booking
@allure.feature('DELETE - DeleteBooking')
class TestDeleteBooking:
    """Тесты метода delete /booking/id."""

    @allure.title('Удаление существующей брони по id')
    def test_delete_by_exist_id(self, booker_api, create_test_booking, status_code_msg):
        """Тестовая функция для проверки удаления бронирования по существующему id.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param create_test_booking: фикстура, создающая тестовое бронирование
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        """
        booking_id = create_test_booking()['bookingid']
        response = booker_api.delete(path=f'{Paths.BOOKING}{booking_id}')

        with allure.step(status_code_msg(201)):
            assert response.status_code == 201, f'Код ответа - {response.status_code}'

        get_after_delete = booker_api.get(path=f'{Paths.BOOKING}{booking_id}')
        with allure.step(status_code_msg(404)):
            assert get_after_delete.status_code == 404, f'Код ответа - {get_after_delete.status_code}'

    @allure.title('Удаление брони по невалидному/несуществующему id - {value}')
    @pytest.mark.parametrize('value', ['abc', '123112'])
    def test_delete_by_invalid_id(self, booker_api, value, status_code_msg):
        """Тестовая функция для проверки удаления бронирования по невалидным id.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param value: передаваемый в урле id
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        """
        response = booker_api.delete(path=f'{Paths.BOOKING}{value}')

        with allure.step(status_code_msg(405)):
            assert response.status_code == 405, f'Код ответа - {response.status_code}'
