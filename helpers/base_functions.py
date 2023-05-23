"""Модуль с общими вспомогательными функциями."""

import allure
import lxml
import urllib

from dicttoxml import dicttoxml
from lxml.etree import fromstring
from multidimensional_urlencode import urlencode
from urllib.parse import unquote


@allure.step('Переконвертировать dict в xml')
def convert_dict_to_xml(d):
    """Конвертация dict в xml."""
    xml = dicttoxml(d, custom_root='booking', attr_type=False)
    with allure.step(f'Тело запроса - {xml}'):
        return xml


@allure.step('Переконвертировать dict в urlencoded')
def convert_dict_to_urlencoded(d):
    """Конвертация dict в urlencoded."""
    for k, j in d.items():
        if isinstance(j, str):
            d[k] = urllib.parse.quote(j.encode('utf-8'))
    urlencode_d = urlencode(d)
    body = unquote(urlencode_d)
    with allure.step(f'Тело запроса - {body}'):
        return body


def get_xml_response_data(booking_data, *args):
    """Получение текста элемента XML дерева."""
    try:
        tree = fromstring(booking_data)
    except lxml.etree.XMLSchemaParseError:
        return False
    elements = []
    for i in args:
        with allure.step(f'Получить элемент с xpath={i}'):
            element = tree.xpath(i).pop()
            elements.append(element.text)
    return elements
