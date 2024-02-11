import requests
from requests import Response
import json
# в этом классе предлагаем сделать функцию, которая будет называться assert_json_value_by_name, то есть мы убеждаемся, что значение внутри json доступно по определнному имени и равняется тому, что мы ожидаем
class Assetions:
    # этот метод мы делаем статическим, так как класс Assetions не является прямым наследником для наших тестов и чтобы использовать функции этого класса в тестах нам потребуется либо каждый раз создавать сначала объект assertion и вызывать функции от объекта, либо сделать функции статическими
    @staticmethod # поэтому здесь напишем staticmethod.
    def assert_json_value_by_name(response: Response, name, expected_value, error_message): # на вход эта функция должна получать объект с ответом сервера, чтобы получить из него текст, также имя по которому искать значение в json, ожидаемое значение и текст ошибки, в случае если это значение не удается найти
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"
        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"
        assert response_as_dict[name] == expected_value, error_message

