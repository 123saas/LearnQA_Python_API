# -*- coding: utf-8 -*-
import requests
import json
import time

response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
print("Создание задачи ", response.text)
response_text = response.text
obj = json.loads(response_text)
token = obj['token'] # в переменную token передается из ответа токен
seconds = obj['seconds'] # в переменную seconds передается из ответа секунды
payload_token = {"token": f"{token}"} # переменная для передачи параметра в GET-запросе
response_with_token_before = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=payload_token)
print("Ответ с token ДО того, как задача готова: ", response_with_token_before.text)
time.sleep(seconds) # ждать нужное количество секунд
response_with_token_after = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=payload_token)
print("Ответ c token ПОСЛЕ того, как задача готова: ", response_with_token_after.text)
