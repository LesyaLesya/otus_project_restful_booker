"""Модуль с классом API клиента."""

import allure
import json
import logging
import requests

from helpers.urls_helper import Paths


class ApiClient:
    """Класс для выполнения запросов к API."""

    def __init__(self, host, schema, login, passw, headers):
        """Конструктор класса.

        :param host: адрес хоста
        :param schema: схема
        :param login: логин для получения auth token
        :param passw: пароль для получения auth token
        :param headers: заголовки запроса
        """
        self.host = host
        self.schema = schema
        self.__login = login
        self.__passw = passw
        self.headers = headers
        self.session = requests.Session()
        self.logger = logging.getLogger('requests')
        self.__token = self.__get_token()

    def _get_url(self, path):
        return f'{self.schema}://{self.host}/{path}'

    def __get_token(self):
        """Метод передачи в запросе учетных данных и получения auth token."""
        payload = {'username': self.__login, 'password': self.__passw}
        url = self._get_url(Paths.AUTH)
        response = self.session.post(url=url, data=payload)
        self.__token = json.loads(response.text)['token']
        self.logger.info(f'Получить токен {self.__token}')
        return self.__token

    def get(self, path='', params=None, headers_new=None, in_xml=False):
        """Возвращает вызов get запроса к API.

        :param path: путь
        :param params: гет параметры
        :param headers_new: кастомные заголовки
        :param in_xml: генерировать ли заголовки для формата xml
        """
        if headers_new:
            headers = headers_new
        else:
            if in_xml:
                headers = self.headers(xml=True)
            else:
                headers = self.headers()
        url = self._get_url(path)
        with allure.step(f'Выполнить запрос GET {url}, headers={headers}, params={params}'):
            res = self.session.get(url=url, params=params, headers=headers)
            self.logger.info(f'Метод и урл запроса: {res.request.method} {res.request.url}')
            self.logger.info(f'Заголовки запроса: {res.request.headers}')
            self.logger.info(f'Заголовки ответа: {res.headers}')
            try:
                self.logger.info(f'Тело ответа: {res.json()}')
            except json.decoder.JSONDecodeError as err:
                self.logger.error(f'Невалидный json в ответе. Error: {err}')
                self.logger.info(f'Тело ответа: {res.content}')
            return res

    def post(self, path='', data=None, headers_new=None, in_xml=False):
        """Возвращает вызов post запроса к API.

        :param path: путь
        :param data: тело запроса
        :param headers_new: кастомные заголовки
        """
        if headers_new:
            headers = headers_new
        else:
            if in_xml:
                headers = self.headers(method='post', xml=True)
            else:
                headers = self.headers(method='post')
        if in_xml:
            data = data
        else:
            data = json.dumps(data)
        url = self._get_url(path)
        with allure.step(f'Выполнить запрос POST {url}, headers={headers}, data={data}'):
            res = self.session.post(url=url, headers=headers, data=data)
            self.logger.info(f'Метод и урл запроса: {res.request.method} {res.request.url}')
            self.logger.info(f'Заголовки запроса: {res.request.headers}')
            self.logger.info(f'Тело запроса: {res.request.body}')
            self.logger.info(f'Заголовки ответа: {res.headers}')
            try:
                self.logger.info(f'Тело ответа: {res.json()}')
            except json.decoder.JSONDecodeError as err:
                self.logger.error(f'Невалидный json в ответе. Error: {err}')
                self.logger.info(f'Тело ответа: {res.content}')
            return res

    def patch(self, path='', data=None, headers_new=None, in_xml=False):
        """Возвращает вызов patch запроса к API.
        Требует передачу в заголовке Cookie auth token.

        :param path: путь
        :param data: тело запроса
        :param headers_new: кастомные заголовки
        """
        if headers_new:
            headers = headers_new
        else:
            if in_xml:
                headers = self.headers(method='patch', xml=True)
            else:
                headers = self.headers(method='patch', token=self.__token)

        if in_xml:
            data = data
        else:
            data = json.dumps(data)
        url = self._get_url(path)
        with allure.step(f'Выполнить запрос PATCH {url}, headers={headers}, data={data}'):
            res = self.session.patch(url=url, headers=headers, data=data)
            self.logger.info(f'Метод и урл запроса: {res.request.method} {res.request.url}')
            self.logger.info(f'Заголовки запроса: {res.request.headers}')
            self.logger.info(f'Тело запроса: {res.request.body}')
            self.logger.info(f'Заголовки ответа: {res.headers}')
            try:
                self.logger.info(f'Тело ответа: {res.json()}')
            except json.decoder.JSONDecodeError as err:
                self.logger.error(f'Невалидный json в ответе. Error: {err}')
                self.logger.info(f'Тело ответа: {res.content}')
            return res

    def put(self, path='', data=None, headers_new=None, in_xml=False):
        """Возвращает вызов put запроса к API.
        Требует передачу в заголовке Cookie auth token.

        :param path: путь
        :param data: тело запроса
        :param headers_new: кастомные заголовки
        """
        if headers_new:
            headers = headers_new
        else:
            if in_xml:
                headers = self.headers(method='put', xml=True)
            else:
                headers = self.headers(method='put', token=self.__token)
        if in_xml:
            data = data
        else:
            data = json.dumps(data)
        url = self._get_url(path)
        with allure.step(f'Выполнить запрос PUT {url}, headers={headers}, data={data}'):
            res = self.session.put(url=url, headers=headers, data=data)
            self.logger.info(f'Метод и урл запроса: {res.request.method} {res.request.url}')
            self.logger.info(f'Заголовки запроса: {res.request.headers}')
            self.logger.info(f'Тело запроса: {res.request.body}')
            self.logger.info(f'Заголовки ответа: {res.headers}')
            try:
                self.logger.info(f'Тело ответа: {res.json()}')
            except json.decoder.JSONDecodeError as err:
                self.logger.error(f'Невалидный json в ответе. Error: {err}')
                self.logger.info(f'Тело ответа: {res.content}')
            return res

    def delete(self, path='', headers_new=None):
        """Возвращает вызов delete запроса к API.
        Требует передачу в заголовке Cookie auth token.

        :param path: адрес хоста
        :param headers_new: кастомные заголовки
        """
        headers = headers_new or self.headers(method='delete', token=self.__token)
        url = self._get_url(path)
        with allure.step(f'Выполнить запрос DELETE {url}, headers={headers}'):
            res = self.session.delete(url=url, headers=headers)
            self.logger.info(f'Метод и урл запроса: {res.request.method} {res.request.url}')
            self.logger.info(f'Заголовки запроса: {res.request.headers}')
            self.logger.info(f'Заголовки ответа: {res.headers}')
            try:
                self.logger.info(f'Тело ответа: {res.json()}')
            except json.decoder.JSONDecodeError as err:
                self.logger.error(f'Невалидный json в ответе. Error: {err}')
                self.logger.info(f'Тело ответа: {res.content}')
            return res
