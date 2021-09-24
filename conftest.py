"""Модуль с фикстурами."""

import json
import pytest
import requests
import allure


def pytest_addoption(parser):
    """Получение аргументов из командной строки."""
    parser.addoption(
        "--url",
        action="store",
        default="https://restful-booker.herokuapp.com",
        help="Enter url")
    parser.addoption(
        "--login",
        action="store",
        required=True,
        help="Enter login")
    parser.addoption(
        "--passw",
        action="store",
        required=True,
        help="Enter password")


class ApiClient:
    """Класс для выполнения запросов к API."""

    @allure.step("Создание экземпляра класса ApiClient")
    def __init__(self, host, login, passw):
        """Конструктор класса.
        При инициализации также создается объект requests.Session(),
        вызывается приватный метод для получения auth token.

        :param host: адрес хоста
        :param login: логин для получения auth token
        :param passw: пароль для получения auth token
        """

        self.host = host
        self.__login = login
        self.__passw = passw
        self.session = requests.Session()
        self.__get_token()

    @allure.step("Получение auth токена")
    def __get_token(self):
        """Метод передачи в запросе учетных данных и получения auth token."""

        payload = {"username": self.__login, "password": self.__passw}
        with allure.step(f"Выполнение post запроса с данными {payload}"):
            response = self.session.post(url=f"{self.host}/auth", data=payload)
        self.__token = json.loads(response.text)["token"]
        with allure.step(f"Получение токена - {self.__token}"):
            return self.__token

    @allure.step("Выполнение get запроса")
    def get(self, path="", params=None):
        """Возвращает вызов get запроса к API.

        :param path: адрес хоста
        :param params: параметры, передаваемые в урле
        """

        url = f"{self.host}/booking/{path}"
        return self.session.get(url=url, params=params)

    @allure.step("Выполнение post запроса")
    def post(self, data=None):
        """Возвращает вызов post запроса к API.

        :param data: передаваемое тело запроса
        """

        url = f"{self.host}/booking"
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        return self.session.post(url=url, headers=headers, data=data)

    @allure.step("Выполнение patch запроса")
    def patch(self, path, data=None):
        """Возвращает вызов patch запроса к API.
        Требует передачу в заголовке Cookie auth token.

        :param path: адрес хоста
        :param data: передаваемое тело запроса
        """

        url = f"{self.host}/booking/{path}"
        headers = {"Content-Type": "application/json",
                   "Accept": "application/json",
                   "Cookie": f"token={self.__get_token()}"}
        return self.session.patch(url=url, headers=headers, data=data)

    @allure.step("Выполнение put запроса")
    def put(self, path, data=None):
        """Возвращает вызов put запроса к API.
        Требует передачу в заголовке Cookie auth token.

        :param path: адрес хоста
        :param data: передаваемое тело запроса
        """

        url = f"{self.host}/booking/{path}"
        headers = {"Content-Type": "application/json",
                   "Accept": "application/json",
                   "Cookie": f"token={self.__get_token()}"}
        return self.session.put(url=url, headers=headers, data=data)

    @allure.step("Выполнение delete запроса")
    def delete(self, path):
        """Возвращает вызов delete запроса к API.
        Требует передачу в заголовке Cookie auth token.

        :param path: адрес хоста
        """

        url = f"{self.host}/booking/{path}"
        headers = {"Content-Type": "application/json",
                   "Cookie": f"token={self.__get_token()}"}
        return self.session.delete(url=url, headers=headers)


@pytest.fixture(scope="session")
def booker_api(request):
    """Фикстура, создающая и возвращающая экземпляр класса ApiClient."""
    url = request.config.getoption("--url")
    login = request.config.getoption("--login")
    passw = request.config.getoption("--passw")
    return ApiClient(url, login, passw)
