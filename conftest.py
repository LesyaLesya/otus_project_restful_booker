"""Модуль с фикстурами."""

import allure
import base64
import jsonschema
import logging
import pytest
import yaml
from io import StringIO
from jsonschema import validate
from lxml import etree

from helpers.base_functions import (
    convert_dict_to_urlencoded, convert_dict_to_xml, get_xml_response_data)
from helpers.clients import ApiClient
from helpers.data import BookingData, BookingDates
from helpers.urls_helper import Paths


def pytest_addoption(parser):
    parser.addoption('--schema', action='store', default='https', choices=['https', 'http'])
    parser.addoption('--host', action='store', default='default')
    parser.addoption('--user', action='store', default='admin')


@pytest.fixture(scope='session')
def parser_schema(request):
    return request.config.getoption('--schema')


@pytest.fixture(scope='session')
def parser_host(request):
    return request.config.getoption('--host')


@pytest.fixture(scope='session')
def parser_user(request):
    return request.config.getoption('--user')


@pytest.fixture(scope='session', autouse=True)
def logger_test():
    logger = logging.getLogger('testing')
    return logger


@pytest.fixture(autouse=True)
def log_test_description(request, logger_test):
    logger_test.info(f'___Test "{request.node.nodeid}" START')
    yield
    logger_test.info(f'___Test "{request.node.nodeid}" COMPLETE')


@pytest.fixture(scope='module', autouse=True)
def log_module_description(request, logger_test):
    logger_test.info(f'_____START testing module {request.node.name}')
    yield
    logger_test.info(f'_____STOP testing module {request.node.name}')


@pytest.fixture(scope='session')
def booker_api(get_host, get_schema, get_login, get_password, headers, logger_test, parser_user):
    """Фикстура, создающая и возвращающая экземпляр класса ApiClient."""
    host = get_host
    schema = get_schema
    login = get_login
    passw = get_password
    header = headers
    user = parser_user
    logger_test.info(
        f'Инициализация экземпляра АПИ клиента: host {host}, '
        f'schema {schema}, user {user}, login {login}, password {passw}, headers {header}')
    return ApiClient(host, schema, header, user, get_login, get_password)


@pytest.fixture(scope='session')
def cfg():
    with open('config.yml', 'r', encoding='utf-8') as file:
        config = yaml.load(file, yaml.SafeLoader)
    return config


@pytest.fixture(scope='session')
def get_host(cfg, parser_host):
    return cfg['host'][parser_host]


@pytest.fixture(scope='session')
def get_schema(cfg, parser_schema):
    return cfg['schema'][parser_schema]


@pytest.fixture(scope='session')
def get_login(cfg, parser_user):
    return cfg['users'][parser_user]['login']


@pytest.fixture(scope='session')
def get_password(cfg, parser_user):
    return cfg['users'][parser_user]['password']


@pytest.fixture(scope='session')
def encode_login_pass(get_login, get_password):
    """Кодирование логина и пароля в base64."""
    login = get_login
    passw = get_password
    for_token = f'{login}:{passw}'
    sample_string_bytes = for_token.encode('ascii')
    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode('ascii')
    return base64_string


@pytest.fixture(scope='session')
def headers(encode_login_pass):
    """Генерация заголовков запроса"""
    def _headers(cont_type=None, accept=None, auth_type=None, token=None):
        headers = {}
        if cont_type == 'json':
            headers['Content-Type'] = 'application/json'
        elif cont_type == 'xml':
            headers['Content-Type'] = 'text/xml'
        elif cont_type == 'urlencoded':
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
        elif cont_type is None:
            pass
        else:
            headers['Content-Type'] = cont_type

        if accept == 'json':
            headers['Accept'] = 'application/json'
        elif accept == 'xml':
            headers['Accept'] = 'application/xml'
        elif accept is None:
            pass
        else:
            headers['Accept'] = accept

        if auth_type == 'cookie':
            headers['Cookie'] = f'token={token}'
        if auth_type == 'basic_auth':
            headers['Authorization'] = f'Basic {encode_login_pass}'
        return headers
    return _headers


@pytest.fixture
@allure.step('Сгенерировать тело для запроса')
def generate_body_booking():
    """Фикстура, создающая и возвращающая тело для запроса."""
    def _generate_body_booking(
            firstname='Susan', lastname='Brown', totalprice=1, depositpaid=True,
            checkin='2018-01-01', checkout='2019-01-01', additionalneeds='Breakfast',
            convert=None):
        data = BookingData(
            firstname=firstname, lastname=lastname, totalprice=totalprice,
            depositpaid=depositpaid,
            bookingdates=BookingDates(checkin=checkin, checkout=checkout),
            additionalneeds=additionalneeds)
        d = data.model_dump(exclude_none=True)
        if convert == 'xml':
            x = convert_dict_to_xml(d)
            with allure.step(f'Тело запроса - {x}'):
                return x, d
        if convert == 'urlencoded':
            u = convert_dict_to_urlencoded(d)
            with allure.step(f'Тело запроса - {u}'):
                return u, d
        with allure.step(f'Тело запроса - {d}'):
            return d
    return _generate_body_booking


