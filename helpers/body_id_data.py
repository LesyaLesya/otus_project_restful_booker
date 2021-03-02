"""Модуль с вспомогательными функциями для id и тела запросов."""

from typing import Dict, Any
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


def get_id_of_entity(booker_api, idx: int) -> str:
    """Возвращает id сущности по переданному в параметрах индексу."""
    get_all_ids: requests.models.Response = booker_api.get()
    id_to_do_request: str = get_all_ids.json()[idx]['bookingid']
    return id_to_do_request
