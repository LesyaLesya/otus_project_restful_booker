"""Модуль с тестами get запросов - GetBookingIds."""

import allure
import pytest

from helpers.schemas import GET_BOOKING_IDS_SCHEMA
from helpers.urls_helper import Params, Paths


@pytest.fixture
def fixture_create_delete_booking_data_firstname(create_test_booking, delete_test_booking, get_params):
    booking = create_test_booking(firstname=get_params)
    booking_id = booking['bookingid']
    yield booking_id
    delete_test_booking(booking_id)


@pytest.fixture
def fixture_create_delete_booking_data_lastname(create_test_booking, delete_test_booking, get_params):
    booking = create_test_booking(lastname=get_params)
    booking_id = booking['bookingid']
    yield booking_id
    delete_test_booking(booking_id)


@pytest.fixture
def fixture_create_delete_booking_data_fullname(create_test_booking, delete_test_booking, get_params):
    booking = create_test_booking(firstname=get_params['first'], lastname=get_params['last'])
    booking_id = booking['bookingid']
    yield booking_id
    delete_test_booking(booking_id)


@pytest.mark.get_booking_ids
@allure.feature('GET - GetBookingIds')
class TestGetBookingIds:
    """Тесты метода get /booking."""

    @allure.title('Получение списка всех броней')
    def test_get_all_bookings(self, booker_api, validate_json, status_code_msg, response_body_msg):
        """Тестовая функция для проверки получения всех сущностей.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param validate_json: фикстура для валидации JSON схемы
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        """
        response = booker_api.get(Paths.BOOKING)
        booking_data = response.json()

        with allure.step(status_code_msg(200)):
            assert response.status_code == 200, f'Код ответа - {response.status_code}'

        assert validate_json(booking_data, GET_BOOKING_IDS_SCHEMA)

        with allure.step(response_body_msg(booking_data)):
            assert len(booking_data) != 0, 'Нет ни одной сущности'

    @allure.story('Проверка параметра firstname')
    @allure.title('Валидные значения firstname - {get_params}')
    @pytest.mark.parametrize('get_params', ['Stacy', 'Olivia'])
    def test_get_by_valid_firstname(
            self, booker_api, fixture_create_delete_booking_data_firstname,
            validate_json, status_code_msg, response_body_msg, get_params):
        """Тестовая функция для проверки получения брони с валидными значениями параметра firstname.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param fixture_create_delete_booking_data_firstname: фикстура для создания и удаления тестовых данных
        :param validate_json: фикстура для валидации JSON схемы
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        """
        booking_id = fixture_create_delete_booking_data_firstname

        payload = {Params.FIRSTNAME: get_params}
        response = booker_api.get(path=Paths.BOOKING, params=payload)
        booking_data = response.json()

        with allure.step(status_code_msg(200)):
            assert response.status_code == 200, f'Код ответа - {response.status_code}'

        assert validate_json(booking_data, GET_BOOKING_IDS_SCHEMA)

        with allure.step(response_body_msg(booking_data)):
            assert len(booking_data) == 1, f'Количество броней с именем {get_params} - {len(booking_data)}'
            assert booking_data[0]['bookingid'] == booking_id, f'Тело ответа {booking_data}'

    @allure.story('Проверка параметра firstname')
    @allure.title('Несуществующие значения firstname - {value}')
    @pytest.mark.parametrize('value', ['Тест', '13'])
    def test_get_by_invalid_firstname(self, booker_api, value, status_code_msg, response_body_msg):
        """Тестовая функция для проверки получения брони с несуществующими значениями параметра firstname.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param value: передаваемый в урле параметр firstname
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        """
        payload = {Params.FIRSTNAME: value}
        response = booker_api.get(path=Paths.BOOKING, params=payload)
        booking_data = response.json()

        with allure.step(status_code_msg(200)):
            assert response.status_code == 200, f'Код ответа - {response.status_code}'

        with allure.step(response_body_msg(booking_data)):
            assert len(booking_data) == 0, f'У {value} есть бронь. Тело ответа {booking_data}'

    @allure.story('Проверка параметра lastname')
    @allure.title('Существующие значения lastname - {get_params}')
    @pytest.mark.parametrize('get_params', ['Chapman-Wilson', 'Chacha'])
    def test_get_by_valid_lastname(
            self, booker_api, status_code_msg, response_body_msg,
             validate_json, fixture_create_delete_booking_data_lastname, get_params):
        """Тестовая функция для проверки получения брони с существующими значениями параметра lastname.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param fixture_create_delete_booking_data_lastname: фикстура для создания и удаления тестовых данных
        :param validate_json: фикстура для валидации JSON схемы
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        """
        booking_id = fixture_create_delete_booking_data_lastname

        payload = {Params.LASTNAME: get_params}
        response = booker_api.get(path=Paths.BOOKING, params=payload)
        booking_data = response.json()

        with allure.step(status_code_msg(200)):
            assert response.status_code == 200, f'Код ответа - {response.status_code}'

        assert validate_json(booking_data, GET_BOOKING_IDS_SCHEMA)

        with allure.step(response_body_msg(booking_data)):
            assert len(booking_data) == 1, f'Количество броней с фамилией {get_params} - {len(booking_data)}'
            assert booking_data[0]['bookingid'] == booking_id, f'Тело ответа {booking_data}'

    @allure.story('Проверка параметра lastname')
    @allure.title('Несуществующие значения lastname - {value}')
    @pytest.mark.parametrize('value', ['0', '$$@*:;'])
    def test_get_by_invalid_lastname(self, booker_api, value, status_code_msg, response_body_msg):
        """Тестовая функция для проверки получения брони с несуществующими значениями параметра lastname.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param value: передаваемый в урле параметр lastname
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        """
        payload = {Params.LASTNAME: value}
        response = booker_api.get(path=Paths.BOOKING, params=payload)
        booking_data = response.json()

        with allure.step(status_code_msg(200)):
            assert response.status_code == 200, f'Код ответа - {response.status_code}'

        with allure.step(response_body_msg(booking_data)):
            assert len(booking_data) == 0, f'У {value} есть бронь. Тело ответа {booking_data}'

    @allure.story('Проверка нескольких параметров')
    @allure.title('Существующие значения firstname и lastname - {get_params}')
    @pytest.mark.parametrize('get_params', [({'first': 'Stella', 'last': 'White'})])
    def test_get_by_valid_fullname(
            self, booker_api, status_code_msg, validate_json, response_body_msg,
            fixture_create_delete_booking_data_fullname, get_params):
        """Тестовая функция для проверки получения брони с существующими значениями параметров firstname и lastname.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param fixture_create_delete_booking_data_fullname: фикстура для создания и удаления тестовых данных
        :param validate_json: фикстура для валидации JSON схемы
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        """
        booking_id = fixture_create_delete_booking_data_fullname

        payload = {Params.FIRSTNAME: get_params['first'], Params.LASTNAME: get_params['last']}
        response = booker_api.get(path=Paths.BOOKING, params=payload)
        booking_data = response.json()

        with allure.step(status_code_msg(200)):
            assert response.status_code == 200, f'Код ответа - {response.status_code}'

        assert validate_json(booking_data, GET_BOOKING_IDS_SCHEMA)

        with allure.step(response_body_msg(booking_data)):
            assert len(booking_data) == 1, \
                f'Количество броней с фамилией {get_params["l"]} и именем {get_params["f"]} - {len(booking_data)}'
            assert booking_data[0]['bookingid'] == booking_id, f'Тело ответа {booking_data}'

    @allure.story('Проверка нескольких параметров')
    @allure.title('Несуществующие значения firstname {first} и lastname {last}')
    @pytest.mark.parametrize('first, last', [('Eric', '0'), ('Test', 'Jones')])
    def test_get_by_invalid_fullname(self, booker_api, first, last, status_code_msg, response_body_msg):
        """Тестовая функция для проверки получения брони с несуществующими значениями параметров firstname и lastname.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param first: передаваемый в урле параметр firstname
        :param last: передаваемый в урле параметр lastname
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        """
        payload = {Params.FIRSTNAME: first, Params.LASTNAME: last}
        response = booker_api.get(path=Paths.BOOKING, params=payload)
        booking_data = response.json()

        with allure.step(status_code_msg(200)):
            assert response.status_code == 200, f'Код ответа - {response.status_code}'

        with allure.step(response_body_msg(booking_data)):
            assert len(booking_data) == 0, f'У {first} {last} есть бронь. Тело ответа {booking_data}'

    @allure.story('Проверка параметра checkin')
    @allure.title('Валидные значения checkin - {value}')
    @pytest.mark.parametrize('value', ['2023-01-01', '2021-02-01'])
    def test_get_by_valid_checkin(self, booker_api, value, status_code_msg, response_body_msg):
        """Тестовая функция для проверки получения брони с валидными значениями параметра checkin.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param value: передаваемый в урле параметр checkin
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        """
        payload = {Params.CHECKIN: value}
        response = booker_api.get(path=Paths.BOOKING, params=payload)
        booking_data = response.json()

        with allure.step(status_code_msg(200)):
            assert response.status_code == 200, f'Код ответа - {response.status_code}'

        with allure.step(response_body_msg(booking_data)):
            assert all([booker_api.get(path=f'{Paths.BOOKING}{i["bookingid"]}').json()['bookingdates']['checkin']
                        >= value for i in booking_data])

    @allure.story('Проверка параметра checkin')
    @allure.title('Невалидные значения checkin - {value}')
    @pytest.mark.parametrize('value', ['11-11-2023', '11.11.2023'])
    def test_get_by_invalid_checkin(self, booker_api, value, status_code_msg, response_body_msg):
        """Тестовая функция для проверки получения брони с валидными значениями параметра checkin.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param value: передаваемый в урле параметр checkin
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        """
        payload = {Params.CHECKIN: value}
        response = booker_api.get(path=Paths.BOOKING, params=payload)
        booking_data = response.json()

        with allure.step(status_code_msg(200)):
            assert response.status_code == 200, f'Код ответа - {response.status_code}'

        with allure.step(response_body_msg(booking_data)):
            assert len(booking_data) == 0, f'Количество броней - {len(booking_data)}'
