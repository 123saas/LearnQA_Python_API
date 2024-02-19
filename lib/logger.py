# работать наш класс будет следующим образом:
# в классе будет два метода: 1) логирование запроса; 2) логирование ответа 3) и один метод, который будет получен текст лога и писать файл
# сам файл мы вынесем, как переменную класса, название файла будет содержать в себе дату и время запуска с точностью до секунды, таким образом для разных запусков у нас будут генерироваться разные файлы
# так как наш логгер будет работать со временем нам потребуется импортировать библиотеку datetime

import datetime
import os
from requests import Response

class Logger:
    file_name = f"logs/log_" + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + ".log"

    # функция, которая пишет в этот файл данные
    @classmethod # это @classmethod, не статикметод, в питоне это похожие вещи с той лишь разницей, что работая с @classmethod у нас появляется возможность обращаться к переменным класса через ключевое слово "cls", а нам как раз и нужно обращаться к переменной, хранящей в себе название файла, куда надо писать лог
    # далее мы открываем этот файл и пишем туда данные, которые нам пришли в параметре строки data
    def _write_log_to_file(cls, data: str):
        with open(cls.file_name, 'a', encoding='utf-8') as logger_file:
            logger_file.write(data)

    # теперь напишем метод, который будет получать данные запроса, подготовливать их в какую-то строку и отдавать нашему методу write to log file
    @classmethod
    def add_request(cls, url: str, data: dict, headers: dict, cookies: dict, method: str): # наш метод на вход будет получать url запроса, его данные, заголовки, куки и сам тип запроса. все это мы будем превращать в строку
        testname = os.environ.get('PYTEST_CURRENT_TEST') # с помощью конструкции "os.environ.get" pytest говорит какой сейчас тест запушен и как он называется, так как мы будем писать в один лог для всех тестов текущего запуска, удобно, чтобы в нашем логе было понятно, какой запрос к какому тесту имеет значение
        # теперь напишем сам метод:
        data_to_add = f"\n-----\n" # конструкция \n означает перенос на другую строку
        data_to_add += f"Test: {testname}\n"
        data_to_add += f"Time: {str(datetime.datetime.now())}\n"
        data_to_add += f"Request method: {method}\n"
        data_to_add += f"Request URL: {url}\n"
        data_to_add += f"Request data: {data}\n"
        data_to_add += f"Request headers: {headers}\n"
        data_to_add += f"Request cookies: {cookies}\n"
        data_to_add += "\n"

        # запишем подготовленные нами в строку данные в файл:
        cls._write_log_to_file(data_to_add)

    # метод для записи ответа от сервера
    @classmethod
    def add_response(cls, response: Response):
        cookies_as_dict = dict(response.cookies)
        headers_as_dict = dict(response.headers)

        # запишем нужные нам данные, которые хотим добавить
        data_to_add = f"Response code: {response.status_code}\n"
        data_to_add += f"Response text: {response.text}\n"
        data_to_add += f"Response headers: {headers_as_dict}\n"
        data_to_add += f"Response cookies: {cookies_as_dict}\n"
        data_to_add += "\n-----\n"

        # запишем в наш файл
        cls._write_log_to_file(data_to_add)
