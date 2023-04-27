"""Модуль с тестами post запросов - CreateBooking."""

import allure
import pytest

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
    booking_data = response.json()
    booking_id = booking_data['bookingid']
    yield response, booking_data, booking_id
    delete_test_booking(booking_id)


@pytest.fixture
def fixture_post_booking_deposit(booker_api, generate_body_booking, delete_test_booking, get_params):
    data = generate_body_booking(depositpaid=get_params)
    response = booker_api.post(Paths.BOOKING, data)
    booking_data = response.json()
    booking_id = booking_data['bookingid']
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
        booker_api, generate_body_booking, delete_test_booking, get_params,
        parsing_xml_response, get_text_of_element_xml_tree, convert_dict_to_xml):
    data = generate_body_booking(firstname=get_params)
    data_xml = convert_dict_to_xml(data)
    response = booker_api.post(Paths.BOOKING, data_xml, cont_type='xml', accept_header='xml')
    booking_data = response.text
    tree = parsing_xml_response(booking_data)
    booking_id = get_text_of_element_xml_tree(tree, 'bookingid')
    yield response, booking_data, booking_id, tree
    delete_test_booking(booking_id)


@pytest.mark.create_booking
@allure.feature('POST - CreateBooking')
class TestCreateBooking:
    """Тесты метода post /booking."""

    @allure.story('Проверка firstname')
    @allure.title('Валидные значения firstname - {get_params}')
    @pytest.mark.parametrize('get_params', ['Peter', 'Maria-Elena', 'Имя Имя', ''])
    def test_post_valid_firstname(
            self, fixture_post_booking_firstname, validate_json, status_code_msg,
            response_body_msg, get_params):
        """Тестовая функция для проверки создания бронирования с валидным именем.

        :param fixture_post_booking_firstname: фикстура создания и удаления тестовых данных и отправки запроса
        :param validate_json: фикстура для валидации JSON схемы
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        """
        response, booking_data, booking_id = fixture_post_booking_firstname

        with allure.step(status_code_msg(200)):
            assert response.status_code == 200, f'Код ответа - {response.status_code}'

        assert validate_json(booking_data, CREATE_BOOKING_SCHEMA)

        with allure.step(response_body_msg(booking_data)):
            assert booking_data['booking']['firstname'] == get_params, \
                f'Имя - {booking_data["booking"]["firstname"]}'

    @allure.story('Проверка firstname')
    @allure.title('Невалидные значения firstname - {value}')
    @pytest.mark.parametrize('value', [123, True, None])
    def test_post_invalid_firstname(
            self, booker_api, value, generate_body_booking, status_code_msg, response_body_msg):
        """Тестовая функция для проверки создания бронирования с невалидным именем.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param value: передаваемые в теле запроса варианты для "firstname"
        :param generate_body_booking: фикстура, создающая тело для запроса
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        """
        data = generate_body_booking(firstname=value)
        response = booker_api.post(Paths.BOOKING, data)
        response_body = response.text

        with allure.step(status_code_msg(500)):
            assert response.status_code == 500, f'Код ответа - {response.status_code}'

        with allure.step(response_body_msg(response_body)):
            assert response_body == 'Internal Server Error', f'Тело ответа  - {response_body}'

    @allure.story('Проверка firstname')
    @allure.title('Не передавать в теле firstname')
    def test_post_without_firstname(self, booker_api, generate_body_booking, status_code_msg, response_body_msg):
        """Тестовая функция для проверки создания бронирования без имени.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param generate_body_booking: фикстура, создающая тело для запроса
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        """
        data = generate_body_booking(del_key=True, key_to_del=['firstname'])
        response = booker_api.post(Paths.BOOKING, data)
        response_body = response.text

        with allure.step(status_code_msg(500)):
            assert response.status_code == 500, f'Код ответа - {response.status_code}'

        with allure.step(response_body_msg(response_body)):
            assert response_body == 'Internal Server Error', f'Тело ответа  - {response_body}'

    @allure.story('Проверка lastname')
    @allure.title('Валидные значения lastname - {get_params}')
    @pytest.mark.parametrize('get_params', ['Иванов', 'Black', 'W', 'Last-name', ''])
    def test_post_valid_lastname(
            self, validate_json, status_code_msg, response_body_msg, fixture_post_booking_lastname, get_params):
        """Тестовая функция для проверки создания бронирования с валидной фамилией.

        :param fixture_post_booking_lastname: фикстура создания и удаления тестовых данных и отправки запроса
        :param validate_json: фикстура для валидации JSON схемы
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        """
        response, booking_data, booking_id = fixture_post_booking_lastname

        with allure.step(status_code_msg(200)):
            assert response.status_code == 200, f'Код ответа - {response.status_code}'

        assert validate_json(booking_data, CREATE_BOOKING_SCHEMA)

        with allure.step(response_body_msg(booking_data)):
            assert booking_data['booking']['lastname'] == get_params, \
                f'Фамилия - {booking_data["booking"]["lastname"]}'

    @allure.story('Проверка lastname')
    @allure.title('Не передавать в теле lastname')
    def test_post_without_lastname(
            self, booker_api, generate_body_booking, status_code_msg, response_body_msg):
        """Тестовая функция для проверки создания бронирования без фамилии.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param generate_body_booking: фикстура, создающая тело для запроса
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        """
        data = generate_body_booking(del_key=True, key_to_del=['lastname'])
        response = booker_api.post(Paths.BOOKING, data)
        response_body = response.text

        with allure.step(status_code_msg(500)):
            assert response.status_code == 500, f'Код ответа - {response.status_code}'

        with allure.step(response_body_msg(response_body)):
            assert response_body == 'Internal Server Error', f'Тело ответа  - {response_body}'

    @allure.story('Проверка totalprice')
    @allure.title('Валидные значения totalprice - {get_params}')
    @pytest.mark.parametrize('get_params', [123, 1, 566778])
    def test_post_valid_totalprice(
            self, fixture_post_booking_totalprice,
            validate_json, status_code_msg, response_body_msg, get_params):
        """Тестовая функция для проверки создания бронирования с валидной ценой.

        :param fixture_post_booking_totalprice: фикстура создания и удаления тестовых данных и отправки запроса
        :param validate_json: фикстура для валидации JSON схемы
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        """
        response, booking_data, booking_id = fixture_post_booking_totalprice

        with allure.step(status_code_msg(200)):
            assert response.status_code == 200, f'Код ответа - {response.status_code}'

        assert validate_json(booking_data, CREATE_BOOKING_SCHEMA)

        with allure.step(response_body_msg(booking_data)):
            assert booking_data['booking']['totalprice'] == get_params, \
                f'Общая сумма - {response.json()["booking"]["totalprice"]}'

    @allure.story('Проверка depositpaid')
    @allure.title('Валидные значения depositpaid - {get_params}')
    @pytest.mark.parametrize('get_params', [True, False])
    def test_post_valid_depositpaid(
            self, validate_json, status_code_msg, response_body_msg,
            fixture_post_booking_deposit, get_params):
        """Тестовая функция для проверки создания бронирования с валидным depositpaid.

        :param fixture_post_booking_deposit:  фикстура создания и удаления тестовых данных и отправки запроса
        :param validate_json: фикстура для валидации JSON схемы
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        """
        response, booking_data, booking_id = fixture_post_booking_deposit

        with allure.step(status_code_msg(200)):
            assert response.status_code == 200, f'Код ответа - {response.status_code}'

        assert validate_json(booking_data, CREATE_BOOKING_SCHEMA)

        with allure.step(response_body_msg(booking_data)):
            assert booking_data['booking']['depositpaid'] == get_params, \
                f'Статус внесения депозита - {booking_data["booking"]["depositpaid"]}'

    @allure.story('Проверка checkin')
    @allure.title('Валидные значения checkin - {get_params}')
    @pytest.mark.parametrize('get_params', ['1900-11-11', '2021-02-11', '2030-06-01'])
    def test_post_valid_checkin(
            self, validate_json, status_code_msg, response_body_msg,
            fixture_post_booking_checkin, get_params):
        """Тестовая функция для проверки создания бронирования с валидным checkin.

        :param fixture_post_booking_checkin: фикстура создания и удаления тестовых данных и отправки запроса
        :param validate_json: фикстура для валидации JSON схемы
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        """
        response, booking_data, booking_id = fixture_post_booking_checkin

        with allure.step(status_code_msg(200)):
            assert response.status_code == 200, f'Код ответа - {response.status_code}'

        assert validate_json(booking_data, CREATE_BOOKING_SCHEMA)

        with allure.step(response_body_msg(booking_data)):
            assert booking_data['booking']['bookingdates']['checkin'] == get_params, \
                f'Дата заезда - {booking_data["booking"]["bookingdates"]["checkin"]}'

    @allure.story('Проверка checkin')
    @allure.title('Невалидные значения checkin - {get_params}')
    @pytest.mark.parametrize('get_params', ['00-00-00', 'tests', ' '])
    def test_post_invalid_checkin(
            self, validate_json, status_code_msg, response_body_msg,
            fixture_post_booking_checkin, get_params):
        """Тестовая функция для проверки создания бронирования с невалидным checkin.

        :param fixture_post_booking_checkin: фикстура создания и удаления тестовых данных и отправки запроса
        :param validate_json: фикстура для валидации JSON схемы
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        """
        response, booking_data, booking_id = fixture_post_booking_checkin

        with allure.step(status_code_msg(200)):
            assert response.status_code == 200, f'Код ответа - {response.status_code}'

        assert validate_json(booking_data, CREATE_BOOKING_SCHEMA)

        with allure.step(response_body_msg(booking_data)):
            assert booking_data['booking']['bookingdates']['checkin'] == '0NaN-aN-aN', \
                f'Дата заезда - {booking_data["booking"]["bookingdates"]["checkin"]}'

    @allure.story('Проверка checkout')
    @allure.title('Валидные значения checkout - {get_params}')
    @pytest.mark.parametrize('get_params', ['1871-01-01', '2021-02-11', '2041-12-31'])
    def test_post_valid_checkout(
            self, validate_json, status_code_msg, response_body_msg,
            fixture_post_booking_checkout, get_params):
        """Тестовая функция для проверки создания бронирования с валидным checkout.

        :param fixture_post_booking_checkout: фикстура создания и удаления тестовых данных и отправки запроса
        :param validate_json: фикстура для валидации JSON схемы
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        """
        response, booking_data, booking_id = fixture_post_booking_checkout

        with allure.step(status_code_msg(200)):
            assert response.status_code == 200, f'Код ответа - {response.status_code}'

        assert validate_json(booking_data, CREATE_BOOKING_SCHEMA)

        with allure.step(response_body_msg(booking_data)):
            assert booking_data['booking']['bookingdates']['checkout'] == get_params, \
                f'Дата выезда - {booking_data["booking"]["bookingdates"]["checkout"]}'

    @allure.story('Проверка additionalneeds')
    @allure.title('Валидные значения additionalneeds - {get_params}')
    @pytest.mark.parametrize('get_params', ['что-то', 'dinner, breakfast', ''])
    def test_post_valid_additionalneeds(
            self, validate_json, status_code_msg, response_body_msg,
            fixture_post_booking_additionalneeds, get_params):
        """Тестовая функция для проверки создания бронирования с валидным additionalneeds.

        :param fixture_post_booking_additionalneeds: фикстура создания и удаления тестовых данных и отправки запроса
        :param validate_json: фикстура для валидации JSON схемы
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        """
        response, booking_data, booking_id = fixture_post_booking_additionalneeds

        with allure.step(status_code_msg(200)):
            assert response.status_code == 200, f'Код ответа - {response.status_code}'

        assert validate_json(booking_data, CREATE_BOOKING_SCHEMA)

        with allure.step(response_body_msg(booking_data)):
            assert booking_data['booking']['additionalneeds'] == get_params, \
                f'Дополнительные пожелания - {booking_data["booking"]["additionalneeds"]}'

    @allure.title('Пустое тело запроса')
    def test_post_empty_body(self, booker_api, status_code_msg, response_body_msg):
        """Тестовая функция для проверки создания бронирования с пустым телом.

        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        """
        response = booker_api.post(Paths.BOOKING, {})
        response_body = response.text

        with allure.step(status_code_msg(500)):
            assert response.status_code == 500, f'Код ответа - {response.status_code}'

        with allure.step(response_body_msg(response_body)):
            assert response_body == 'Internal Server Error', f'Тело ответа  - {response_body}'

    @allure.title('Повторное создание бронирования')
    def test_post_repeat_create_booking(
            self, validate_json, status_code_msg, response_body_msg, fixture_post_booking_repeat):
        """Тестовая функция для проверки повторного создания бронирования.

        :param fixture_post_booking_repeat: фикстура создания и удаления тестовых данных и отправки запроса
        :param validate_json: фикстура для валидации JSON схемы
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        """
        data, response_first, response_repeat = fixture_post_booking_repeat
        response_body_first = response_first.json()
        response_body_repeat = response_repeat.json()

        with allure.step(status_code_msg(200)):
            assert response_first.status_code == 200, f'Код ответа - {response_first.status_code}'

        with allure.step(status_code_msg(200)):
            assert response_repeat.status_code == 200, f'Код ответа - {response_repeat.status_code}'

        assert validate_json(response_body_first, CREATE_BOOKING_SCHEMA)
        assert validate_json(response_body_repeat, CREATE_BOOKING_SCHEMA)

        with allure.step(response_body_msg(response_body_repeat)):
            assert response_body_repeat['booking'] == data, f'Тело ответа  - {response_body_repeat}'

    @allure.story('Проверка firstname')
    @allure.title('Валидные значения firstname - запрос в xml')
    @pytest.mark.parametrize('get_params', ['Peter', 'Maria', '', 'имя'])
    def test_post_valid_firstname_xml(
            self, fixture_post_booking_firstname_xml, status_code_msg, response_body_msg,
            get_params, validate_xml, get_text_of_element_xml_tree):
        """Тестовая функция для проверки создания бронирования с валидным именем.

        :param fixture_post_booking_firstname_xml: фикстура создания и удаления тестовых данных и отправки запроса (xml)
        :param validate_xml: фикстура валидации xml схемы
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param get_text_of_element_xml_tree: фикстура получения текста элемента XML дерева
        """

        response, booking_data, booking_id, tree = fixture_post_booking_firstname_xml

        with allure.step(status_code_msg(200)):
            assert response.status_code == 200, f'Код ответа - {response.status_code}'

        assert validate_xml(booking_data, CREATE_BOOKING_SCHEMA_XSD)

        with allure.step(response_body_msg(booking_data)):
            firstname = get_text_of_element_xml_tree(tree, 'booking/firstname')
            if get_params == '':
                assert firstname is None, f'Имя - {firstname}'
            else:
                assert firstname == get_params, f'Имя - {firstname}'

    @allure.story('Проверка заголовков')
    @allure.title('Content-type: text/plain')
    def test_post_with_content_type_text_plain(
            self, booker_api, status_code_msg, response_body_msg, generate_body_booking):
        """Тестовая функция для проверки создания бронирования с заголовком Content-type: text/plain.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param generate_body_booking: фикстура, создающая тело для запроса
        """
        data = generate_body_booking()
        response = booker_api.post(Paths.BOOKING, data, headers_new={'Content-type': 'text/plain'})
        booking_data = response.text

        with allure.step(status_code_msg(500)):
            assert response.status_code == 500, f'Код ответа - {response.status_code}'

        with allure.step(response_body_msg(booking_data)):
            assert booking_data == 'Internal Server Error', \
                f'Тело ответа, если Content-type: text/plain  - {booking_data}'
