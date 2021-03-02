"""Модуль с вспомогательными функциями для id и тела запросов."""

from typing import Dict, Any
import json
import requests


class TestDictForRequests:
    """Класс с методами, возвращающими словари с параметризованными значениями полей"""
    def __init__(self) -> None:
        """Конструктор класса. При инициализации создается словарь, у которого
        меняются значения полей в методах класса
        """
        self.data: Dict[str, Any] = {
            "firstname": "Susan",
            "lastname": "Brown",
            "totalprice": 1,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2018-01-01",
                "checkout": "2019-01-01"
            },
            "additionalneeds": "Breakfast"}

    def return_dict_with_firstname(self, param: Any) -> Dict[str, Any]:
        """Возвращает словарь с параметризованным значением для ключа firstname."""
        self.data["firstname"] = param
        return self.data

    def return_dict_with_lastname(self, param: Any) -> Dict[str, Any]:
        """Возвращает словарь с параметризованным значением для ключа lastname."""
        self.data["lastname"] = param
        return self.data

    def return_dict_with_totalprice(self, param: Any) -> Dict[str, Any]:
        """Возвращает словарь с параметризованным значением для ключа totalprice."""
        self.data["totalprice"] = param
        return self.data

    def return_dict_with_depositpaid(self, param: Any) -> Dict[str, Any]:
        """Возвращает словарь с параметризованным значением для ключа depositpaid."""
        self.data["depositpaid"] = param
        return self.data

    def return_dict_with_chekin(self, param: Any) -> Dict[str, Any]:
        """Возвращает словарь с параметризованным значением для ключа checkin."""
        self.data["bookingdates"]["checkin"] = param
        return self.data

    def return_dict_with_chekout(self, param: Any) -> Dict[str, Any]:
        """Возвращает словарь с параметризованным значением для ключа checkout."""
        self.data["bookingdates"]["checkout"] = param
        return self.data

    def return_dict_with_addneeds(self, param: Any) -> Dict[str, Any]:
        """Возвращает словарь с параметризованным значением для ключа additionalneeds."""
        self.data["additionalneeds"] = param
        return self.data

    def return_dict(self) -> Dict[str, Any]:
        """Возвращает словарь без параметризации значений ключей."""
        return self.data

    def return_dict_other(self) -> Dict[str, Any]:
        """Возвращает словарь без параметризации значений ключей."""
        self.data: Dict[str, Any] = {
            "firstname": "Anna",
            "lastname": "Chapman",
            "totalprice": 100,
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2014-03-01",
                "checkout": "2015-04-01"
            },
            "additionalneeds": "no"}
        return self.data


def create_test_entity(booker_api) -> str:
    """Создает тестовую сущность и возвращает ее id."""
    data: Dict[str, Any] = TestDictForRequests().return_dict_other()
    ent: requests.models.Response = booker_api.post(data=json.dumps(data))
    id_to_do_request: str = ent.json()['bookingid']
    return id_to_do_request
