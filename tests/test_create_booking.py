"""Модуль с тестами post запросов - CreateBooking."""

import allure
import pytest

from helpers.base_functions import get_xml_response_data
from helpers.schemas import CREATE_BOOKING_SCHEMA, CREATE_BOOKING_SCHEMA_XSD
from helpers.urls_helper import Paths


@pytest.fixture
def fixture_post_booking_firstname(booker_api, generate_body_booking, delete_test_booking, get_params):
    data = generate_body_booking(firstname=get_params)
    response = booker_api.post(Paths.BOOKING, data)
    booking_data = response.json()
    booking_id = booking_data['bookingid']
    yield response, booking_data, booking_id
    delete_test_booking(booking_id)


@pytest.fixture
def fixture_post_booking_lastname(booker_api, generate_body_booking, delete_test_booking, get_params):
    data = generate_body_booking(lastname=get_params)
    response = booker_api.post(Paths.BOOKING, data)
    booking_data = response.json()
    booking_id = booking_data['bookingid']
    yield response, booking_data, booking_id
    delete_test_booking(booking_id)


@pytest.fixture
def fixture_post_booking_totalprice(booker_api, generate_body_booking, delete_test_booking, get_params):
    data = generate_body_booking(totalprice=get_params)
    response = booker_api.post(Paths.BOOKING, data)
    try:
        booking_data = response.json()
        booking_id = booking_data['bookingid']
    except:
        booking_data = response.text
        booking_id = None
    yield response, booking_data, booking_id
    delete_test_booking(booking_id)


@pytest.fixture
def fixture_post_booking_deposit(booker_api, generate_body_booking, delete_test_booking, get_params):
    data = generate_body_booking(depositpaid=get_params)
    response = booker_api.post(Paths.BOOKING, data)
    try:
        booking_data = response.json()
        booking_id = booking_data['bookingid']
    except:
        booking_data = response.text
        booking_id = None
    yield response, booking_data, booking_id
    delete_test_booking(booking_id)


@pytest.fixture
def fixture_post_booking_checkin(booker_api, generate_body_booking, delete_test_booking, get_params):
    data = generate_body_booking(checkin=get_params)
    response = booker_api.post(Paths.BOOKING, data)
    booking_data = response.json()
    booking_id = booking_data['bookingid']
    yield response, booking_data, booking_id
    delete_test_booking(booking_id)


@pytest.fixture
def fixture_post_booking_checkout(booker_api, generate_body_booking, delete_test_booking, get_params):
    data = generate_body_booking(checkout=get_params)
    response = booker_api.post(Paths.BOOKING, data)
    booking_data = response.json()
    booking_id = booking_data['bookingid']
    yield response, booking_data, booking_id
    delete_test_booking(booking_id)


@pytest.fixture
def fixture_post_booking_additionalneeds(booker_api, generate_body_booking, delete_test_booking, get_params):
    data = generate_body_booking(additionalneeds=get_params)
    response = booker_api.post(Paths.BOOKING, data)
    booking_data = response.json()
    booking_id = booking_data['bookingid']
    yield response, booking_data, booking_id
    delete_test_booking(booking_id)


@pytest.fixture
def fixture_post_booking_without_additionalneeds(booker_api, generate_body_booking, delete_test_booking):
    data = generate_body_booking(key_to_del=['additionalneeds'])
    response = booker_api.post(Paths.BOOKING, data)
    booking_data = response.json()
    booking_id = booking_data['bookingid']
    yield response, booking_data, booking_id
    delete_test_booking(booking_id)


@pytest.fixture
def fixture_post_booking_repeat(booker_api, generate_body_booking, delete_test_booking):
    data = generate_body_booking()
    response_first = booker_api.post(Paths.BOOKING, data)
    response_repeat = booker_api.post(Paths.BOOKING, data)
    booking_data_first = response_first.json()
    booking_data_repeat = response_repeat.json()
    booking_id_first = booking_data_first['bookingid']
    booking_id_repeat = booking_data_repeat['bookingid']
    yield data, response_first, response_repeat
    delete_test_booking(booking_id_first)
    delete_test_booking(booking_id_repeat)


@pytest.fixture
def fixture_post_booking_firstname_xml(
        booker_api, generate_body_booking, delete_test_booking, get_params):
    data_xml, data = generate_body_booking(firstname=get_params, convert='xml')
    response = booker_api.post(Paths.BOOKING, data_xml, cont_type='xml', accept_header='xml')
    booking_data = response.text
    booking_id, firstname = get_xml_response_data(booking_data, 'bookingid', 'booking/firstname')
    yield response, booking_data, booking_id, firstname
    delete_test_booking(booking_id)


