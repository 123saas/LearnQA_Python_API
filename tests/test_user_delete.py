from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assetions
import time
import json
import allure

@allure.epic("Кейсы на удаление")
class TestUserDelete(BaseCase):
    @allure.title("Удаление пользователя с ID 2")
    @allure.description("Попытка удалить пользователя с ID 2. У пользвателей с ID = 1, 2, 3, 4 или 5 запрет на их удаление")
    # Тест 1 - попытка удалить пользователя по ID 2
    def test_delete_user_with_id_2(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        # АВТОРИЗАЦИЯ
        response1 = MyRequests.post("/user/login", data=data)
        # вытаскиваем нужные нам значения:
        auth_sid = self.get_cookie(response1, 'auth_sid')
        token = self.get_header(response1, "x-csrf-token")
        user_id = self.get_json_value(response1, "user_id")


        # УДАЛЕНИЕ
        response2 = MyRequests.delete(f"/user/{user_id}",
                                      headers={'x-csrf-token': token},
                                      cookies={'auth_sid': auth_sid})

        # Проверки
        Assetions.assert_code_status(response2, 400)
        assert response2.content.decode(
            "utf-8") == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"Непредвиденный содержание ответа {response2.content}" # проверка, что появилось данное сообщение

        # ПОЛУЧЕНИЕ
        response3 = MyRequests.get(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid})

        # Проверка, что пользователь не удален
        Assetions.assert_json_value_by_name(response3,
                                            'id',
                                            "2",
                                            f"Пользователь с id={user_id} удален!")

    @allure.title("Создание пользователя и его удаление")
    @allure.description(
        "В тесте:"
        "1. Создается пользователь;"
        "2. Происходит авторизация из-под него;"
        "3. Удаление данного пользователя;"
        "4. Попытка получения его данных по ID;"
        "5. Проверка, что пользователь действительно удален")
    @allure.tag("Создание", "Авторизация", "Удаление")
    # Тест 2 - Создать пользователя, авторизоваться из-под него, удалить, затем попробовать получить его данные по ID и убедиться, что пользователь действительно удален.
    def test_create_and_delete_user(self):
        # РЕГИСТРАЦИЯ
        register_data = self.prepare_registration_data()  # 1. подготовить данные для создания пользователей, в том числе и его имейла. Генерируем пользователя
        response1 = MyRequests.post("/user/", data=register_data)

        # убедимся, что на запрос, который мы послали сервер ответил кодом ответа 200 и что в ответе есть id нового пользователя:
        Assetions.assert_code_status(response1, 200)
        Assetions.assert_json_has_key(response1, "id")

        # в переменных email, password и user_id разложим соответствующие данные:
        email = register_data['email']
        password = register_data['password']

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
        user_id = self.get_json_value(response2, "user_id")

        # УДАЛЕНИЕ
        response3 = MyRequests.delete(f"/user/{user_id}",
                                      headers={'x-csrf-token': token},
                                      cookies={'auth_sid': auth_sid})


        # ПОЛУЧЕНИЕ
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid})


        # Проверки
        Assetions.assert_code_status(response4, 404)
        assert response4.content.decode(
            "utf-8") == "User not found", \
            f"Непредвиденный содержание ответа {response4.content}" # проверка, что появилось данное сообщение

    @allure.title("Удаление пользователя, будучи авторизованными другим пользователем")
    @allure.description(
        "В тесте:"
        "1. Создаются два пользователя;"
        "2. Происходит авторизация под двумя пользователями;"
        "3. Удаление второго пользователя по данным первого;"
        "4. Проверка, что оба пользователя не удалены")
    @allure.tag("Создание", "Авторизация", "Удаление")
    # Тест 3 - Удалить пользователя, будучи авторизованными другим пользователем.
    def test_delete_another_user(self):
        # РЕГИСТРАЦИЯ

        # Первый пользователь
        register_data_first = self.prepare_registration_data()
        response1_first_user = MyRequests.post("/user/", data=register_data_first)


        # убедимся, что на запрос, который мы послали сервер ответил кодом ответа 200 и что в ответе есть id нового пользователя:
        Assetions.assert_code_status(response1_first_user, 200)
        Assetions.assert_json_has_key(response1_first_user, "id")

        email_1 = register_data_first['email']
        password_1 = register_data_first['password']
        user_id_first = self.get_json_value(response1_first_user, "id")

        time.sleep(2)

        # Второй пользователь
        register_data_second = self.prepare_registration_data()
        response1_second_user = MyRequests.post("/user/", data=register_data_second)

        # убедимся, что на запрос, который мы послали сервер ответил кодом ответа 200 и что в ответе есть id нового пользователя:
        Assetions.assert_code_status(response1_second_user, 200)
        Assetions.assert_json_has_key(response1_second_user, "id")

        email_2 = register_data_second['email']
        password_2 = register_data_second['password']
        user_id_second = self.get_json_value(response1_second_user, "id")

        # АВТОРИЗАЦИЯ

        # Первый пользователь
        login_data_first = {
            'email': email_1,
            'password': password_1
        }

        response2_first_user = MyRequests.post("/user/login",
                                               data=login_data_first)  # авторизация по новым пользователем

        # вытаскиваем нужные нам значения:
        auth_sid_1 = self.get_cookie(response2_first_user, 'auth_sid')
        token_1 = self.get_header(response2_first_user, "x-csrf-token")

        # Второй пользователь
        login_data_second = {
            'email': email_2,
            'password': password_2
        }

        response2_second_user = MyRequests.post("/user/login",
                                                data=login_data_second)  # авторизация по новым пользователем

        # вытаскиваем нужные нам значения:
        auth_sid_2 = self.get_cookie(response2_second_user, 'auth_sid')
        token_2 = self.get_header(response2_second_user, "x-csrf-token")

        # УДАЛЕНИЕ
        #удаление второго пользователя при авторизации первым

        response3 = MyRequests.delete(f"/user/{user_id_second}",
                                      headers={'x-csrf-token': token_1},
                                      cookies={'auth_sid': auth_sid_1})

        Assetions.assert_code_status(response3, 200)

        # ПОЛУЧЕНИЕ
        # Первый пользователь
        response4_first_user = MyRequests.get(f"/user/{user_id_first}",
                                              headers={'x-csrf-token': token_1},
                                              cookies={'auth_sid': auth_sid_1})



        # проверка, что пользователь не удален
        Assetions.assert_code_status(response4_first_user, 200)
        Assetions.assert_content_type_header(response4_first_user, 'application/json') # ожидаемый результат "'application/json'", так как ожидается, что пользователь не удалился
        # Второй пользователь
        response4_second_user = MyRequests.get(f"/user/{user_id_second}",
                                               headers={'x-csrf-token': token_2},
                                               cookies={'auth_sid': auth_sid_2})


        # проверка, что пользователь не удален
        Assetions.assert_code_status(response4_second_user, 200)
        Assetions.assert_content_type_header(response4_second_user, 'application/json')












