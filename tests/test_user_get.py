from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure

@allure.epic("Info user cases")
class TestUserGet(BaseCase):
    #python -m pytest -s tests/test_user_get.py -k "test_get_user_details_not_auth"
    @allure.title("Инфа юзера без авторизации")
    @allure.description("Тест на получение информации юзера без авторизации")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("info")
    def test_get_user_details_not_auth(self):
        #resp1=requests.get("https://playground.learnqa.ru/api/user/2")
        with allure.step('Инфа пользователя'):
            resp1=MyRequests.get("/user/2")
        #print(resp1.content)
            Assertions.assert_json_has_key(resp1, "username")
            Assertions.assert_json_has_not_key(resp1, "email")
            Assertions.assert_json_has_not_key(resp1, "firstName")
            Assertions.assert_json_has_not_key(resp1, "lastName")

    # python -m pytest -s tests/test_user_get.py -k "test_get_user_details_auth_as_same_user"
    @allure.title("Инфа юзера под тем же пользоваталем")
    @allure.description("Тест на получение информации юзера им же")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("auth", "info")
    def test_get_user_details_auth_as_same_user(self):
        data = {'email': 'vinkotov@example.com', 'password': '1234'}
        #resp1=requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        with allure.step('Авторизуем пользователя'):
            resp1=MyRequests.post("/user/login", data=data)
            auth_sid=self.get_cookie(resp1, "auth_sid")
            token=self.get_header(resp1, "x-csrf-token")
            user_id_from_auth_method = self.get_json_value(resp1, "user_id")
        with allure.step('Инфа пользователя'):
            resp2=MyRequests.get(f"/user/{user_id_from_auth_method}",
                               headers={"x-csrf-token": token},
                               cookies={"auth_sid": auth_sid}
                               )

            expected_fields=["username","email","firstName","lastName"]
            Assertions.assert_json_has_keys(resp2, expected_fields)
        """
        Assertions.assert_json_has_key(resp2, "username")
        Assertions.assert_json_has_key(resp2, "email")
        Assertions.assert_json_has_key(resp2, "firstName")
        Assertions.assert_json_has_key(resp2, "lastName")
        """

    @allure.title("Инфа юзера под другим пользоваталем")
    @allure.description("Тест на получение информации юзера другим пользоваталем")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("auth", "info")
    def test_get_another_user_details(self):
        data = {'email': 'JQnZjk@example.com', 'password': '1234'}
        # 76039
        with allure.step('Авторизуем пользователя'):
            resp1=MyRequests.post("/user/login", data=data)
            auth_sid=self.get_cookie(resp1, "auth_sid")
            token=self.get_header(resp1, "x-csrf-token")
        #user_id_from_auth_method = self.get_json_value(resp1, "user_id")
        with allure.step('Инфа пользователя'):
            resp2=MyRequests.get(f"/user/2",
                               headers={"x-csrf-token": token},
                               cookies={"auth_sid": auth_sid}
                               )
            #print(resp2.content)
            #print(user_id_from_auth_method)
            #resp3 = MyRequests.get(f"/user/{user_id_from_auth_method}",
            #                       headers={"x-csrf-token": token},
            #                       cookies={"auth_sid": auth_sid}
            #                       )
            #print(resp3.content)
            expected_fields=["id","email","firstName","lastName"]
            #expected_fields3 = ["email", "firstName", "lastName"]
            # Проверяем, что вернуло username
            Assertions.assert_json_has_key(resp2, "username")
            # Проверяем, что отсутствуют "id","email","firstName","lastName"
            Assertions.assert_json_has_not_keys(resp2, expected_fields)
        #Assertions.assert_json_has_keys(resp3, expected_fields3)

