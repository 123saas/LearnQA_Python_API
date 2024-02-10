# -*- coding: utf-8 -*-
import requests
import pytest
import json

class TestUserAgent:

    expected_values_platform = [
        ('"platform":"Mobile"'),
        ('"platform":"Googlebot"'),
        ('"platform":"Web"')
    ]

    expected_values_browser = [
        ('"browser":"No"'),
        ('"browser":"Chrome"'),
        ('"browser":"Unknown"')
    ]

    expected_values_device = [
        ('"device":"Android"'),
        ('"device":"iOS"'),
        ('"device":"Unknown"'),
        ('"device":"No"'),
        ('"device":"iPhone"')
    ]

    user_agents = [
        ("Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"),
        ("Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1"),
        ("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"),
        ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0"),
        ("Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1")
    ]

    @pytest.mark.parametrize("exp_val_pl, exp_val_brow, exp_val_dev, user_agent", [
        (expected_values_platform[0], expected_values_browser[0], expected_values_device[0], user_agents[0]),
        (expected_values_platform[0], expected_values_browser[1], expected_values_device[1], user_agents[1]),
        (expected_values_platform[1], expected_values_browser[2], expected_values_device[2], user_agents[2]),
        (expected_values_platform[2], expected_values_browser[1], expected_values_device[3], user_agents[3]),
        (expected_values_platform[0], expected_values_browser[0], expected_values_device[4], user_agents[4])])
    def test_user_agent(self, exp_val_pl, exp_val_brow, exp_val_dev, user_agent):
        url = "https://playground.learnqa.ru/ajax/api/user_agent_check"
        response = requests.get(url, headers={"User-Agent": user_agent})
        keys = [
            ("platform"),
            ("browser"),
            ("device")
        ]
        response_text = response.text
        obj = json.loads(response_text)
        platform = obj['platform']  # в переменную platform передается из ответа платформа
        browser = obj['browser']  # в переменную browser передается из ответа браузер
        device = obj['device']  # в переменную device передается из ответа девайс
        user_agent_1 = obj['user_agent']  # в переменную user_agent_1 передается из ответа user_agent
        count_keys = len(keys)
        for i in range(count_keys):
            assert keys[i] in response.text, f"Ключ {keys[i]} отсутствует"  # проверка, что все ключи есть в ответе
        assert exp_val_pl in response.text, f"ОР {exp_val_pl} не совпадает с ФР platform={platform} в user_agent={user_agent_1}"
        assert exp_val_brow in response.text, f"ОР {exp_val_brow} не совпадает с ФР browser={browser} в user_agent={user_agent_1}"
        assert exp_val_dev in response.text, f"ОР {exp_val_dev} не совпадает с ФР device={device} в user_agent={user_agent_1}"