@pytest.fixture
def fixture_post_booking_firstname_urlencoded(
        booker_api, generate_body_booking, delete_test_booking, get_params):
    data_urlencoded, data = generate_body_booking(firstname=get_params, convert='urlencoded')
    response = booker_api.post(Paths.BOOKING, data_urlencoded, cont_type='urlencoded')
    booking_data = response.json()
    booking_id = booking_data['bookingid']
    yield response, booking_data, booking_id
    delete_test_booking(booking_id)


@pytest.mark.create_booking
@allure.feature('POST - CreateBooking - JSON')
class TestCreateBookingJSON:
    """Тесты метода post /booking - JSON."""

    @allure.story('Проверка firstname')
    @allure.title('Валидные значения firstname - {get_params}')
    @pytest.mark.parametrize('get_params', ['Peter', 'Maria-Elena', 'Имя Имя', ''])
    def test_post_valid_firstname(
            self, fixture_post_booking_firstname, validate_json, check_response_status_code,
            response_body_msg, get_params, check_response_time):
        """Тестовая функция для проверки создания бронирования с валидным именем.

        :param fixture_post_booking_firstname: фикстура создания и удаления тестовых данных и отправки запроса
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        response, booking_data, booking_id = fixture_post_booking_firstname

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(booking_data, CREATE_BOOKING_SCHEMA)

        with allure.step(response_body_msg(booking_data)):
            assert booking_data['booking']['firstname'] == get_params, \
                f'Имя - {booking_data["booking"]["firstname"]}'

    @allure.story('Проверка firstname')
    @allure.title('Невалидные значения firstname - {value}')
    @pytest.mark.parametrize('value', [123, True, None])
    def test_post_invalid_firstname(
            self, booker_api, value, generate_body_booking, check_response_status_code,
            response_body_msg, check_response_time):
        """Тестовая функция для проверки создания бронирования с невалидным именем.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param value: передаваемые в теле запроса варианты для "firstname"
        :param generate_body_booking: фикстура, создающая тело для запроса
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        data = generate_body_booking(firstname=value)
        response = booker_api.post(Paths.BOOKING, data)
        response_body = response.text

        check_response_status_code(response, 500)
        check_response_time(response)

        with allure.step(response_body_msg(response_body)):
            assert response_body == 'Internal Server Error', f'Тело ответа  - {response_body}'

    @allure.story('Проверка firstname')
    @allure.title('Не передавать в теле firstname')
    def test_post_without_firstname(
            self, booker_api, generate_body_booking, check_response_status_code,
            response_body_msg, check_response_time):
        """Тестовая функция для проверки создания бронирования без имени.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param generate_body_booking: фикстура, создающая тело для запроса
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        data = generate_body_booking(key_to_del=['firstname'])
        response = booker_api.post(Paths.BOOKING, data)
        response_body = response.text

        check_response_status_code(response, 500)
        check_response_time(response)

        with allure.step(response_body_msg(response_body)):
            assert response_body == 'Internal Server Error', f'Тело ответа  - {response_body}'

    @allure.story('Проверка lastname')
    @allure.title('Валидные значения lastname - {get_params}')
    @pytest.mark.parametrize('get_params', ['Иванов', 'Black', 'W', 'Last-name', ''])
    def test_post_valid_lastname(
            self, validate_json, check_response_status_code, response_body_msg,
            fixture_post_booking_lastname, get_params, check_response_time):
        """Тестовая функция для проверки создания бронирования с валидной фамилией.

        :param fixture_post_booking_lastname: фикстура создания и удаления тестовых данных и отправки запроса
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        response, booking_data, booking_id = fixture_post_booking_lastname

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(booking_data, CREATE_BOOKING_SCHEMA)

        with allure.step(response_body_msg(booking_data)):
            assert booking_data['booking']['lastname'] == get_params, \
                f'Фамилия - {booking_data["booking"]["lastname"]}'

    @allure.story('Проверка lastname')
    @allure.title('Невалидные значения lastname - {value}')
    @pytest.mark.parametrize('value', [['sth'], {}, None])
    def test_post_invalid_lastname(
            self, booker_api, value, generate_body_booking, check_response_status_code,
            response_body_msg, check_response_time):
        """Тестовая функция для проверки создания бронирования с невалидной фамилией.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param value: передаваемые в теле запроса варианты для "lastname"
        :param generate_body_booking: фикстура, создающая тело для запроса
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        data = generate_body_booking(lastname=value)
        response = booker_api.post(Paths.BOOKING, data)
        response_body = response.text

        check_response_status_code(response, 500)
        check_response_time(response)

        with allure.step(response_body_msg(response_body)):
            assert response_body == 'Internal Server Error', f'Тело ответа  - {response_body}'

    @allure.story('Проверка lastname')
    @allure.title('Не передавать в теле lastname')
    def test_post_without_lastname(
            self, booker_api, generate_body_booking, check_response_status_code,
            response_body_msg, check_response_time):
        """Тестовая функция для проверки создания бронирования без фамилии.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param generate_body_booking: фикстура, создающая тело для запроса
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        data = generate_body_booking(key_to_del=['lastname'])
        response = booker_api.post(Paths.BOOKING, data)
        response_body = response.text

        check_response_status_code(response, 500)
        check_response_time(response)

        with allure.step(response_body_msg(response_body)):
            assert response_body == 'Internal Server Error', f'Тело ответа  - {response_body}'

    @allure.story('Проверка totalprice')
    @allure.title('Валидные значения totalprice - {get_params}')
    @pytest.mark.parametrize('get_params', [123, 1, 566778, 11.2, 0.6])
    def test_post_valid_totalprice(
            self, fixture_post_booking_totalprice,
            validate_json, check_response_status_code, response_body_msg, get_params, check_response_time):
        """Тестовая функция для проверки создания бронирования с валидной ценой.

        :param fixture_post_booking_totalprice: фикстура создания и удаления тестовых данных и отправки запроса
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        response, booking_data, booking_id = fixture_post_booking_totalprice

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(booking_data, CREATE_BOOKING_SCHEMA)

        with allure.step(response_body_msg(booking_data)):
            assert booking_data['booking']['totalprice'] == int(get_params), \
                f'Общая сумма - {booking_data["booking"]["totalprice"]}'

    @allure.story('Проверка totalprice')
    @allure.title('Невалидные значения totalprice - {get_params}')
    @pytest.mark.parametrize('get_params', [False, 'test', None])
    def test_post_invalid_totalprice(
            self, fixture_post_booking_totalprice, get_params, check_response_status_code,
            response_body_msg, check_response_time, validate_json):
        """Тестовая функция для проверки создания бронирования с невалидной ценой.

        :param fixture_post_booking_totalprice: фикстура создания и удаления тестовых данных и отправки запроса
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        :param validate_json: фикстура для валидации JSON схемы
        """
        response, booking_data, booking_id = fixture_post_booking_totalprice

        check_response_time(response)

        if get_params is None:
            check_response_status_code(response, 500)
            with allure.step(response_body_msg(booking_data)):
                assert booking_data == 'Internal Server Error', f'Тело ответа  - {booking_data}'
        else:
            check_response_status_code(response, 200)
            validate_json(booking_data, CREATE_BOOKING_SCHEMA)
            with allure.step(response_body_msg(booking_data)):
                assert booking_data['booking']['totalprice'] is None, \
                    f'Тело ответа  - {booking_data}["booking"]["totalprice"]'

    @allure.story('Проверка totalprice')
    @allure.title('Не передавать в теле totalprice')
    def test_post_without_totalprice(
            self, booker_api, generate_body_booking, check_response_status_code,
            response_body_msg, check_response_time):
        """Тестовая функция для проверки создания бронирования без цены.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param generate_body_booking: фикстура, создающая тело для запроса
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        data = generate_body_booking(key_to_del=['totalprice'])
        response = booker_api.post(Paths.BOOKING, data)
        response_body = response.text

        check_response_status_code(response, 500)
        check_response_time(response)

        with allure.step(response_body_msg(response_body)):
            assert response_body == 'Internal Server Error', f'Тело ответа  - {response_body}'

    @allure.story('Проверка depositpaid')
    @allure.title('Валидные значения depositpaid - {get_params}')
    @pytest.mark.parametrize('get_params', [True, False])
    def test_post_valid_depositpaid(
            self, validate_json, check_response_status_code, response_body_msg,
            fixture_post_booking_deposit, get_params, check_response_time):
        """Тестовая функция для проверки создания бронирования с валидным depositpaid.

        :param fixture_post_booking_deposit:  фикстура создания и удаления тестовых данных и отправки запроса
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        response, booking_data, booking_id = fixture_post_booking_deposit

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(booking_data, CREATE_BOOKING_SCHEMA)

        with allure.step(response_body_msg(booking_data)):
            assert booking_data['booking']['depositpaid'] == get_params, \
                f'Статус внесения депозита - {booking_data["booking"]["depositpaid"]}'

    @allure.story('Проверка depositpaid')
    @allure.title('Невалидные значения depositpaid - {get_params}')
    @pytest.mark.parametrize('get_params', [123, 0, None, 'test'])
    def test_post_invalid_depositpaid(
            self, validate_json, check_response_status_code, response_body_msg,
            fixture_post_booking_deposit, get_params, check_response_time):
        """Тестовая функция для проверки создания бронирования с валидным depositpaid.

        :param fixture_post_booking_deposit:  фикстура создания и удаления тестовых данных и отправки запроса
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        response, booking_data, booking_id = fixture_post_booking_deposit

        check_response_time(response)

        if get_params is None:
            check_response_status_code(response, 500)
            with allure.step(response_body_msg(booking_data)):
                assert booking_data == 'Internal Server Error', f'Тело ответа  - {booking_data}'
        else:
            check_response_status_code(response, 200)
            validate_json(booking_data, CREATE_BOOKING_SCHEMA)
            with allure.step(response_body_msg(booking_data)):
                assert booking_data['booking']['depositpaid'] == bool(get_params), \
                    f'Статус внесения депозита - {booking_data["booking"]["depositpaid"]}'

    @allure.story('Проверка checkin')
    @allure.title('Валидные значения checkin - {get_params}')
    @pytest.mark.parametrize('get_params', ['1900-11-11', '2021-02-11', '2030-06-01'])
    def test_post_valid_checkin(
            self, validate_json, check_response_status_code, response_body_msg,
            fixture_post_booking_checkin, get_params, check_response_time):
        """Тестовая функция для проверки создания бронирования с валидным checkin.

        :param fixture_post_booking_checkin: фикстура создания и удаления тестовых данных и отправки запроса
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        response, booking_data, booking_id = fixture_post_booking_checkin

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(booking_data, CREATE_BOOKING_SCHEMA)

        with allure.step(response_body_msg(booking_data)):
            assert booking_data['booking']['bookingdates']['checkin'] == get_params, \
                f'Дата заезда - {booking_data["booking"]["bookingdates"]["checkin"]}'

    @allure.story('Проверка checkin')
    @allure.title('Невалидные значения checkin - {get_params}')
    @pytest.mark.parametrize('get_params', ['00-00-00', 'tests', ' '])
    def test_post_invalid_checkin(
            self, validate_json, check_response_status_code, response_body_msg,
            fixture_post_booking_checkin, get_params, check_response_time):
        """Тестовая функция для проверки создания бронирования с невалидным checkin.

        :param fixture_post_booking_checkin: фикстура создания и удаления тестовых данных и отправки запроса
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        response, booking_data, booking_id = fixture_post_booking_checkin

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(booking_data, CREATE_BOOKING_SCHEMA)

        with allure.step(response_body_msg(booking_data)):
            assert booking_data['booking']['bookingdates']['checkin'] == '0NaN-aN-aN', \
                f'Дата заезда - {booking_data["booking"]["bookingdates"]["checkin"]}'

    @allure.story('Проверка checkout')
    @allure.title('Валидные значения checkout - {get_params}')
    @pytest.mark.parametrize('get_params', ['1871-01-01', '2021-02-11', '2041-12-31'])
    def test_post_valid_checkout(
            self, validate_json, check_response_status_code, response_body_msg,
            fixture_post_booking_checkout, get_params, check_response_time):
        """Тестовая функция для проверки создания бронирования с валидным checkout.

        :param fixture_post_booking_checkout: фикстура создания и удаления тестовых данных и отправки запроса
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        response, booking_data, booking_id = fixture_post_booking_checkout

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(booking_data, CREATE_BOOKING_SCHEMA)

        with allure.step(response_body_msg(booking_data)):
            assert booking_data['booking']['bookingdates']['checkout'] == get_params, \
                f'Дата выезда - {booking_data["booking"]["bookingdates"]["checkout"]}'

    @allure.story('Проверка additionalneeds')
    @allure.title('Валидные значения additionalneeds - {get_params}')
    @pytest.mark.parametrize('get_params', ['что-то', 'dinner, breakfast', ''])
    def test_post_valid_additionalneeds(
            self, validate_json, check_response_status_code, response_body_msg,
            fixture_post_booking_additionalneeds, get_params, check_response_time):
        """Тестовая функция для проверки создания бронирования с валидным additionalneeds.

        :param fixture_post_booking_additionalneeds: фикстура создания и удаления тестовых данных и отправки запроса
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        response, booking_data, booking_id = fixture_post_booking_additionalneeds

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(booking_data, CREATE_BOOKING_SCHEMA)

        with allure.step(response_body_msg(booking_data)):
            assert booking_data['booking']['additionalneeds'] == get_params, \
                f'Дополнительные пожелания - {booking_data["booking"]["additionalneeds"]}'

    @allure.story('Проверка additionalneeds')
    @allure.title('Не передавать в теле additionalneeds')
    def test_post_without_additionalneeds(
            self, validate_json, check_response_status_code, response_body_msg,
            fixture_post_booking_without_additionalneeds, check_response_time):
        """Тестовая функция для проверки создания бронирования без additionalneeds.

        :param fixture_post_booking_without_additionalneeds: фикстура создания и удаления тестовых данных и отправки запроса
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        response, booking_data, booking_id = fixture_post_booking_without_additionalneeds

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(booking_data, CREATE_BOOKING_SCHEMA)

        with allure.step(response_body_msg(booking_data)):
            assert 'additionalneeds' not in booking_data, \
                f'Дополнительные пожелания - {booking_data["booking"]["additionalneeds"]}'

    @allure.title('Пустое тело запроса')
    def test_post_empty_body(
            self, booker_api, check_response_status_code, response_body_msg, check_response_time):
        """Тестовая функция для проверки создания бронирования с пустым телом.

        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        response = booker_api.post(Paths.BOOKING, {})
        response_body = response.text

        check_response_status_code(response, 500)
        check_response_time(response)

        with allure.step(response_body_msg(response_body)):
            assert response_body == 'Internal Server Error', f'Тело ответа  - {response_body}'

    @allure.title('Повторное создание бронирования')
    def test_post_repeat_create_booking(
            self, validate_json, check_response_status_code,
            response_body_msg, fixture_post_booking_repeat, check_response_time):
        """Тестовая функция для проверки повторного создания бронирования.

        :param fixture_post_booking_repeat: фикстура создания и удаления тестовых данных и отправки запроса
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        data, response_first, response_repeat = fixture_post_booking_repeat
        response_body_first = response_first.json()
        response_body_repeat = response_repeat.json()

        check_response_status_code(response_first, 200)
        check_response_status_code(response_repeat, 200)

        check_response_time(response_first)
        check_response_time(response_repeat)

        validate_json(response_body_first, CREATE_BOOKING_SCHEMA)
        validate_json(response_body_repeat, CREATE_BOOKING_SCHEMA)

        with allure.step(response_body_msg(response_body_repeat)):
            assert response_body_repeat['booking'] == data, f'Тело ответа  - {response_body_repeat}'


@pytest.mark.create_booking
@allure.feature('POST - CreateBooking - XML')
class TestCreateBookingXML:
    """Тесты метода post /booking - XML."""

    @allure.story('Проверка firstname')
    @allure.title('Валидные значения firstname')
    @pytest.mark.parametrize('get_params', ['Peter', 'Maria', '', 'имя'])
    def test_post_valid_firstname_xml(
            self, fixture_post_booking_firstname_xml, check_response_status_code, response_body_msg,
            get_params, validate_xml, check_response_time):
        """Тестовая функция для проверки создания бронирования с валидным именем.

        :param fixture_post_booking_firstname_xml: фикстура создания и удаления тестовых данных и отправки запроса (xml)
        :param validate_xml: фикстура валидации xml схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """

        response, booking_data, booking_id, firstname = fixture_post_booking_firstname_xml

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_xml(booking_data, CREATE_BOOKING_SCHEMA_XSD)

        with allure.step(response_body_msg(booking_data)):
            if get_params == '':
                assert firstname is None, f'Имя - {firstname}'
            else:
                assert firstname == get_params, f'Имя - {firstname}'

    @allure.story('Проверка firstname')
    @allure.title('Не передавать в теле firstname')
    def test_post_without_firstname_xml(
            self, booker_api, generate_body_booking, check_response_status_code,
            response_body_msg, check_response_time):
        """Тестовая функция для проверки создания бронирования без имени.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param generate_body_booking: фикстура, создающая тело для запроса
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        data_xml, data = generate_body_booking(key_to_del=['firstname'], convert='xml')
        response = booker_api.post(Paths.BOOKING, data_xml, cont_type='xml', accept_header='xml')
        response_body = response.text

        check_response_status_code(response, 500)
        check_response_time(response)

        with allure.step(response_body_msg(response_body)):
            assert response_body == 'Internal Server Error', f'Тело ответа  - {response_body}'


