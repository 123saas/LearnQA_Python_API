from requests import Response
import json
# в этом классе мы предлагаем для начала написать методы для получения значений куки и хэдер из ответа сервера по имени.
# суть этих методов бцдет заключаться в следующем:
# 1. сначала мы бцдем передавать в него объект ответа, который мы получаем от запроса и имя, по которому из этого ответа мы будем получать либо хэдер, либо куки
# Метод сам будет предварительно понимать есть ли такие данные в ответе и если нет, тест будет падать, значит что-то пошло не так, раз мы ожидали, что данные должны быть, а их нет
# Если данные есть, метод будет их возвращать
class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie with name {cookie_name} in the last response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Cannot find header with name {headers_name} in the last response"
        return response.headers[headers_name]

    # прежде чем получить что-то из json,мы должны убедиться, что ответ от сервера действительно нам пришел в этом формате.
    # Именно поэтому будет использовать try except.
    # Тут мы пытаемся распарсить ответ сервера будто это JSON. Мы специально это обернули в try, тк если у нас не получится, то есть если ответ окажется в каком-то другом формате, то у нас будет исключение JSONDecodeError и без конструкции try тест сломается ьез какой-то понятной ошибки.
    # Вместо этого в except, куда мы попадем в случае,если не сможем распарсить ответ,мы делаем assert False, то есть тоже делаем так, чтобы тест упал, однако, уже с нашей понятной нам ошибкой
    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"
    # если парсинг прошел успешно, то сделаем следующее:
        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"
        return response_as_dict[name]
    #То есть если парсинг прошел успешно, то мы делаем assert name in response_as_dict, f"Response JSON doesn't have key '{name}'" и убеждаемся, что значение по имени name присутствует в ответе и если все хорошо, возвращаем это значение

