"""Модуль с фикстурами."""

import allure
import base64
import jsonschema
import logging
import lxml
import pytest
import yaml
from io import StringIO
from dataclasses import asdict
from dicttoxml import dicttoxml
from jsonschema import validate
from lxml import etree
from lxml.etree import fromstring
from urllib.parse import unquote
from multidimensional_urlencode import urlencode


from helpers.clients import ApiClient
from helpers.data import BookingData, BookingDates
from helpers.urls_helper import Paths


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
def booker_api(get_host, get_schema, get_admin_login, get_admin_password, headers, logger_test):
    """Фикстура, создающая и возвращающая экземпляр класса ApiClient."""
    host = get_host
    schema = get_schema('https')
    login = get_admin_login
    passw = get_admin_password
    headers = headers
    logger_test.info(
        f'Инициализация экземпляра АПИ клиента: host {host}, '
        f'schema {schema}, login {login}, password {passw}, headers {headers}')
    return ApiClient(host, schema, login, passw, headers)


@pytest.fixture(scope='session')
def cfg():
    with open('helpers/config.yml', 'r', encoding='utf-8') as file:
        config = yaml.load(file, yaml.SafeLoader)
    return config


@pytest.fixture(scope='session')
def get_host(cfg):
    return cfg['host']['default']


@pytest.fixture(scope='session')
def get_schema(cfg):
    def _get_schema(sch):
        return cfg['schema'][sch]
    return _get_schema


@pytest.fixture(scope='session')
def get_admin_login(cfg):
    return cfg['admin']['login']


@pytest.fixture(scope='session')
def get_admin_password(cfg):
    return cfg['admin']['password']


@pytest.fixture(scope='session')
def encode_login_pass(get_admin_login, get_admin_password):
    """Кодирование логина и пароля в base64."""
    login = get_admin_login
    passw = get_admin_password
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
        if cont_type == 'xml':
            headers['Content-Type'] = 'text/xml'
        if cont_type == 'urlencoded':
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
        if accept == 'json':
            headers['Accept'] = 'application/json'
        if accept == 'xml':
            headers['Accept'] = 'application/xml'
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
            del_key=False, key_to_del=None):
        data = asdict(BookingData(
            firstname, lastname, totalprice, depositpaid, BookingDates(checkin, checkout), additionalneeds))
        if del_key:
            for i in key_to_del:
                data.pop(i)
        with allure.step(f'Тело запроса - {data}'):
            return data
    return _generate_body_booking


@pytest.fixture
@allure.step('Переконвертировать dict в xml')
def convert_dict_to_xml():
    """Фикстура конвертации dict в xml."""
    def _convert_dict_to_xml(d):
        xml = dicttoxml(d, custom_root='booking', attr_type=False)
        with allure.step(f'Тело запроса - {xml}'):
            return xml
    return _convert_dict_to_xml


@pytest.fixture
@allure.step('Переконвертировать dict в urlencoded')
def convert_dict_to_urlencoded():
    """Фикстура конвертации dict в urlencoded."""
    def _convert_dict_to_urlencoded(d):
        urlencode_d = urlencode(d)
        body = unquote(urlencode_d)
        with allure.step(f'Тело запроса - {body}'):
            return body
    return _convert_dict_to_urlencoded


@pytest.fixture
def create_test_booking(
        booker_api, generate_body_booking, convert_dict_to_xml, logger_test, parsing_xml_response):
    """Фикстура, создающая тестовую сущность и возвращающая ее тело."""
    @allure.step(
        'Создать тестовое бронирование: firstname={firstname}, lastname={lastname}, totalprice={totalprice}, '
        'depositpaid={depositpaid}, checkin={checkin}, checkout={checkout}, additionalneeds={additionalneeds}')
    def _create_test_booking(firstname='Susan', lastname='Brown', totalprice=1, depositpaid=True,
                             checkin='2018-01-01', checkout='2019-01-01', additionalneeds='Breakfast',
                             data_type='json'):
        data = generate_body_booking(
            firstname, lastname, totalprice, depositpaid, checkin, checkout, additionalneeds)
        if data_type == 'xml':
            data_xml = convert_dict_to_xml(data)
            logger_test.info(f'Создать тестовую бронь: data {data_xml}.')
            test_booking = booker_api.post(Paths.BOOKING, data, cont_type='xml', accept_header='xml')
            booking_data = test_booking.text
            tree = parsing_xml_response(booking_data)
            return tree
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
def validate_json(logger_test):
    """Фикстура валидации json схемы."""
    @allure.step('Провалидировать схему для тела ответа {json_data}')
    def _validate(json_data, base_schema):
        try:
            logger_test.info(f'Валидация схемы для тела {json_data}, схема: {base_schema}')
            validate(instance=json_data, schema=base_schema)
        except jsonschema.exceptions.ValidationError:
            return False
        return True
    return _validate


@pytest.fixture
def status_code_msg(logger_test):
    def _status_code_msg(code):
        logger_test.info(f'Проверить код ответа - {code}')
        return f'Проверить, что код ответа {code}'
    return _status_code_msg


@pytest.fixture
def response_body_msg(logger_test):
    def _response_body_msg(body):
        logger_test.info(f'Проверить тело ответа - {body}')
        return f'Проверить тело ответа - {body}'
    return _response_body_msg


@pytest.fixture
def get_params(request):
    return request.param


@pytest.fixture
def fixture_create_delete_booking_data(create_test_booking, delete_test_booking):
    """Фикстура создания дефолтной тестовой брони и ее удаления."""
    booking = create_test_booking()
    booking_id = booking['bookingid']
    booking_data = booking['booking']
    yield booking_id, booking_data
    delete_test_booking(booking_id)


@pytest.fixture
def parsing_xml_response():
    """Фикстура парсинга XML из строки."""
    def _parsing_xml_response(booking_data):
        try:
            tree = fromstring(booking_data)
        except lxml.etree.XMLSchemaParseError:
            return False
        return tree
    return _parsing_xml_response


@pytest.fixture
def get_text_of_element_xml_tree():
    """Фикстура получения текста элемента XML дерева."""
    def _get_text_of_element_xml_tree(parsing_xml_response, path):
        with allure.step(f'Получить элемент с xpath={path}'):
            element = parsing_xml_response.xpath(path).pop()
        return element.text
    return _get_text_of_element_xml_tree


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
            return xmlschema_parse.validate(data_parse)
        except lxml.etree.XMLSchemaParseError:
            return False
    return _validate