@pytest.fixture
def create_test_booking(
        booker_api, generate_body_booking, logger_test):
    """Фикстура, создающая тестовую сущность и возвращающая ее тело."""
    @allure.step(
        'Создать тестовое бронирование: firstname={firstname}, lastname={lastname}, totalprice={totalprice}, '
        'depositpaid={depositpaid}, checkin={checkin}, checkout={checkout}, additionalneeds={additionalneeds}')
    def _create_test_booking(firstname='Susan', lastname='Brown', totalprice=1, depositpaid=True,
                             checkin='2018-01-01', checkout='2019-01-01', additionalneeds='Breakfast',
                             data_type='json', *args):
        data = generate_body_booking(
            firstname, lastname, totalprice, depositpaid, checkin, checkout, additionalneeds)
        if data_type == 'xml':
            data_xml = convert_dict_to_xml(data)
            logger_test.info(f'Создать тестовую бронь: data {data_xml}.')
            test_booking = booker_api.post(Paths.BOOKING, data, cont_type='xml', accept_header='xml')
            booking_data = test_booking.text
            elements = get_xml_response_data(booking_data, args)
            return elements
        else:
            logger_test.info(f'Создать тестовую бронь: data {data}.')
            test_booking = booker_api.post(Paths.BOOKING, data)
            test_booking_data = test_booking.json()
            return test_booking_data
    return _create_test_booking


@pytest.fixture
def delete_test_booking(booker_api, logger_test):
    """Фикстура, удаляющая тестовую сущность.
    :param booker_api: id брони для удаления
    """
    @allure.step('Удалить бронь с id {booking_id}')
    def _delete_test_booking(booking_id):
        logger_test.info(f'Удалить тестовую бронь {booking_id}')
        return booker_api.delete(f'{Paths.BOOKING}{booking_id}')
    return _delete_test_booking


@pytest.fixture
def get_params(request):
    return request.param


@pytest.fixture
def fixture_create_delete_booking_data(create_test_booking, delete_test_booking, request):
    """Фикстура создания дефолтной тестовой брони и ее удаления."""
    def _create_delete(
            firstname='Susan', lastname='Brown', totalprice=1, depositpaid=True,
            checkin='2018-01-01', checkout='2019-01-01', additionalneeds='Breakfast'):
        booking = create_test_booking(
            firstname, lastname, totalprice, depositpaid, checkin, checkout, additionalneeds)
        booking_id = booking['bookingid']
        booking_data = booking['booking']

        def teardown():
            delete_test_booking(booking_id)
        request.addfinalizer(teardown)
        return booking_id, booking_data
    return _create_delete


@pytest.fixture
def validate_json(logger_test):
    """Фикстура валидации json схемы."""
    @allure.step('Провалидировать схему для тела ответа {json_data}')
    def _validate(json_data, base_schema):
        try:
            schema = base_schema.model_json_schema()
            logger_test.info(f'Валидация схемы для тела {json_data}, схема: {schema}')
            validate(instance=json_data, schema=schema)
        except jsonschema.exceptions.ValidationError:
            assert False
        assert True
    return _validate


@pytest.fixture
def check_response_status_code(logger_test):
    """Фикстура проверки кода ответа."""
    @allure.step('Проверить, что код ответа {code}')
    def _check_response_status_code(response, code):
        logger_test.info(f'Проверка кода ответа {response}, ОР код: {code}')
        assert response.status_code == code, f'Код ответа {response.status_code}, ОР {code}'
    return _check_response_status_code


@pytest.fixture
def response_body_msg(logger_test):
    def _response_body_msg(body):
        logger_test.info(f'Проверить тело ответа - {body}')
        return f'Проверить тело ответа - {body}'
    return _response_body_msg


@pytest.fixture
def validate_xml(logger_test):
    """Фикстура валидации xml схемы."""
    @allure.step('Провалидировать xml схему для тела ответа {data}')
    def _validate(data, schema):
        try:
            logger_test.info(f'Валидация схемы для тела {data}, схема: {schema}')
            xmlschema = etree.parse(StringIO(schema))
            xmlschema_parse = etree.XMLSchema(xmlschema)

            data_parse = etree.parse(StringIO(data))
            assert xmlschema_parse.validate(data_parse)
        except etree.XMLSchemaParseError:
            assert False
    return _validate


@pytest.fixture
def check_response_time(logger_test):
    """Фикстура проверки времени ответа."""
    @allure.step('Проверить, что время ответа меньше {tims_ms} ms')
    def _check_response_time(response, tims_ms=400):
        actual_time = response.elapsed.total_seconds() * 1000
        logger_test.info(f'Проверить время ответа - {actual_time}')
        assert actual_time < tims_ms, f'Время ответа {actual_time}, ОР {tims_ms} ms'
    return _check_response_time
