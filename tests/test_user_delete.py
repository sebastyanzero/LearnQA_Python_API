import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import time
import allure
import random, string

@allure.epic("Delete cases")
class TestUserDelete(BaseCase):
    @allure.title("Удаление пользователя с ИД=2")
    @allure.description("Тест на попытку удаления пользователя с ИД=2")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link('https://playground.learnqa.ru/api/map', name='Подробнее по методам')
    @allure.issue('140', 'Ссылка на систему управления ошибками')
    @allure.testcase('https://github.com/sebastyanzero/LearnQA_Python_API/blob/main/tests/test_user_delete.py',
                     'Test case here')
    @allure.tag("reg", "del", "auth", "info")
    def test_del_user_id2(self):
        # login
        login_data = {'email': 'vinkotov@example.com',
            'password': '1234'}
        resp1 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(resp1, "auth_sid")
        token = self.get_header(resp1, "x-csrf-token")
        #delete

        resp2 = MyRequests.delete("/user/2",
                            headers={"x-csrf-token": token},
                            cookies={"auth_sid": auth_sid})
        #print(resp2.status_code)
        #print(resp2.content)
        Assertions.assert_code_status(resp2,400)
        assert resp2.content.decode("utf-8") == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", f"Unexpected response content {resp2.content}"

        # info user 2
        resp3 = MyRequests.get(f"/user/2",
                               headers={"x-csrf-token": token},
                               cookies={"auth_sid": auth_sid})
        #print(resp3.content)
        Assertions.assert_code_status(resp3, 200)
        # Проверяем, что по пользователю есть инфа
        #Assertions.assert_json_value_by_name(resp3, "username","Vitaliy")
        expected_fields = ["id","username", "email", "firstName", "lastName"]
        expected_value=["2","Vitaliy","vinkotov@example.com","Vitalii","Kotov"]
        for i in range(0,5):
            Assertions.assert_json_value_by_name(resp3,expected_fields[i],expected_value[i],f"Wrong values for '{expected_fields[i]}'")

        # Авторизуемся для проверки работы учётной записи
        resp4 = MyRequests.post("/user/login", data=login_data)
        Assertions.assert_code_status(resp4, 200)
        Assertions.assert_json_value_by_name(resp4,"user_id",2,"Не тот код")

    @allure.title("Удаление пользователя самим собой")
    @allure.description("Тест на попытку удаления пользователя самим собой")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("reg", "del", "auth", "info")
    def test_del_created_user(self):
        # creat user
        register_data = self.prepare_reg_data()
        with allure.step('Регистрируем пользователя'):
            resp1 = MyRequests.post("/user/", data=register_data)
            Assertions.assert_code_status(resp1, 200)
            Assertions.assert_json_has_key(resp1, "id")
        password = register_data['password']
        #first_name = register_data['firstName']
        email = register_data['email']
        user_id = self.get_json_value(resp1, "id")
        #usernames = register_data['username']

        # login
        login_data = {'email': email,
                      'password': password}
        with allure.step('Авторизуем пользователя'):
            resp2 = MyRequests.post("/user/login", data=login_data)
            auth_sid = self.get_cookie(resp2, "auth_sid")
            token = self.get_header(resp2, "x-csrf-token")

        # delete
        with allure.step('Удаляем пользователя'):
            resp3 = MyRequests.delete(f"/user/{user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})
            Assertions.assert_code_status(resp3, 200)

        # info user
        with allure.step('Инфа пользователя'):
            resp4 = MyRequests.get(f"/user/{user_id}")
            Assertions.assert_code_status(resp4, 404)
            assert resp4.content.decode("utf-8") == "User not found", f"Unexpected response content {resp4.content}"

        # login 2
        login_data = {'email': email,
                      'password': password}
        with allure.step('Авторизуем пользователя'):
            resp5 = MyRequests.post("/user/login", data=login_data)
            Assertions.assert_code_status(resp5, 400)
            assert resp5.content.decode("utf-8") == "Invalid username/password supplied", f"Unexpected response content {resp5.content}"
        #print(resp5.status_code)
        #print(resp5.content)

    @allure.title("Удаление пользователя другим пользователем")
    @allure.description("Тест на попытку удаления пользователя авторизованным другим пользователем")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("reg", "del", "auth", "info")
    def test_del_another_user(self):
        # creat user for delete
        register_data = self.prepare_reg_data()
        with allure.step('Регистрируем пользователя1'):
            resp1 = MyRequests.post("/user/", data=register_data)
            Assertions.assert_code_status(resp1, 200)
            Assertions.assert_json_has_key(resp1, "id")
        password = register_data['password']
        first_name = register_data['firstName']
        email = register_data['email']
        user_id = self.get_json_value(resp1, "id")
        usernames = register_data['username']

        time.sleep(1)

        # creat user for auth
        register_data2 = self.prepare_reg_data()
        with allure.step('Регистрируем пользователя2'):
            resp1a = MyRequests.post("/user/", data=register_data2)
            Assertions.assert_code_status(resp1a, 200)
            Assertions.assert_json_has_key(resp1a, "id")
        password2 = register_data2['password']
        email2 = register_data2['email']
        user_id2 = self.get_json_value(resp1a, "id")

        # login Автоизуемся под 2м аккаунтом
        login_data = {'email': email2,
                      'password': password2}
        with allure.step('Авторизуем пользователя2'):
            resp2 = MyRequests.post("/user/login", data=login_data)
            auth_sid = self.get_cookie(resp2, "auth_sid")
            token = self.get_header(resp2, "x-csrf-token")
        # delete Указываем ИД первого аккаунта
        with allure.step('Пользователь2 указывает id Пользователя1 для удаления'):
            resp3 = MyRequests.delete(f"/user/{user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})
            Assertions.assert_code_status(resp3, 200)

        # info user Инфо по "удалёеному". Он не удалится
        with allure.step('Инфа Пользователь1'):
            resp4 = MyRequests.get(f"/user/{user_id}")
            Assertions.assert_code_status(resp4, 200)
            Assertions.assert_json_has_key(resp4,"username")

        # info user2 Инфо под тем кем удаляли. По факту удаляется тот акк, который вызвал метод.
        with allure.step('Инфа Пользователь2'):
            resp4a = MyRequests.get(f"/user/{user_id2}")
            #print(resp4a.status_code, " - ", user_id2)
            #print(resp4a.content, " - ", user_id2)
            Assertions.assert_code_status(resp4a, 404)
            assert resp4a.content.decode("utf-8") == "User not found", f"Unexpected response content {resp4.content}"

        # login Пытаемся авторизоваться под тем кого пыталисб удалить. Акк остался
        login_data2 = {'email': email,
                      'password': password}
        with allure.step('Авторизация под Пользователь2'):
            resp5= MyRequests.post("/user/login", data=login_data2)
            #print(resp5.status_code)
            #print(resp5.content)
            Assertions.assert_code_status(resp5, 200)
            Assertions.assert_json_value_by_name(resp5,"user_id",int(user_id), "Another id")

        # login Пытаемся авторизоваться под тем кто удалился. Им пытались удалить
        with allure.step('Авторизация под Пользователь1'):
            login_data3 = {'email': email2,
                          'password': password2}
            resp5a= MyRequests.post("/user/login", data=login_data3)
            Assertions.assert_code_status(resp5a, 400)
            assert resp5a.content.decode(
                "utf-8") == "Invalid username/password supplied", f"Unexpected response content {resp4.content}"
            #print(resp5a.status_code)
            #print(resp5a.content)