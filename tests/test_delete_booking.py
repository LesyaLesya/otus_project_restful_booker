"""Модуль с тестами delete запросов - DeleteBooking."""


import allure
import pytest

from helpers.urls_helper import Paths


@pytest.mark.delete_booking
@allure.feature('DELETE - DeleteBooking')
class TestDeleteBooking:
    """Тесты метода delete /booking/id."""

    @allure.title('Удаление существующей брони по id с авторизацией через куки')
    def test_delete_by_exist_id_with_cookie(self, booker_api, create_test_booking, status_code_msg):
        """Тестовая функция для проверки удаления бронирования по существующему id с авторизацией через куки.

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

    @allure.title('Удаление существующей брони по id с авторизацией через basic auth')
    def test_delete_by_exist_id_with_basic_auth(self, booker_api, create_test_booking, status_code_msg):
        """Тестовая функция для проверки удаления бронирования по существующему id  с авторизацией через basic auth.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param create_test_booking: фикстура, создающая тестовое бронирование
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        """
        booking_id = create_test_booking()['bookingid']
        response = booker_api.delete(path=f'{Paths.BOOKING}{booking_id}', auth='basic_auth')

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

    @allure.title('Удаление существующей брони без токена')
    def test_delete_without_token(
            self, booker_api, fixture_create_delete_booking_data, status_code_msg, response_body_msg):
        """Тестовая функция для проверки удаления бронирования без токена.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param fixture_create_delete_booking_data: фикстура для создания и удаления тестовых данных
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        """
        booking_id, booking_test_data = fixture_create_delete_booking_data
        response = booker_api.delete(
            path=f'{Paths.BOOKING}{booking_id}', headers_new={'Content-Type': 'application/json'})
        response_text = response.text

        with allure.step(status_code_msg(403)):
            assert response.status_code == 403, f'Код ответа - {response.status_code}'

        with allure.step(response_body_msg(response_text)):
            assert response_text == 'Forbidden', f'Тело ответа без токена - {response_text}'

        get_after_delete = booker_api.get(path=f'{Paths.BOOKING}{booking_id}')
        get_after_delete_body = get_after_delete.json()
        with allure.step(status_code_msg(200)):
            assert get_after_delete.status_code == 200, f'Код ответа - {get_after_delete.status_code}'
        with allure.step(response_body_msg(get_after_delete_body)):
            assert get_after_delete_body == booking_test_data, \
                f'Бронь после попытки удаления без токена {get_after_delete_body}'
