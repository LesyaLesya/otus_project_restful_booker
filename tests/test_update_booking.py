"""Модуль с тестами put запросов - UpdateBooking."""


import allure
import pytest

from helpers.schemas import GET_BOOKING_SCHEMA
from helpers.urls_helper import Paths


@pytest.mark.put_booking
@allure.feature('PUT - UpdateBooking')
class TestUpdateBooking:
    """Тесты метода put /booking/id."""

    @allure.story('Обновление всех параметров')
    @allure.title('Валидные значения у всех полей')
    def test_put_valid_all_fields(
            self, booker_api, fixture_create_delete_booking_data, validate_json,
            status_code_msg, response_body_msg, generate_body_booking):
        """Тестовая функция для проверки обновления брони с валидными значениями (все поля).

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param fixture_create_delete_booking_data: фикстура для создания и удаления тестовых данных
        :param validate_json: фикстура для валидации JSON схемы
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param generate_body_booking: фикстура, создающая тело для запроса
        """
        booking_id, booking_data = fixture_create_delete_booking_data

        data = generate_body_booking(
            'Alex', 'Tompson', 13, True, '2023-04-20', '2023-05-05', '')
        response = booker_api.put(f'{Paths.BOOKING}{booking_id}', data)
        booking_data_new = response.json()

        with allure.step(status_code_msg(200)):
            assert response.status_code == 200, f'Код ответа - {response.status_code}'

        assert validate_json(booking_data, GET_BOOKING_SCHEMA)

        with allure.step(response_body_msg(booking_data_new)):
            assert booking_data_new['firstname'] == data['firstname'], \
                f'Имя - {booking_data_new["firstname"]}'
            assert booking_data_new['lastname'] == data['lastname'], \
                f'Фамилия - {booking_data_new["lastname"]}'
            assert booking_data_new['totalprice'] == data['totalprice'], \
                f'Итоговая цена - {booking_data_new["totalprice"]}'
            assert booking_data_new['depositpaid'] == data['depositpaid'], \
                f'Депозит - {booking_data_new["depositpaid"]}'
            assert booking_data_new['bookingdates']['checkin'] == \
                   data['bookingdates']['checkin'], \
                f'Дата заезда - {booking_data_new["bookingdates"]["checkin"]}'
            assert booking_data_new['bookingdates']['checkout'] == \
                   data['bookingdates']['checkout'], \
                f'Дата выезда - {booking_data_new["bookingdates"]["checkout"]}'
            assert booking_data_new['additionalneeds'] == data['additionalneeds'], \
                f'Пожелания - {booking_data_new["additionalneeds"]}'

    @allure.story('Обновление части параметров')
    @allure.title('Валидные значения firstname {first} и lastname {last}')
    @pytest.mark.parametrize('first, last', [('Peter', 'Jackson')])
    def test_put_not_all_fields(
            self, booker_api, first, last, fixture_create_delete_booking_data, status_code_msg):
        """Тестовая функция для проверки обновления брони с частью параметров.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param first: передаваемый в теле запроса firstname
        :param last: передаваемый в теле запроса lastname
        :param fixture_create_delete_booking_data: фикстура для создания и удаления тестовых данных
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        """
        booking_id, booking_data = fixture_create_delete_booking_data

        data = {'firstname': first, 'lastname': last}
        response = booker_api.put(f'{Paths.BOOKING}{booking_id}', data)

        with allure.step(status_code_msg(400)):
            assert response.status_code == 400, f'Код ответа - {response.status_code}'

    @allure.title('Пустое тело')
    def test_put_empty_body(
            self, booker_api, fixture_create_delete_booking_data, status_code_msg):
        """Тестовая функция для проверки обновления брони с пустым телом.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param fixture_create_delete_booking_data: фикстура для создания и удаления тестовых данных
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        """
        booking_id, booking_data = fixture_create_delete_booking_data
        response = booker_api.put(f'{Paths.BOOKING}{booking_id}', {})
        with allure.step(status_code_msg(400)):
            assert response.status_code == 400, f'Код ответа - {response.status_code}'

    @allure.title('Обновление брони по невалидному id {value}')
    @pytest.mark.parametrize('value', ['34533424553', '&(*&(*UIU*('])
    def test_put_invalid_id(self, booker_api, value, generate_body_booking, status_code_msg):
        """Тестовая функция для проверки обновления брони по невалидному id.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param value: передаваемый в урле id
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param generate_body_booking: фикстура, создающая тело для запроса
        """
        data = generate_body_booking()
        response = booker_api.put(f'{Paths.BOOKING}{value}', data)
        with allure.step(status_code_msg(405)):
            assert response.status_code == 405, f'Код ответа - {response.status_code}'
