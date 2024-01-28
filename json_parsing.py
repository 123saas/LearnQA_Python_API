import json

json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}' # здесь мы задаем переменную типа стринг
obj = json.loads(json_text) # при помощи библиотеки json парсим нашу строку, она превращается в объект (по своим свойтсвам напоминающую словарь в питоне). этот словарь мы и кладем в obj
message_2 = obj['messages'][1]
print(message_2['message']) # обращаемся к ключу message в словаре message_2 и возвращем его значение
