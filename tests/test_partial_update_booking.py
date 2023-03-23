"""Модуль с тестами patch запросов - PartialUpdateBooking."""


import allure
import pytest

from helpers.schemas import GET_BOOKING_SCHEMA
from helpers.urls_helper import Paths


@pytest.mark.patch_booking
@allure.feature('PATCH - PartialUpdateBooking')
class TestPartialUpdateBooking:
    """Тесты метода patch /booking/id."""

    @allure.story('Обновление части параметров')
    @allure.title('Валидные значения firstname {first} и lastname {last}')
    @pytest.mark.parametrize('first, last', [('Peter', 'Jackson'), ('Emma', 'Star')])
    def test_patch_valid_firstname_lastname(
            self, booker_api, first, last, fixture_create_delete_booking_data,
            status_code_msg, response_body_msg, validate_json):
        """Тестовая функция для проверки обновления брони с валидными значениями firstname, lastname.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param first: передаваемый в теле запроса firstname
        :param last: передаваемый в теле запроса lastname
        :param fixture_create_delete_booking_data: фикстура для создания и удаления тестовых данных
        :param validate_json: фикстура для валидации JSON схемы
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        """
        booking_id, booking_data = fixture_create_delete_booking_data

        data = {'firstname': first, 'lastname': last}
        response = booker_api.patch(f'{Paths.BOOKING}{booking_id}', data)
        booking_data_new = response.json()

        with allure.step(status_code_msg(200)):
            assert response.status_code == 200, f'Код ответа - {response.status_code}'

        assert validate_json(booking_data, GET_BOOKING_SCHEMA)

        with allure.step(response_body_msg(booking_data_new)):
            assert booking_data_new['firstname'] == first, f'Имя - {booking_data_new["firstname"]}'
            assert booking_data_new['lastname'] == last, f'Фамилия - {booking_data_new["lastname"]}'
            assert booking_data_new['totalprice'] == booking_data['totalprice'], \
                f'Итоговая цена - {booking_data_new["totalprice"]}'
            assert booking_data_new['depositpaid'] == booking_data['depositpaid'], \
                f'Депозит - {booking_data_new["depositpaid"]}'
            assert booking_data_new['bookingdates']['checkin'] == \
                booking_data['bookingdates']['checkin'], \
                f'Дата заезда - {booking_data_new["bookingdates"]["checkin"]}'
            assert booking_data_new['bookingdates']['checkout'] == \
                booking_data['bookingdates']['checkout'], \
                f'Дата выезда - {booking_data_new["bookingdates"]["checkout"]}'
            assert booking_data_new['additionalneeds'] == \
                   booking_data['additionalneeds'], \
                   f'additionalneeds - {booking_data_new["additionalneeds"]}'

    @allure.story('Обновление всех параметров')
    @allure.title('Валидные значения у всех полей')
    def test_patch_valid_all_fields(
            self, booker_api, fixture_create_delete_booking_data, status_code_msg,
            response_body_msg, validate_json, generate_body_booking):
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
            'Andrea', 'Jackson', 232, False, '2022-05-01', '2022-06-01', 'Breakfast, Dinner')
        response = booker_api.patch(f'{Paths.BOOKING}{booking_id}', data)
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

    @allure.title('Пустое тело')
    def test_patch_empty_body(
            self, booker_api, fixture_create_delete_booking_data, status_code_msg, validate_json, response_body_msg):
        """Тестовая функция для проверки обновления брони при передаче пустого тела.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param fixture_create_delete_booking_data: фикстура для создания и удаления тестовых данных
        :param validate_json: фикстура для валидации JSON схемы
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        """
        booking_id, booking_data = fixture_create_delete_booking_data

        response = booker_api.patch(f'{Paths.BOOKING}{booking_id}', {})
        booking_data_new = response.json()

        with allure.step(status_code_msg(200)):
            assert response.status_code == 200, f'Код ответа - {response.status_code}'

        assert validate_json(booking_data, GET_BOOKING_SCHEMA)

        with allure.step(response_body_msg(booking_data_new)):
            assert booking_data_new['firstname'] == booking_data['firstname'], \
                f'Имя - {booking_data_new["firstname"]}'
            assert booking_data_new['lastname'] == booking_data['lastname'], \
                f'Фамилия - {booking_data_new["lastname"]}'
            assert booking_data_new['totalprice'] == booking_data['totalprice'], \
                f'Итоговая цена - {booking_data_new["totalprice"]}'
            assert booking_data_new['depositpaid'] == booking_data['depositpaid'], \
                f'Депозит - {booking_data_new["depositpaid"]}'
            assert booking_data_new['bookingdates']['checkin'] == \
                   booking_data['bookingdates']['checkin'], \
                f'Дата заезда - {booking_data_new["bookingdates"]["checkin"]}'
            assert booking_data_new['bookingdates']['checkout'] == \
                   booking_data['bookingdates']['checkout'], \
                f'Дата выезда - {booking_data_new["bookingdates"]["checkout"]}'
            assert booking_data_new['additionalneeds'] == booking_data['additionalneeds'], \
                f'Пожелания - {booking_data_new["additionalneeds"]}'

    @allure.title('Обновление брони по невалидному id {value}')
    @pytest.mark.parametrize('value', ['213123', 'tests'])
    def test_patch_invalid_id(self, booker_api, value, generate_body_booking, status_code_msg):
        """Тестовая функция для проверки обновления брони по невалидному id.

        :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
        :param value: передеваемый в урле id
        :param status_code_msg: фикстура, возвращающая текст проверки кода ответа
        :param generate_body_booking: фикстура, создающая тело для запроса
        """
        data = generate_body_booking()
        response = booker_api.patch(f'{Paths.BOOKING}{value}', data)
        with allure.step(status_code_msg(405)):
            assert response.status_code == 405, f'Код ответа - {response.status_code}'
