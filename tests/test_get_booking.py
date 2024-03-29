"""Модуль с тестами get запросов - GetBooking."""


import allure
import pytest

from helpers.base_functions import get_xml_response_data
from helpers.schemas import GetBookingSchema, XSDSchemas
from helpers.urls_helper import Paths


@pytest.mark.get_booking
@allure.feature('GET - GetBooking')
class TestGetBooking:
    """Тесты метода get /booking/id."""

    @allure.title('Получение существующей брони по id')
    def test_get_by_exist_id(
            self, booker_api, fixture_create_delete_booking_data, validate_json,
            check_response_status_code, response_body_msg, check_response_time):
        """Тестовая функция для проверки получения бронирования по существующему id.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param fixture_create_delete_booking_data: фикстура для создания и удаления тестовых данных
        :param check_response_time: фикстура проверки времени ответа
        """
        booking_id, booking_test_data = fixture_create_delete_booking_data()
        response = booker_api.get(path=f'{Paths.BOOKING}{booking_id}')
        booking_data = response.json()

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(booking_data, GetBookingSchema)

        with allure.step(response_body_msg(booking_data)):
            assert booking_data['firstname'] == booking_test_data['firstname'], \
                f'firstname - {booking_data["firstname"]}'
            assert booking_data['lastname'] == booking_test_data['lastname'], \
                f'lastname - {booking_data["lastname"]}'
            assert booking_data['totalprice'] == booking_test_data['totalprice'], \
                f'totalprice - {booking_data["totalprice"]}'
            assert booking_data['depositpaid'] == booking_test_data['depositpaid'], \
                f'depositpaid - {booking_data["depositpaid"]}'
            assert booking_data['bookingdates']['checkin'] == booking_test_data['bookingdates']['checkin'], \
                f'checkin - {booking_data["bookingdates"]["checkin"]}'
            assert booking_data['bookingdates']['checkout'] == booking_test_data['bookingdates']['checkout'], \
                f'checkout - {booking_data["bookingdates"]["checkout"]}'
            assert booking_data['additionalneeds'] == booking_test_data['additionalneeds'], \
                f'additionalneeds - {booking_data["additionalneeds"]}'

    @allure.title('Получение брони по невалидному id - {value}')
    @pytest.mark.parametrize('value', ['10000000', 'hello', '0'])
    def test_get_by_invalid_id(
            self, booker_api, value, check_response_status_code, response_body_msg, check_response_time):
        """Тестовая функция для проверки получения бронирования по невалидному id.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param value: передаваемые в урле id сущностей
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        response = booker_api.get(path=f'{Paths.BOOKING}{value}')
        response_body = response.text

        check_response_status_code(response, 404)
        check_response_time(response, 300)

        with allure.step(response_body_msg(response_body)):
            assert response_body == 'Not Found', f'Текст ответа - {response_body}'

    @allure.title('Получение существующей брони по id - проверка получения ответа в xml')
    def test_get_by_exist_id_in_xml(
            self, booker_api, fixture_create_delete_booking_data, validate_xml,
            check_response_status_code, response_body_msg, check_response_time):
        """Тестовая функция для проверки получения бронирования по существующему id в xml.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param fixture_create_delete_booking_data: фикстура для создания и удаления тестовых данных
        :param validate_xml: фикстура валидации xml схемы
        :param check_response_time: фикстура проверки времени ответа
        """
        booking_id, booking_test_data = fixture_create_delete_booking_data()
        response = booker_api.get(
            path=f'{Paths.BOOKING}{booking_id}', accept_header='xml')
        booking_data = response.text

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_xml(booking_data, XSDSchemas.GET_BOOKING_SCHEMA_XSD)

        with allure.step(response_body_msg(booking_data)):
            firstname, lastname, totalprice, depositpaid, checkin, checkout, additionalneeds = \
                get_xml_response_data(
                    booking_data, 'firstname', 'lastname', 'totalprice', 'depositpaid',
                    'bookingdates/checkin', 'bookingdates/checkout', 'additionalneeds')

            assert firstname == booking_test_data['firstname'], f'firstname - {firstname}'
            assert lastname == booking_test_data['lastname'], f'lastname - {lastname}'
            assert totalprice == str(booking_test_data['totalprice']), f'totalprice - {totalprice}'
            assert depositpaid == str(booking_test_data['depositpaid']).lower(), f'depositpaid - {depositpaid}'
            assert checkin == booking_test_data['bookingdates']['checkin'], f'checkin - {checkin}'
            assert checkout == booking_test_data['bookingdates']['checkout'], f'checkout - {checkout}'
            assert additionalneeds == booking_test_data['additionalneeds'], f'additionalneeds - {additionalneeds}'

    @pytest.mark.parametrize('header', ['text/plain', 'text/html', 'application/pdf'])
    @allure.title('Получение существующей брони с невалидным заголовком')
    def test_get_by_exist_id_with_invalid_headers(
            self, booker_api, fixture_create_delete_booking_data, validate_json,
            check_response_status_code, response_body_msg, header, check_response_time):
        """Тестовая функция для проверки получения бронирования по существующему id.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param fixture_create_delete_booking_data: фикстура для создания и удаления тестовых данных
        :param header: значение заголовка Accept
        :param check_response_time: фикстура проверки времени ответа
        """
        booking_id, booking_test_data = fixture_create_delete_booking_data()
        response = booker_api.get(path=f'{Paths.BOOKING}{booking_id}', headers_new={'Accept': header})
        response_text = response.text

        check_response_status_code(response, 418)
        check_response_time(response)

        with allure.step(response_body_msg(response_text)):
            assert response_text == "I'm a Teapot", \
                f'Ответ при невалидном заголовке Accept: {header} - {response_text}'
