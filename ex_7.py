# -*- coding: utf-8 -*-
import requests

method = ['GET', 'POST', 'PUT', 'DELETE']

response_without_method = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print("Ответ на http-запрос без параметра 'method':", response_without_method.text)
response_with_method_head = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method":"HEAD"})
print("Ответ на http-запрос c параметром method=HEAD:", response_with_method_head.text)
response_with_correct_method = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method":"GET"})
print("Ответ на http-запрос верным параметром 'method':", response_with_correct_method.text)

for i in range(len(method)):
    response_get = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method":f"{method[i]}"})
    response_post = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method":f"{method[i]}"})
    response_put = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method":f"{method[i]}"})
    response_delete = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method":f"{method[i]}"})
    print(f"GET-запрос. Ответ при method={method[i]}:", response_get.text)
    print(f"POST-запрос. Ответ при method={method[i]}:", response_post.text)
    print(f"PUT-запрос. Ответ при method={method[i]}:", response_put.text)
    print(f"DELETE-запрос. Ответ при method={method[i]}:", response_delete.text)
