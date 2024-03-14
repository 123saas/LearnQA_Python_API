import pytest

from lib.base_case import BaseCase
from lib.assertions import Assetions
from lib.my_requests import MyRequests
import allure

@allure.epic("Авторизационные кейсы") # эпик означает, что последующие тесты принадлежат большой единой общей части (авторизационные кейсы)
class TestUserAuth(BaseCase):
    execlude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)


        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

    @allure.description("Этот тест успешно авторизует пользователя по электронной почте и паролю") # описание нужно для того, чтобы в отчете было понятно, что именно этот тест проверяет
    def test_auth_user(self):
        response2 = MyRequests.get("/user/auth",
                                   headers={"x-csrf-token": self.token},
                                   cookies={"auth_sid": self.auth_sid})
        Assetions.assert_json_value_by_name(
            response2,
            "user_id",
            self.user_id_from_auth_method,
            "User id from auth method is not equal to user id from check method"
        )

    @allure.description("Этот тест проверяет статус авторизации без отправки файла cookie или токена")
    @pytest.mark.parametrize('condition', execlude_params)
    def test_negative_auth_check(self, condition):

        if condition == "no-cookie":
            response2 = MyRequests.get("/user/auth", headers={"x-csrf-token": self.token})
        else:
            response2 = MyRequests.get("/user/auth",
                                       cookies={"auth_sid": self.auth_sid})

        Assetions.assert_json_value_by_name(
            response2,
            "user_id",
            0,
            f"User is authorized with condition {condition}"
        )
