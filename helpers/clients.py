"""Модуль с классом API клиента."""

import allure
import json
import logging
import requests

from helpers.urls_helper import Paths


class ApiClient:
    """Класс для выполнения запросов к API."""

    def __init__(self, host, schema, headers, user, get_login, get_password):
        """Конструктор класса.

        :param host: адрес хоста
        :param schema: схема
        :param headers: заголовки запроса
        :param user: пользователь
        """
        self.host = host
        self.schema = schema
        self.headers = headers
        self.session = requests.Session()
        self.logger = logging.getLogger('requests')
        self.__token = self.__get_token(get_login, get_password)
        self.user = user

    def _get_url(self, path):
        return f'{self.schema}://{self.host}/{path}'

    def __get_token(self, get_login, get_password):
        """Метод передачи в запросе учетных данных и получения auth token."""
        payload = {'username': get_login, 'password': get_password}
        url = self._get_url(Paths.AUTH)
        response = self.session.post(url=url, data=payload)
        self.__token = json.loads(response.text)['token']
        self.logger.info(f'Получить токен {self.__token}')
        return self.__token

    def get(self, path='', params=None, headers_new=None, accept_header='json'):
        """Возвращает вызов get запроса к API.

        :param path: путь
        :param params: гет параметры
        :param headers_new: кастомные заголовки
        :param accept_header: в каком типе данных получать ответ
        """
        headers = headers_new or self.headers(accept=accept_header)
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

    def post(self, path='', data=None, headers_new=None, cont_type='json', accept_header='json'):
        """Возвращает вызов post запроса к API.

        :param path: путь
        :param data: тело запроса
        :param headers_new: кастомные заголовки
        :param accept_header: в каком типе данных получать ответ
        :param cont_type: в каком типе данных отправлять запрос
        """
        headers = headers_new or self.headers(cont_type=cont_type, accept=accept_header)
        if cont_type == 'json':
            data = json.dumps(data)
        else:
            data = data
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

    def patch(
            self, path='', data=None, headers_new=None, cont_type='json',
            accept_header='json', auth_type='cookie'):
        """Возвращает вызов patch запроса к API.
        Требует передачу в заголовке Cookie auth token.

        :param path: путь
        :param data: тело запроса
        :param headers_new: кастомные заголовки
        :param accept_header: в каком типе данных получать ответ
        :param cont_type: в каком типе данных отправлять запрос
        :param auth_type: как авторизоваться
        """
        headers = headers_new or self.headers(
            cont_type=cont_type, accept=accept_header, auth_type=auth_type, token=self.__token)
        if cont_type == 'json':
            data = json.dumps(data)
        else:
            data = data
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

    def put(self, path='', data=None, headers_new=None, cont_type='json',
            accept_header='json', auth_type='cookie'):
        """Возвращает вызов put запроса к API.
        Требует передачу в заголовке Cookie auth token.

        :param path: путь
        :param data: тело запроса
        :param headers_new: кастомные заголовки
        :param accept_header: в каком типе данных получать ответ
        :param cont_type: в каком типе данных отправлять запрос
        :param auth_type: как авторизоваться
        """
        headers = headers_new or self.headers(
            cont_type=cont_type, accept=accept_header, auth_type=auth_type, token=self.__token)
        if cont_type == 'json':
            data = json.dumps(data)
        else:
            data = data
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

    def delete(self, path='', headers_new=None, cont_type='json', auth_type='cookie'):
        """Возвращает вызов delete запроса к API.
        Требует передачу в заголовке Cookie auth token.

        :param path: адрес хоста
        :param headers_new: кастомные заголовки
        :param cont_type: в каком типе данных отправлять запрос
        :param auth_type: как авторизоваться
        """
        headers = headers_new or self.headers(
            cont_type=cont_type, auth_type=auth_type, token=self.__token)
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
