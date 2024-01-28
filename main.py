# -*- coding: utf-8 -*-
import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True) # allow_redirects=True означает, что сервер пытается перенаправить нас на новую урл, мы следуем за них пока не достигнем конечной точки. allow_redirects=False мы не пойдем на рекдирект и в ответе будут только данные первого запроса. True - дефолтное значение
all_responses = response.history # чтобы узнать куда именно нас перенаправили, мы можем вызвать фукцию history. она вернет массив всех
for i in range(len(all_responses)): # цикл от 0 до количества редиректов (len(all_responses))
    url_response = response.history[i] # в переменную кладем урл
    count = i + 1
    print(f"Url {count}:", url_response.url)
print("Количество url:", len(all_responses))
