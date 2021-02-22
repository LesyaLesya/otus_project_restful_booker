""" Модуль с вспомогательными функциями. """


from typing import Dict, Any


def return_dict_with_firstname(param: Any) -> Dict[str, Any]:
    """
    Функция, возвращающая словарь с параметризованным
    значением для ключа firstname.

    """
    data: Dict[str, Any] = {
        "firstname": param,
        "lastname": "Brown",
        "totalprice": 1,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2018-01-01",
            "checkout": "2019-01-01"
        },
        "additionalneeds": "Breakfast"}
    return data


def return_dict_with_lastname(param: Any) -> Dict[str, Any]:
    """
    Функция, возвращающая словарь с параметризованным
    значением для ключа lastname.

    """
    data: Dict[str, Any] = {
        "firstname": "Sam",
        "lastname": param,
        "totalprice": 111,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2000-03-11",
            "checkout": "2019-02-02"
        },
        "additionalneeds": "Breakfast"}
    return data


def return_dict_with_totalprice(param: Any) -> Dict[str, Any]:
    """
    Функция, возвращающая словарь с параметризованным
    значением для ключа totalprice.

    """
    data: Dict[str, Any] = {
        "firstname": "Sam",
        "lastname": "Jackson",
        "totalprice": param,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2015-12-30",
            "checkout": "2015-12-31"
        },
        "additionalneeds": "Breakfast"}
    return data


def return_dict_with_depositpaid(param: Any) -> Dict[str, Any]:
    """
    Функция, возвращающая словарь с параметризованным
    значением для ключа depositpaid.

    """
    data: Dict[str, Any] = {
        "firstname": "Sam",
        "lastname": "Jackson",
        "totalprice": 4000,
        "depositpaid": param,
        "bookingdates": {
            "checkin": "2011-01-01",
            "checkout": "2012-01-01"
        },
        "additionalneeds": "Breakfast"}
    return data


def return_dict_with_chekin(param: Any) -> Dict[str, Any]:
    """
    Функция, возвращающая словарь с параметризованным
    значением для ключа checkin.

    """
    data: Dict[str, Any] = {
        "firstname": "Sam",
        "lastname": "Jackson",
        "totalprice": 5,
        "depositpaid": False,
        "bookingdates": {
            "checkin": param,
            "checkout": "2019-01-01"
        },
        "additionalneeds": "Breakfast"}
    return data


def return_dict_with_chekout(param: Any) -> Dict[str, Any]:
    """
    Функция, возвращающая словарь с параметризованным
    значением для ключа checkout.

    """
    data: Dict[str, Any] = {
        "firstname": "Sam",
        "lastname": "Jackson",
        "totalprice": 123,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2019-01-01",
            "checkout": param
        },
        "additionalneeds": "Breakfast"}
    return data


def return_dict_with_addneeds(param: Any) -> Dict[str, Any]:
    """
    Функция, возвращающая словарь с параметризованным
    значением для ключа additionalneeds.

    """
    data: Dict[str, Any] = {
        "firstname": "Sam",
        "lastname": "Jackson",
        "totalprice": 123,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2018-01-01",
            "checkout": "2019-01-01"
        },
        "additionalneeds": param}
    return data


def return_dict() -> Dict[str, Any]:
    """
    Функция, возвращающая словарь для использования в запросах
    без параметризации значений ключей.

    """
    data: Dict[str, Any] = {
        "firstname": "Leena",
        "lastname": "White",
        "totalprice": 1000,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2021-01-01",
            "checkout": "2023-12-01"
        },
        "additionalneeds": "Nothing"}
    return data
