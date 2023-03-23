"""Модуль с фикстурами."""

import allure
import jsonschema
import logging
import lxml
import pytest
import yaml
from io import StringIO
from dicttoxml import dicttoxml
from jsonschema import validate
from lxml import etree
from lxml.etree import fromstring


from helpers.clients import ApiClient
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
    logger_test.info(f'_____Start testing module {request.node.name}')
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
def headers():
    """Генерация заголовков запроса"""
    def _headers(method='get', token=None):
        headers = {'Accept': 'application/json'}
        if method == 'post':
            headers.update({'Content-Type': 'application/json'})
        if method == 'put' or method == 'patch' or method == 'delete':
            headers.update({'Content-Type': 'application/json', 'Cookie': f'token={token}'})
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
        data = {
                'firstname': firstname,
                'lastname': lastname,
                'totalprice': totalprice,
                'depositpaid': depositpaid,
                'bookingdates': {
                    'checkin': checkin,
                    'checkout': checkout
                },
                'additionalneeds': additionalneeds}
        if del_key:
            for i in key_to_del:
                data.pop(i)
        with allure.step(f'Тело запроса - {data}'):
            return data
    return _generate_body_booking


@pytest.fixture
@allure.step('Сгенерировать тело для запроса в xml')
def generate_body_booking_xml(generate_body_booking):
    """Фикстура, создающая и возвращающая тело для запроса в xml."""
    def _generate_body_booking_xml(
            firstname='Susan', lastname='Brown', totalprice=1, depositpaid=True,
            checkin='2018-01-01', checkout='2019-01-01', additionalneeds='Breakfast'):
        d = generate_body_booking(
            firstname, lastname, totalprice, depositpaid, checkin, checkout, additionalneeds)
        xml = dicttoxml(d, custom_root='booking', attr_type=False)
        with allure.step(f'Тело запроса - {xml}'):
            return xml
    return _generate_body_booking_xml


@pytest.fixture
def create_test_booking(booker_api, generate_body_booking, logger_test):
    """Фикстура, создающая тестовую сущность и возвращающая ее тело."""
    @allure.step(
        'Создать тестовое бронирование: firstname={firstname}, lastname={lastname}, totalprice={totalprice}, '
        'depositpaid={depositpaid}, checkin={checkin}, checkout={checkout}, additionalneeds={additionalneeds}')
    def _create_test_booking(firstname='Susan', lastname='Brown', totalprice=1, depositpaid=True,
                             checkin='2018-01-01', checkout='2019-01-01', additionalneeds='Breakfast'):
        data = generate_body_booking(
            firstname, lastname, totalprice, depositpaid, checkin, checkout, additionalneeds)
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
