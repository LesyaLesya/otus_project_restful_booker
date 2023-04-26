"""Модуль с тестами get запросов - GetBooking."""


import allure
import pytest

from helpers.schemas import GET_BOOKING_SCHEMA, GET_BOOKING_SCHEMA_XSD
from helpers.urls_helper import Paths


@pytest.mark.get_booking
@allure.feature('GET - GetBooking')
class TestGetBooking:
    """Тесты метода get /booking/id."""

    @allure.title('Получение существующей брони по id')
    def test_get_by_exist_id(
            self, booker_api, fixture_create_delete_booking_data, validate_json,
            status_code_msg, response_body_msg):
        """Тестовая функция для проверки получения бронирования по существующему id.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param validate_json: фикстура для валидации JSON схемы
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param fixture_create_delete_booking_data: фикстура для создания и удаления тестовых данных
        """
        booking_id, booking_test_data = fixture_create_delete_booking_data
        response = booker_api.get(path=f'{Paths.BOOKING}{booking_id}')
        booking_data = response.json()

        with allure.step(status_code_msg(200)):
            assert response.status_code == 200, f'Код ответа - {response.status_code}'

        assert validate_json(booking_data, GET_BOOKING_SCHEMA)

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
    def test_get_by_invalid_id(self, booker_api, value, status_code_msg, response_body_msg):
        """Тестовая функция для проверки получения бронирования по невалидному id.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param value: передаваемые в урле id сущностей
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        """
        response = booker_api.get(path=f'{Paths.BOOKING}{value}')
        response_body = response.text

        with allure.step(status_code_msg(404)):
            assert response.status_code == 404, f'Код ответа - {response.status_code}'

        with allure.step(response_body_msg(response_body)):
            assert response_body == 'Not Found', f'Текст ответа - {response_body}'

    @allure.title('Получение существующей брони по id - проверка получения ответа в xml')
    def test_get_by_exist_id_in_xml(
            self, booker_api, fixture_create_delete_booking_data, validate_xml,
            status_code_msg, response_body_msg, parsing_xml_response, get_text_of_element_xml_tree):
        """Тестовая функция для проверки получения бронирования по существующему id в xml.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param fixture_create_delete_booking_data: фикстура для создания и удаления тестовых данных
        :param parsing_xml_response: фикстура парсинга XML из строки
        :param get_text_of_element_xml_tree: фикстура получения текста элемента XML дерева
        :param validate_xml: фикстура валидации xml схемы
        """
        booking_id, booking_test_data = fixture_create_delete_booking_data
        response = booker_api.get(
            path=f'{Paths.BOOKING}{booking_id}', in_xml=True)
        booking_data = response.text

        with allure.step(status_code_msg(200)):
            assert response.status_code == 200, f'Код ответа - {response.status_code}'

        assert validate_xml(booking_data, GET_BOOKING_SCHEMA_XSD)

        with allure.step(response_body_msg(booking_data)):
            tree = parsing_xml_response(booking_data)
            firstname = get_text_of_element_xml_tree(tree, 'firstname')
            lastname = get_text_of_element_xml_tree(tree, 'lastname')
            totalprice = int(get_text_of_element_xml_tree(tree, 'totalprice'))
            depositpaid = bool(get_text_of_element_xml_tree(tree, 'depositpaid'))
            checkin = get_text_of_element_xml_tree(tree, 'bookingdates/checkin')
            checkout = get_text_of_element_xml_tree(tree, 'bookingdates/checkout')
            additionalneeds = get_text_of_element_xml_tree(tree, 'additionalneeds')

            assert firstname == booking_test_data['firstname'], f'firstname - {firstname}'
            assert lastname == booking_test_data['lastname'], f'lastname - {lastname}'
            assert totalprice == booking_test_data['totalprice'], f'totalprice - {totalprice}'
            assert depositpaid == booking_test_data['depositpaid'], f'depositpaid - {depositpaid}'
            assert checkin == booking_test_data['bookingdates']['checkin'], f'checkin - {checkin}'
            assert checkout == booking_test_data['bookingdates']['checkout'], f'checkout - {checkout}'
            assert additionalneeds == booking_test_data['additionalneeds'], f'additionalneeds - {additionalneeds}'

    @pytest.mark.parametrize('header', ['text/plain', 'text/html', 'application/pdf'])
    @allure.title('Получение существующей брони с невалидным заголовком')
    def test_get_by_exist_id_with_invalid_headers(
            self, booker_api, fixture_create_delete_booking_data, validate_json,
            status_code_msg, response_body_msg, header):
        """Тестовая функция для проверки получения бронирования по существующему id.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param validate_json: фикстура для валидации JSON схемы
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param fixture_create_delete_booking_data: фикстура для создания и удаления тестовых данных
        :param header: значение заголовка Accept
        """
        booking_id, booking_test_data = fixture_create_delete_booking_data
        response = booker_api.get(path=f'{Paths.BOOKING}{booking_id}', headers_new={'Accept': header})
        response_text = response.text

        with allure.step(status_code_msg(418)):
            assert response.status_code == 418, f'Код ответа - {response.status_code}'

        with allure.step(response_body_msg(response_text)):
            assert response_text == "I'm a Teapot", \
                f'Ответ при невалидном заголовке Accept: {header} - {response_text}'
