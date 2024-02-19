
from lib.base_case import BaseCase
from lib.assertions import Assetions
from lib.my_requests import MyRequests
import time

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


# Попытаемся изменить данные пользователя, будучи неавторизованными
    def test_edit_user_details_not_auth(self):
        # РЕГИСТРАЦИЯ
        register_data = self.prepare_registration_data()  # 1. подготовить данные для создания пользователей, в том числе и его имейла. Генерируем пользователя
        response1 = MyRequests.post("/user/", data=register_data)

        # убедимся, что на запрос, который мы послали сервер ответил кодом ответа 200 и что в ответе есть id нового пользователя:
        Assetions.assert_code_status(response1, 200)
        Assetions.assert_json_has_key(response1, "id")

        # в переменных email, password и user_id разложим соответствующие данные:
        email = register_data['email']
        firstname = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # ИЗМЕНЕНИЕ ДАННЫХ

        new_name = "Change Name"

        response3 = MyRequests.put(f"/user/{user_id}", data={'firstName': new_name})


        Assetions.assert_code_status(response3, 400)
        assert response3.content.decode(
            "utf-8") == "Auth token not supplied", f"Непредвиденный содержание ответа {response3.content}"


# Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем
    def test_edit_another_user_detailing(self):

#РЕГИСТРАЦИЯ

# Первый пользователь
        register_data_first = self.prepare_registration_data()
        response1_first_user = MyRequests.post("/user/", data=register_data_first)
        print("response_first_user=", response1_first_user.content)

        #убедимся, что на запрос, который мы послали сервер ответил кодом ответа 200 и что в ответе есть id нового пользователя:
        Assetions.assert_code_status(response1_first_user, 200)
        Assetions.assert_json_has_key(response1_first_user, "id")

        email_1 = register_data_first['email']
        password_1 = register_data_first['password']
        firstname_1 = register_data_first['firstName']
        user_id_first = self.get_json_value(response1_first_user, "id")

        time.sleep(2)

# Второй пользователь
        register_data_second = self.prepare_registration_data()
        response1_second_user = MyRequests.post("/user/", data=register_data_second)

        #убедимся, что на запрос, который мы послали сервер ответил кодом ответа 200 и что в ответе есть id нового пользователя:
        Assetions.assert_code_status(response1_second_user, 200)
        Assetions.assert_json_has_key(response1_second_user, "id")

        email_2 = register_data_second['email']
        password_2 = register_data_second['password']
        firstname_2 = register_data_second['firstName']
        user_id_second = self.get_json_value(response1_second_user, "id")

#АВТОРИЗАЦИЯ

# Первый пользователь
        login_data_first = {
                    'email': email_1,
                    'password': password_1
                }

        response2_first_user = MyRequests.post("/user/login", data=login_data_first)  # авторизация по новым пользователем

        # вытаскиваем нужные нам значения:
        auth_sid_1 = self.get_cookie(response2_first_user, 'auth_sid')
        token_1 = self.get_header(response2_first_user, "x-csrf-token")

# Второй пользователь
        login_data_second = {
            'email': email_2,
            'password': password_2
        }

        response2_second_user = MyRequests.post("/user/login", data=login_data_second)  # авторизация по новым пользователем

        # вытаскиваем нужные нам значения:
        auth_sid_2 = self.get_cookie(response2_second_user, 'auth_sid')
        token_2 = self.get_header(response2_second_user, "x-csrf-token")


#ИЗМЕНЕНИЕ
            # запрос на изменение данных
            # нам надо сделать запрос типа PUT. В запрос мы должны передать токен, авторизационный куки и поле, которое хотим менять новым значением, а менять мы будем firstname
        new_name = "Change Name second user"

        response3 = MyRequests.put(f"/user/{user_id_second}",
                                   headers={'x-csrf-token': token_1},
                                   cookies={'auth_sid': auth_sid_1},
                                   data={'firstName': new_name})

        Assetions.assert_code_status(response3, 200)

# ПОЛУЧЕНИЕ
# Первый пользователь
        response4_first_user = MyRequests.get(f"/user/{user_id_first}",
                                   headers={'x-csrf-token': token_1},
                                   cookies={'auth_sid': auth_sid_1})

        # проверка, что имя не изменилось
        Assetions.assert_code_status(response4_first_user, 200)
        Assetions.assert_json_value_by_name(response4_first_user,
                                            'firstName',
                                            firstname_1,
                                            f"Имя пользователя с id = {user_id_first} поменялось на {new_name}")

# Второй пользователь
        response4_second_user = MyRequests.get(f"/user/{user_id_second}",
                                   headers={'x-csrf-token': token_2},
                                   cookies={'auth_sid': auth_sid_2})

        # проверка, что имя не изменилось
        Assetions.assert_code_status(response4_second_user, 200)
        Assetions.assert_json_value_by_name(response4_second_user,
                                            'firstName',
                                            firstname_2,
                                            f"Имя пользователя с id = {user_id_second} поменялось на {new_name}")


# Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @
    def test_edit_user_email_without_at_in_email(self):
# РЕГИСТРАЦИЯ
        register_data = self.prepare_registration_data() # 1. подготовить данные для создания пользователей, в том числе и его имейла. Генерируем пользователя
        response1 = MyRequests.post("/user/", data=register_data)

        #убедимся, что на запрос, который мы послали сервер ответил кодом ответа 200 и что в ответе есть id нового пользователя:
        Assetions.assert_code_status(response1, 200)
        Assetions.assert_json_has_key(response1, "id")

        # в переменных email, password и user_id разложим соответствующие данные:
        email = register_data['email']
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
        new_email = "vinkotovexample.com"

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid},
                                   data={'email': new_email})

        Assetions.assert_code_status(response3, 400)

        # ПОЛУЧЕНИЕ
        # получение данных пользователя и сравнение его имени с новым

        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid})

        Assetions.assert_json_value_by_name(response4,
                                            'email',
                                            email,
                                            'Invalid email format')



# Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем, на очень короткое значение в один символ
    def test_edit_name_on_one_character(self):
        # РЕГИСТРАЦИЯ
        register_data = self.prepare_registration_data()  # 1. подготовить данные для создания пользователей, в том числе и его имейла. Генерируем пользователя
        response1 = MyRequests.post("/user/", data=register_data)

        # убедимся, что на запрос, который мы послали сервер ответил кодом ответа 200 и что в ответе есть id нового пользователя:
        Assetions.assert_code_status(response1, 200)
        Assetions.assert_json_has_key(response1, "id")

        # в переменных email, password и user_id разложим соответствующие данные:
        email = register_data['email']
        password = register_data['password']
        firstname = register_data['firstName']
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
        new_name = "v"

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid},
                                   data={'email': new_name})

        Assetions.assert_code_status(response3, 400)

        # ПОЛУЧЕНИЕ
        # получение данных пользователя и сравнение его имени с новым

        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid})

        Assetions.assert_json_value_by_name(response4,
                                            'firstName',
                                            firstname,
                                            "The value of 'firstName' field is too short")


