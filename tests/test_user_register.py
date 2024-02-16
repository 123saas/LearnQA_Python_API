
from lib.base_case import BaseCase
from lib.assertions import Assetions
import pytest
import json
from random import choice
from datetime import datetime
from lib.my_requests import MyRequests

class TestUserRegister(BaseCase):

    params_without_password = {

        'username': 'learnqa',
        'firstName': 'learnqa',
        'lastName': 'learnqa',
        'email': 'vinkotov@example.com'
    }
    params_without_username = {
        'password': '123',

        'firstName': 'learnqa',
        'lastName': 'learnqa',
        'email': 'vinkotov@example.com'
    }
    params_without_firstname = {
        'password': '123',
        'username': 'learnqa',

        'lastName': 'learnqa',
        'email': 'vinkotov@example.com'
    }
    params_without_lastname = {
        'password': '123',
        'username': 'learnqa',
        'firstName': 'learnqa',

        'email': 'vinkotov@example.com'
    }
    params_without_email = {
        'password': '123',
        'username': 'learnqa',
        'firstName': 'learnqa',
        'lastName': 'learnqa'

    }



# успешное создание пользователя
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)
        # assert response.status_code == 200, f"Непредвиденный статус код {response.status_code}"
        Assetions.assert_code_status(response, 200)
        Assetions.assert_json_has_key(response, "id")


    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user/", data=data)
        # print(response.status_code)
        # print(response.content)

        Assetions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Непредвиденный содержание ответа {response.content}"

    # Создание пользователя с некорректным email - без символа @
    def test_create_user_without_at_in_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)
        # print(response.status_code)
        # print(response.content)

        Assetions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format", f"Непредвиденный содержание ответа {response.content}"

# Создание пользователя без указания одного из полей - с помощью @parametrize необходимо проверить, что отсутствие любого параметра не дает зарегистрировать пользователя
    @pytest.mark.parametrize('without_one_param', ((params_without_password),
                                                   (params_without_username),
                                                   (params_without_firstname),
                                                   (params_without_lastname),
                                                   (params_without_email)))
    def test_create_user_without_one_param(self, without_one_param):

        response = MyRequests.post("/user/", data=without_one_param)
        correct_params = [
            ("password"),
            ("username"),
            ("firstName"),
            ("lastName"),
            ("email")
        ]

        for i in range(len(correct_params)): # цикл проходится по всем параметрам
            if correct_params[i] not in without_one_param: # если какого-то параметра нет в without_one_param
                missed_params = correct_params[i] # то в missed_params записывать этот параметр
                break
        # print(response.status_code)
        # print(response.content)
        # print("missed_params", missed_params)

        Assetions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {missed_params}", f"Непредвиденный содержание ответа {response.content}"

# Создание пользователя с очень коротким именем в один символ
    def test_name_in_one_character(self):
        firstName = 'l'
        data_1 = {
            'password': '123',
            'username': 'learnqa',
            'firstName': firstName,
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'

        }
        response = MyRequests.post("/user/", data=data_1)
        # print(response.status_code)
        # print(response.content)
        Assetions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'firstName' field is too short", f"Непредвиденный содержание ответа {response.content}"

# Создание пользователя с очень длинным именем - длиннее 250 символов
    def test_name_more_250_characters(self):
        firstName = "".join(choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for i in range(260)) # генерация 260 символов в имене
        data_1 = {
            'password': '123',
            'username': 'learnqa',
            'firstName': firstName,
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'

        }

        response = MyRequests.post("/user/", data=data_1)
        # print(response.status_code)
        # print(response.content)
        Assetions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'firstName' field is too long", f"Непредвиденный содержание ответа {response.content}"
