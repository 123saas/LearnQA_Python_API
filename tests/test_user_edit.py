
from lib.base_case import BaseCase
from lib.assertions import Assetions
from lib.my_requests import MyRequests

# создадим следующий тест:
# вначале мы будем создавать пользователя, потом его редактировать, а затем проверять, что мы успешно его отредактировали с помощью метода получения данных о пользователе
# и для получения, и для редактирования данных нам потребудется авторизоваться этим пользователям
# получается:
# 1. Создание пользвателя
# 2. Авторизация
# 3. Редактирование
# 4. Получение данных
class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):

        # РЕГИСТРАЦИЯ
        register_data = self.prepare_registration_data() # 1. подготовить данные для создания пользователей, в том числе и его имейла. Генерируем пользователя
        response1 = MyRequests.post("/user/", data=register_data)

        #убедимся, что на запрос, который мы послали сервер ответил кодом ответа 200 и что в ответе есть id нового пользователя:
        Assetions.assert_code_status(response1, 200)
        Assetions.assert_json_has_key(response1, "id")

        # в переменных email, password и user_id разложим соответствующие данные:
        email = register_data['email']
        firstname = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # АВТОРИЗАЦИЯ
        # пропишем часть с авторизацией
        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)  # авторизация по новым пользователем

        # вытаскиваем нужные нам значения:
        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, "x-csrf-token")

        # ИЗМЕНЕНИЕ
        # запрос на изменение данных
        # нам надо сделать запрос типа PUT. В запрос мы должны передать токен, авторизационный куки и поле, которое хотим менять новым значением, а менять мы будем firstname
        new_name = "Change Name"

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid},
                                   data={'firstName': new_name})

        Assetions.assert_code_status(response3, 200)

        # ПОЛУЧЕНИЕ
        # получение данных пользователя и сравнение его имени с новым

        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid})

        Assetions.assert_json_value_by_name(response4,
                                            'firstName',
                                            new_name,
                                            'Неверное имя пользователя после изменения')
