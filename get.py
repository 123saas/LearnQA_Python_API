import requests

response = requests.get("https://playground.learnqa.ru/api/get_text") # создаем GET-запрос на этот адрес. В переменной response будет храниться информация об ответе на запрос
print(response.text) # распечатываем текст ответа