@pytest.mark.create_booking
@allure.feature('POST - CreateBooking - Urlencoded')
class TestCreateBookingUrlencoded:
    """Тесты метода post /booking - Urlencoded."""

    @allure.story('Проверка firstname')
    @allure.title('Валидные значения firstname')
    @pytest.mark.parametrize('get_params', ['', 'Anna Maria', 'Stacy', 'Аня'])
    def test_post_valid_firstname_urlencoded(
            self, booker_api, fixture_post_booking_firstname_urlencoded, validate_json,
            check_response_status_code, response_body_msg, check_response_time, get_params):
        """Тестовая функция для проверки создания бронирования с валидным именем.

        :param fixture_post_booking_firstname_urlencoded: фикстура создания и удаления тестовых данных и отправки запроса
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        response, booking_data, booking_id = fixture_post_booking_firstname_urlencoded

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(booking_data, CREATE_BOOKING_SCHEMA)

        with allure.step(response_body_msg(booking_data)):
            assert booking_data['booking']['firstname'] == get_params, \
                f'Имя - {booking_data["booking"]["firstname"]}'

    @allure.story('Проверка firstname')
    @allure.title('Не передавать в теле firstname')
    def test_post_without_firstname_urlencoded(
            self, booker_api, generate_body_booking, check_response_status_code,
            response_body_msg, check_response_time):
        """Тестовая функция для проверки создания бронирования без имени.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param generate_body_booking: фикстура, создающая тело для запроса
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        data_urlencoded, data = generate_body_booking(key_to_del=['firstname'], convert='urlencoded')
        response = booker_api.post(Paths.BOOKING, data_urlencoded, cont_type='urlencoded')
        response_body = response.text

        check_response_status_code(response, 500)
        check_response_time(response)

        with allure.step(response_body_msg(response_body)):
            assert response_body == 'Internal Server Error', f'Тело ответа  - {response_body}'


