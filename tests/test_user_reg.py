import pytest
import requests
from lib.base_case import BaseCase
#from lib.assertions import Assertions
import random, string

#python -m pytest -s tests/test_user_reg.py

class TestUserReg(BaseCase):
    def test_creat_user_with_existing_email(self):
        email='vinkotov@example.com'
        data={
            'password':'123',
            'username':'learnqa',
            'firstName':'learnqa',
            'lastName':'learnqa',
            'email':email
        }
        resp1=requests.post('https://playground.learnqa.ru/api/user/',data=data)
        assert resp1.status_code==400, f"Unexpected status code {resp1.status_code}"
        assert resp1.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {resp1.content}"
        #print(resp1.status_code)
        #print(resp1.content)

    def test_creat_user_with_uncor_email(self):
        email = 'nameexample.com'
        data = {
            'password': '123',
            'username': 'uname',
            'firstName': 'fname',
            'lastName': 'lname',
            'email': email
        }
        resp1 = requests.post('https://playground.learnqa.ru/api/user/', data=data)
        #print(resp1.status_code)
        #print(resp1.content)
        assert resp1.status_code == 400, f"Unexpected status code {resp1.status_code}"
        assert resp1.content.decode("utf-8") == f"Invalid email format", f"Unexpected response content {resp1.content}"

    users = [
        (None,'Uname', 'Fname', 'Lname', 'test@test.ts'),
        ('123456',None, 'Fname', 'Lname', 'test@test.ts'),
        ('123456','Uname', None, 'Lname', 'test@test.ts'),
        ('123456','Uname', 'Fname', None, 'test@test.ts'),
        ('123456','Uname', 'Fname', 'Lname', None),
        (None,None,None,None,None)]

    @pytest.mark.parametrize('userdate', users)
    def test_creat_user_with_param(self, userdate):
        data = {
            'password': userdate[0],
            'username': userdate[1],
            'firstName': userdate[2],
            'lastName': userdate[3],
            'email': userdate[4]
        }
        resp1 = requests.post('https://playground.learnqa.ru/api/user/', data=data)
        #print(resp1.status_code)
        #print(resp1.content)
        #print(resp1.text)
        assert resp1.status_code == 400, f"Unexpected status code {resp1.status_code}"
        assert f"The following required params are missed:" in resp1.content.decode("utf-8"), f"Unexpected response content {resp1.content}"

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
        resp1 = requests.post('https://playground.learnqa.ru/api/user/', data=data)
        #print(resp1.status_code)
        #print(resp1.content)
        assert resp1.status_code == 400, f"Unexpected status code {resp1.status_code}"
        assert resp1.content.decode("utf-8") == f"The value of 'username' field is too short", f"Unexpected response content {resp1.content}"

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
        resp1 = requests.post('https://playground.learnqa.ru/api/user/', data=data)
        #print(resp1.status_code)
        #print(resp1.content)
        assert resp1.status_code == 400, f"Unexpected status code {resp1.status_code}"
        assert resp1.content.decode("utf-8") == f"The value of 'username' field is too long", f"Unexpected response content {resp1.content}"