import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import random, string
import allure
#from datetime import datetime

#python -m pytest -s tests/test_user_reg.py

@allure.epic("Registration cases")
class TestUserReg(BaseCase):

    # python -m pytest -s tests/test_user_reg.py -k "test_create_user_successfully"
    @allure.title("Создание юзера")
    @allure.description("Тест на успешную регистрацию пользователя")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_user_successfully(self):
        with allure.step('Регистрируем пользователя'):
            data=self.prepare_reg_data()
            resp1=MyRequests.post('/user/',data=data)
            #assert resp1.status_code==200, f"Unexpected status code {resp1.status_code}"
            Assertions.assert_code_status(resp1, 200)
            #print(resp.content)
            Assertions.assert_json_has_key(resp1, "id")

    @allure.title("Создание юзера с занятым e-mail")
    @allure.description("Тест на регистрацию пользователя с существующем в базе e-mail")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_creat_user_with_existing_email(self):
        email='vinkotov@example.com'
        data = self.prepare_reg_data(email)
        with allure.step('Регистрируем пользователя'):
            resp1=MyRequests.post('/user/',data=data)
            #assert resp1.status_code==400, f"Unexpected status code {resp1.status_code}"
            Assertions.assert_code_status(resp1, 400)
            assert resp1.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {resp1.content}"
            #print(resp1.status_code)
            #print(resp1.content)

    @allure.title("Создание юзера с некорректным e-mail")
    @allure.description("Неуспех при регистрации пользователя с некорректным e-mail")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_creat_user_with_uncor_email(self):
        email = 'nameexample.com'
        data = self.prepare_reg_data(email)
        with allure.step('Регистрируем пользователя'):
            resp1 = MyRequests.post('/user/', data=data)
            #print(resp1.status_code)
            #print(resp1.content)
            Assertions.assert_code_status(resp1, 400)
            #assert resp1.status_code == 400, f"Unexpected status code {resp1.status_code}"
            assert resp1.content.decode("utf-8") == f"Invalid email format", f"Unexpected response content {resp1.content}"

    users = [
        (None,'Uname', 'Fname', 'Lname', 'test@test.ts'),
        ('123456',None, 'Fname', 'Lname', 'test@test.ts'),
        ('123456','Uname', None, 'Lname', 'test@test.ts'),
        ('123456','Uname', 'Fname', None, 'test@test.ts'),
        ('123456','Uname', 'Fname', 'Lname', None),
        (None,None,None,None,None)]

    @allure.description("Тест на регистрацию пользователя с незаполненным полем")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link('https://playground.learnqa.ru/api/map', name='Подробнее по методам')
    @allure.issue('140', 'Pytest-flaky test retries shows like test steps')
    @allure.testcase('https://github.com/sebastyanzero/LearnQA_Python_API/blob/main/tests/test_user_reg.py',
                     'Test case here')
    @allure.title("Создание юзера с параметрами: {userdate}")
    @pytest.mark.parametrize('userdate', users)
    def test_creat_user_with_param(self, userdate):
        data = {
            'password': userdate[0],
            'username': userdate[1],
            'firstName': userdate[2],
            'lastName': userdate[3],
            'email': userdate[4]
        }
        with allure.step('Регистрируем пользователя'):
            resp1 = MyRequests.post('/user/', data=data)
            #print(resp1.status_code)
            #print(resp1.content)
            #print(resp1.text)
            Assertions.assert_code_status(resp1, 400)
            #assert resp1.status_code == 400, f"Unexpected status code {resp1.status_code}"
            assert f"The following required params are missed:" in resp1.content.decode("utf-8"), f"Unexpected response content {resp1.content}"

    @allure.title("Создание юзера с параметрами: {userdate}")
    @allure.description("Тест на регистрацию пользователя с username в 1 случайный символ")
    @allure.severity(allure.severity_level.NORMAL)
    def test_creat_user_name_1symbol(self):
        #rand = random.choice(string.ascii_letters)
        randsymbol = random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        #print(randsymbol)
        #email = 'nameexample.com'
        data = {
            'password': '123',
            'username': randsymbol,
            'firstName': 'fname',
            'lastName': 'lname',
            'email': 'name@example.com'
        }

        with allure.step('Регистрируем пользователя'):
            resp1 = MyRequests.post('/user/', data=data)
            #print(resp1.status_code)
            #print(resp1.content)
            Assertions.assert_code_status(resp1, 400)
            #assert resp1.status_code == 400, f"Unexpected status code {resp1.status_code}"
            assert resp1.content.decode("utf-8") == f"The value of 'username' field is too short", f"Unexpected response content {resp1.content}"

    @allure.title("Создание юзера с очень большим username")
    @allure.description("Тест на регистрацию пользователя с username в 251 символ")
    @allure.severity(allure.severity_level.NORMAL)
    def test_creat_user_longname(self):
        longrandname = ''.join(random.choices(string.ascii_letters, k=251))
        #print(longrandname)
        data = {
            'password': '123',
            'username': longrandname,
            'firstName': 'fname',
            'lastName': 'lname',
            'email': 'name@example.com'
        }
        with allure.step('Регистрируем пользователя'):
            resp1 = MyRequests.post('/user/', data=data)
            #print(resp1.status_code)
            #print(resp1.content)
            Assertions.assert_code_status(resp1, 400)
            #assert resp1.status_code == 400, f"Unexpected status code {resp1.status_code}"
            assert resp1.content.decode("utf-8") == f"The value of 'username' field is too long", f"Unexpected response content {resp1.content}"