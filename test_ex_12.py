# -*- coding: utf-8 -*-
import requests

class TestHeader:
    def test_method_header(self):
        url = "https://playground.learnqa.ru/api/homework_header"
        response = requests.get(url)
        header_dict = dict(response.headers) # отображение header в виде словаря
        key = "x-secret-homework-header"
        print(header_dict)
        assert key in header_dict, f"Ключ {key} отсутствует" # проверка, что есть ключ HomeWork
        expected_response_text = "Some secret value" # ожидаемый текст
        actual_response_text = header_dict['x-secret-homework-header'] # фактический текст
        assert expected_response_text == actual_response_text, f"Фактический текст не совпадает с ожидаемым"