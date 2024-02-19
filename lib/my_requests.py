import requests
from lib.logger import Logger

class MyRequests:
    # def _send - это приватный метод, поэтому напишем 4 публичных метода
    @staticmethod
    def post(url: str, data: dict=None, headers: dict=None, cookies: dict=None):
        return MyRequests._send(url, data, headers, cookies, 'POST')

    @staticmethod
    def put(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, headers, cookies, 'PUT')

    @staticmethod
    def delete(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, headers, cookies, 'DELETE')

    @staticmethod
    def get(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, headers, cookies, 'GET')


    # сначала сделаем центальный метод send. именно он будет отправлять наши запросы. мы сделаем его статическим, так как класс является вспомогательным и создавать объект этого класса нам не потребуется
    @staticmethod
    def _send(url: str, data: dict, headers: dict, cookies: dict, method: str): # метод _send начинается с нижнего подчеркивания, дело в том что в python нет как таковых приватных функций, как в других языках программирования, все фунции можно вызывать от мени класса или от объекта класса, но чтобы как-то обозначить что та или иная функция все же должна использоваться только внутри класса (является вспомогательной) не для использования извне, разработчики python договорились имена таких функций начинать с нижнего подчеркивания
        url = f"https://playground.learnqa.ru/api{url}" # здесь мы один раз напишем домен нашего api, чтобы в самих тестах не дублировать его каждый раз
        # создадим проверку
        if headers is None: # если в функцию не был передан словарь headers, то мы заменяем его значение None на пустой словарь
            headers = {} # headers равно пустой массив
        if cookies is None:
            cookies = {} # cookies равно пустой массив

        Logger.add_request(url, data, headers, cookies, method)

        # код для выбора метода
        if method == 'GET':
            response = requests.get(url, params=data, headers=headers, cookies=cookies)
        elif method == 'POST':
            response = requests.post(url, data=data, headers=headers, cookies=cookies)
        elif method == 'PUT':
            response = requests.put(url, data=data, headers=headers, cookies=cookies)
        elif method == 'DELETE':
            response = requests.delete(url, data=data, headers=headers, cookies=cookies)
        else:
            raise Exception(f"HTTP method '{method}' was received")

        # и перед тем, как возвращать запрос, напишем:
        Logger.add_response(response)

        return response