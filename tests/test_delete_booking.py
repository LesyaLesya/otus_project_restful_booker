"""Модуль с тестами delete запросов - DeleteBooking."""


import allure
import pytest

from helpers.urls_helper import Paths


@pytest.mark.delete_booking
@allure.feature('DELETE - DeleteBooking')
class TestDeleteBooking:
    """Тесты метода delete /booking/id."""

    @allure.title('Удаление существующей брони по id с авторизацией через куки')
    def test_delete_by_exist_id_with_cookie(
            self, booker_api, create_test_booking, check_response_status_code, check_response_time):
        """Тестовая функция для проверки удаления бронирования по существующему id с авторизацией через куки.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param create_test_booking: фикстура, создающая тестовое бронирование
        :param check_response_status_code: фикстура, проверки кода ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        booking_id = create_test_booking()['bookingid']
        response = booker_api.delete(path=f'{Paths.BOOKING}{booking_id}')

        check_response_status_code(response, 201)
        check_response_time(response)

        get_after_delete = booker_api.get(path=f'{Paths.BOOKING}{booking_id}')
        check_response_status_code(get_after_delete, 404)

    @allure.title('Удаление существующей брони по id с авторизацией через basic auth')
    def test_delete_by_exist_id_with_basic_auth(
            self, booker_api, create_test_booking, check_response_status_code, check_response_time):
        """Тестовая функция для проверки удаления бронирования по существующему id  с авторизацией через basic auth.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param create_test_booking: фикстура, создающая тестовое бронирование
        :param check_response_status_code: фикстура, проверки кода ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        booking_id = create_test_booking()['bookingid']
        response = booker_api.delete(path=f'{Paths.BOOKING}{booking_id}', auth_type='basic_auth')

        check_response_status_code(response, 201)
        check_response_time(response)

        get_after_delete = booker_api.get(path=f'{Paths.BOOKING}{booking_id}')
        check_response_status_code(get_after_delete, 404)

    @allure.title('Удаление брони по невалидному/несуществующему id - {value}')
    @pytest.mark.parametrize('value', ['abc', '123112'])
    def test_delete_by_invalid_id(self, booker_api, value, check_response_status_code, check_response_time):
        """Тестовая функция для проверки удаления бронирования по невалидным id.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param value: передаваемый в урле id
        :param check_response_status_code: фикстура, проверки кода ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        response = booker_api.delete(path=f'{Paths.BOOKING}{value}')

        check_response_status_code(response, 405)
        check_response_time(response)

    @allure.title('Удаление существующей брони без авторизации')
    def test_delete_without_auth(
            self, booker_api, fixture_create_delete_booking_data, check_response_status_code,
            response_body_msg, check_response_time):
        """Тестовая функция для проверки удаления бронирования без авторизации.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param fixture_create_delete_booking_data: фикстура для создания и удаления тестовых данных
        :param check_response_status_code: фикстура, проверки кода ответа
        :param check_response_time: фикстура проверки времени ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        """
        booking_id, booking_test_data = fixture_create_delete_booking_data()
        response = booker_api.delete(
            path=f'{Paths.BOOKING}{booking_id}', headers_new={'Content-Type': 'application/json'})
        response_text = response.text

        check_response_status_code(response, 403)
        check_response_time(response)

        with allure.step(response_body_msg(response_text)):
            assert response_text == 'Forbidden', f'Тело ответа без авторизации - {response_text}'

        get_after_delete = booker_api.get(path=f'{Paths.BOOKING}{booking_id}')
        get_after_delete_body = get_after_delete.json()
        check_response_status_code(get_after_delete, 200)
        with allure.step(response_body_msg(get_after_delete_body)):
            assert get_after_delete_body == booking_test_data, \
                f'Бронь после попытки удаления без авторизации {get_after_delete_body}'
