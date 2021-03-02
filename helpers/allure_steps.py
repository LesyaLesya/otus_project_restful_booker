"""Модуль с вспомогательными функциями для allure шагов."""

from typing import Union, Dict


def check_200_status_code() -> str:
    """Возвращает строку с указанием, какой код ответа проверяем."""
    return "Проверяем, что код ответа 200"


def check_500_status_code() -> str:
    """Возвращает строку с указанием, какой код ответа проверяем."""
    return "Проверяем, что код ответа 500"


def check_405_status_code() -> str:
    """Возвращает строку с указанием, какой код ответа проверяем."""
    return "Проверяем, что код ответа 405"


def check_201_status_code() -> str:
    """Возвращает строку с указанием, какой код ответа проверяем."""
    return "Проверяем, что код ответа 201"


def check_404_status_code() -> str:
    """Возвращает строку с указанием, какой код ответа проверяем."""
    return "Проверяем, что код ответа 404"


def check_400_status_code() -> str:
    """Возвращает строку с указанием, какой код ответа проверяем."""
    return "Проверяем, что код ответа 400"


def create_test_entity() -> str:
    """Возвращает строку о создании тестовой сущности."""
    return "Создаем тестовую сущность и получаем ее id"


def send_delete_request(param: Union[int, str]) -> str:
    """Возвращает строку об отправке delete запроса к id"""
    return f"Отправляем delete запрос с id {param}"


def send_get_request(param: Union[int, str]) -> str:
    """Возвращает строку об отправке get запроса к id"""
    return f"Отправляем get запрос с id {param}"


def send_get_request_with_param(param: Dict[str, str]) -> str:
    """Возвращает строку об отправке get запроса с параметром"""
    return f"Отправляем get запрос с параметром -  {param}"


def send_patch_request(data: Dict[str, str], bid) -> str:
    """Возвращает строку об отправке patch запроса с параметрами"""
    return f"Отправляем patch запрос с data - {data} и id {bid}"


def send_put_request(data: Dict[str, str], bid) -> str:
    """Возвращает строку об отправке put запроса с параметрами"""
    return f"Отправляем put запрос с телом - {data} и id {bid}"


def check_firstname(param: str) -> str:
    """Возвращает строку с указанием, какой параметр проверяем."""
    return f"Проверяем, что firstname - '{param}'"


def check_lastname(param: str) -> str:
    """Возвращает строку с указанием, какой параметр проверяем."""
    return f"Проверяем, что lastname - '{param}'"


def check_totalprice(param: int) -> str:
    """Возвращает строку с указанием, какой параметр проверяем."""
    return f"Проверяем, что totalprice - '{param}'"


def check_depositpaid(param: bool) -> str:
    """Возвращает строку с указанием, какой параметр проверяем."""
    return f"Проверяем, что depositpaid - '{param}'"


def check_checkin(param: str) -> str:
    """Возвращает строку с указанием, какой параметр проверяем."""
    return f"Проверяем, что checkin - '{param}'"


def check_checkout(param: str) -> str:
    """Возвращает строку с указанием, какой параметр проверяем."""
    return f"Проверяем, что checkout - '{param}'"


def check_addneeds(param: str) -> str:
    """Возвращает строку с указанием, какой параметр проверяем."""
    return f"Проверяем, что additionalneeds - '{param}'"