@pytest.mark.create_booking
@allure.feature('POST - CreateBooking - Other data types')
class TestCreateBookingOtherDataType:
    """Тесты метода post /booking - Other data types."""

    @allure.story('Проверка заголовков')
    @allure.title('Content-type: {cont_type}')
    @pytest.mark.parametrize('cont_type', ['text/plain', 'text/html'])
    def test_post_with_invalid_content_type(
            self, booker_api, check_response_status_code, response_body_msg,
            generate_body_booking, cont_type, check_response_time):
        """Тестовая функция для проверки создания бронирования с заголовком Content-type: text/plain.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param generate_body_booking: фикстура, создающая тело для запроса
        :param cont_type: значение заголовка Content-type
        :param check_response_time: фикстура проверки времени ответа
        """
        data = generate_body_booking()
        response = booker_api.post(Paths.BOOKING, data, cont_type=cont_type)
        booking_data = response.text

        check_response_status_code(response, 500)
        check_response_time(response)

        with allure.step(response_body_msg(booking_data)):
            assert booking_data == 'Internal Server Error', \
                f'Тело ответа, если Content-type: {cont_type}  - {booking_data}'

    @allure.story('Проверка заголовков')
    @allure.title('Accept: {accept}')
    @pytest.mark.parametrize('accept', ['application/javascript', 'text/html'])
    def test_post_with_invalid_accept(
            self, booker_api, check_response_status_code, response_body_msg,
            generate_body_booking, accept, check_response_time):
        """Тестовая функция для проверки создания бронирования с заголовком Content-type: text/plain.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param generate_body_booking: фикстура, создающая тело для запроса
        :param accept: значение заголовка Accept
        :param check_response_time: фикстура проверки времени ответа
        """
        data = generate_body_booking()
        response = booker_api.post(Paths.BOOKING, data, accept_header=accept)
        booking_data = response.text

        check_response_status_code(response, 418)
        check_response_time(response)

        with allure.step(response_body_msg(booking_data)):
            assert booking_data == "I'm a Teapot", \
                f'Тело ответа, если Accept: {accept}  - {booking_data}'
