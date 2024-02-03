# -*- coding: utf-8 -*-
import requests
class TestCookie:
    def test_method_cookie(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"
        response = requests.get(url)
        cookie_dict = dict(response.cookies) # отображение cookie в виде словаря
        print(cookie_dict)
        assert "HomeWork" in cookie_dict, f"Ключ 'HomeWork' отсутствует" # проверка, что есть ключ HomeWork
        expected_response_text = "hw_value" # ожидаемый текст
        actual_response_text = cookie_dict['HomeWork'] # фактический текст
        assert expected_response_text == actual_response_text, f"Фактический текст не совпадает с ожидаемым"