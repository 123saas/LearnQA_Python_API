
from lib.base_case import BaseCase
from lib.assertions import Assetions
from datetime import datetime
from lib.my_requests import MyRequests

class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self): # тест для получения данных пользователя будучи никем не авторизованным
        response = MyRequests.get("/user/2")
        # print(response.content)
        # нам надо зафиксировать не только то что какое-то поле есть, но и то, что каких-то полей нет, например, email, lastname и password
        Assetions.assert_json_has_key(response, "username")
        Assetions.assert_json_has_no_key(response, "email")
        Assetions.assert_json_has_no_key(response, "lastName")
        Assetions.assert_json_has_no_key(response, "firstName")

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assetions.assert_json_has_keys(response2, expected_fields)

# Запрос данных другого пользователя
    def test_get_another_user_detaling(self):
        base_part = "learnqa"  # сначала опеределяем базовую часть имейла, то есть ту подстроку с которой будут начинаться все имейлы
        domain = "example.com"  # домен
        random_part = datetime.now().strftime(
            "%m%d%Y%H%M%S")  # случайная часть, которая будет генерироваться на основе сегодняшней даты вплоть до секунды
        email = f"{base_part}{random_part}@{domain}"  # кладем имейл в переменную вызванную через self чтобы она была доступна в других функциях тестов
        password = '123'
        data_reg = {
            'password': password,
            'username': 'learnqa1',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email,

        }
        response = MyRequests.post("/user/", data=data_reg) # регистрация нового пользователя

        data = {
                'email': email,
                'password': password
            }
        response1 = MyRequests.post("/user/login", data=data) # авторизация подновым пользователем

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id") - 1 # сохраняется user_id предыдущего пользователя
        response2 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        expected_fields = ["email", "firstName", "lastName"]
        Assetions.assert_json_has_no_keys(response2, expected_fields) # проверка, что не отображаются ключи: ["email", "firstName", "lastName"]
        Assetions.assert_json_has_key(response2, "username") # проверка, что отображается username
