"""Модуль с тестами get запросов - GetBookingIds."""

import allure
import pytest

from helpers.schemas import GetBookingIds
from helpers.urls_helper import Params, Paths


@pytest.mark.get_booking_ids
@allure.feature('GET - GetBookingIds')
class TestGetBookingIds:
    """Тесты метода get /booking."""

    @allure.title('Получение списка всех броней')
    def test_get_all_bookings(
            self, booker_api, validate_json, check_response_status_code, response_body_msg, check_response_time):
        """Тестовая функция для проверки получения всех сущностей.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        response = booker_api.get(Paths.BOOKING)
        booking_data = response.json()

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(booking_data, GetBookingIds)

        with allure.step(response_body_msg(booking_data)):
            assert len(booking_data) != 0, 'Нет ни одной сущности'

    @allure.story('Проверка параметра firstname')
    @allure.title('Валидные значения firstname - {get_params}')
    @pytest.mark.parametrize('get_params', ['Sometest1', 'Olivia12'])
    def test_get_by_valid_firstname(
            self, booker_api, fixture_create_delete_booking_data,
            validate_json, check_response_status_code, response_body_msg, get_params,
            check_response_time):
        """Тестовая функция для проверки получения брони с валидными значениями параметра firstname.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param fixture_create_delete_booking_data: фикстура для создания и удаления тестовых данных
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        booking_id, booking_data = fixture_create_delete_booking_data(firstname=get_params)
        payload = {Params.FIRSTNAME: get_params}
        response = booker_api.get(path=Paths.BOOKING, params=payload)
        booking_data = response.json()

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(booking_data, GetBookingIds)

        with allure.step(response_body_msg(booking_data)):
            assert len(booking_data) == 1, f'Количество броней с именем {get_params} - {len(booking_data)}'
            assert booking_data[0]['bookingid'] == booking_id, f'Тело ответа {booking_data}'

    @allure.story('Проверка параметра firstname')
    @allure.title('Несуществующие значения firstname - {value}')
    @pytest.mark.parametrize('value', ['Тест', '13'])
    def test_get_by_invalid_firstname(
            self, booker_api, value, check_response_status_code, response_body_msg, check_response_time):
        """Тестовая функция для проверки получения брони с несуществующими значениями параметра firstname.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param value: передаваемый в урле параметр firstname
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        payload = {Params.FIRSTNAME: value}
        response = booker_api.get(path=Paths.BOOKING, params=payload)
        booking_data = response.json()

        check_response_status_code(response, 200)
        check_response_time(response)

        with allure.step(response_body_msg(booking_data)):
            assert len(booking_data) == 0, f'У {value} есть бронь. Тело ответа {booking_data}'

    @allure.story('Проверка параметра lastname')
    @allure.title('Существующие значения lastname - {get_params}')
    @pytest.mark.parametrize('get_params', ['SomeTest_2', 'Lalala'])
    def test_get_by_valid_lastname(
            self, booker_api, check_response_status_code, response_body_msg,
            validate_json, fixture_create_delete_booking_data, get_params,
            check_response_time):
        """Тестовая функция для проверки получения брони с существующими значениями параметра lastname.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param fixture_create_delete_booking_data: фикстура для создания и удаления тестовых данных
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        booking_id, booking_data = fixture_create_delete_booking_data(lastname=get_params)

        payload = {Params.LASTNAME: get_params}
        response = booker_api.get(path=Paths.BOOKING, params=payload)
        booking_data = response.json()

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(booking_data, GetBookingIds)

        with allure.step(response_body_msg(booking_data)):
            assert len(booking_data) == 1, f'Количество броней с фамилией {get_params} - {len(booking_data)}'
            assert booking_data[0]['bookingid'] == booking_id, f'Тело ответа {booking_data}'

    @allure.story('Проверка параметра lastname')
    @allure.title('Несуществующие значения lastname - {value}')
    @pytest.mark.parametrize('value', ['0', '$$@*:;'])
    def test_get_by_invalid_lastname(
            self, booker_api, value, check_response_status_code, response_body_msg, check_response_time):
        """Тестовая функция для проверки получения брони с несуществующими значениями параметра lastname.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param value: передаваемый в урле параметр lastname
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        payload = {Params.LASTNAME: value}
        response = booker_api.get(path=Paths.BOOKING, params=payload)
        booking_data = response.json()

        check_response_status_code(response, 200)
        check_response_time(response)

        with allure.step(response_body_msg(booking_data)):
            assert len(booking_data) == 0, f'У {value} есть бронь. Тело ответа {booking_data}'

    @allure.story('Проверка нескольких параметров')
    @allure.title('Существующие значения firstname {first} и lastname {last}')
    @pytest.mark.parametrize('first, last', [('test2', 'tester12')])
    def test_get_by_valid_fullname(
            self, booker_api, check_response_status_code, validate_json, response_body_msg,
            fixture_create_delete_booking_data, first, last, check_response_time):
        """Тестовая функция для проверки получения брони с существующими значениями параметров firstname и lastname.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param fixture_create_delete_booking_data: фикстура для создания и удаления тестовых данных
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        booking_id, booking_data = fixture_create_delete_booking_data(firstname=first, lastname=last)

        payload = {Params.FIRSTNAME: first, Params.LASTNAME: last}
        response = booker_api.get(path=Paths.BOOKING, params=payload)
        booking_data = response.json()

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(booking_data, GetBookingIds)

        with allure.step(response_body_msg(booking_data)):
            assert len(booking_data) == 1, \
                f'Количество броней с фамилией {last} и именем {first} - {len(booking_data)}'
            assert booking_data[0]['bookingid'] == booking_id, f'Тело ответа {booking_data}'

    @allure.story('Проверка нескольких параметров')
    @allure.title('Несуществующие значения firstname {first} и lastname {last}')
    @pytest.mark.parametrize('first, last', [('Eric', '0'), ('Test', 'Jones')])
    def test_get_by_invalid_fullname(
            self, booker_api, first, last, check_response_status_code, response_body_msg, check_response_time):
        """Тестовая функция для проверки получения брони с несуществующими значениями параметров firstname и lastname.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param first: передаваемый в урле параметр firstname
        :param last: передаваемый в урле параметр lastname
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        payload = {Params.FIRSTNAME: first, Params.LASTNAME: last}
        response = booker_api.get(path=Paths.BOOKING, params=payload)
        booking_data = response.json()

        check_response_status_code(response, 200)
        check_response_time(response)

        with allure.step(response_body_msg(booking_data)):
            assert len(booking_data) == 0, f'У {first} {last} есть бронь. Тело ответа {booking_data}'

    @allure.story('Проверка параметра checkin')
    @allure.title('Валидные значения checkin - {value}')
    @pytest.mark.parametrize('value', ['2022-11-15', '2021-02-01'])
    def test_get_by_valid_checkin(
            self, booker_api, value, check_response_status_code, response_body_msg, check_response_time):
        """Тестовая функция для проверки получения брони с валидными значениями параметра checkin.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param value: передаваемый в урле параметр checkin
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        payload = {Params.CHECKIN: value}
        response = booker_api.get(path=Paths.BOOKING, params=payload)
        booking_data = response.json()

        check_response_status_code(response, 200)
        check_response_time(response)

        with allure.step(response_body_msg(booking_data)):
            assert all([booker_api.get(path=f'{Paths.BOOKING}{i["bookingid"]}').json()['bookingdates']['checkin']
                        >= value for i in booking_data])

    @allure.story('Проверка параметра checkin')
    @allure.title('Невалидные значения checkin - {value}')
    @pytest.mark.parametrize('value', ['2222', '11-11-2023'])
    def test_get_by_invalid_checkin(
            self, booker_api, value, check_response_status_code, response_body_msg, check_response_time):
        """Тестовая функция для проверки получения брони с валидными значениями параметра checkin.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param value: передаваемый в урле параметр checkin
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        payload = {Params.CHECKIN: value}
        response = booker_api.get(path=Paths.BOOKING, params=payload)
        booking_data = response.json()

        check_response_status_code(response, 200)
        check_response_time(response)

        with allure.step(response_body_msg(booking_data)):
            assert len(booking_data) == 0, \
                f'Количество броней - {len(booking_data)}, тело ответа {booking_data}'
