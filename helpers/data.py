""" Модуль для генерации данных для запросов. """


from typing import Any
from pydantic import BaseModel


class BookingDates(BaseModel):
    checkin: Any = None
    checkout: Any = None


class BookingData(BaseModel):
    firstname: Any = None
    lastname: Any = None
    totalprice: Any = None
    depositpaid: Any = None
    bookingdates: BookingDates = None
    additionalneeds: Any = None
