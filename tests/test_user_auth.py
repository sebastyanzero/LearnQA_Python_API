import pytest
import requests
from lib.base_case import  BaseCase
from lib.assertions import Assertions

class TestUserAuth(BaseCase):
    exl_param=[
        ("no_cookie"),
        ("no_token")
    ]

    def setup_method(self):
        data = {'email': 'vinkotov@example.com', 'password': '1234'}
        url1 = 'https://playground.learnqa.ru/api/user/login'
        resp1 = requests.post(url1, data=data)

        self.auth_sid = self.get_cookie(resp1,"auth_sid")
        self.token = self.get_header(resp1,"x-csrf-token")
        self.user_id1 = self.get_json_value(resp1,"user_id")

    def test_auth_user(self):

        url2='https://playground.learnqa.ru/api/user/auth'
        resp2=requests.get(url2,
                           headers={"x-csrf-token":self.token},
                           cookies={"auth_sid":self.auth_sid})

        Assertions.assert_json_value_by_name(
            resp2,
            "user_id",
            self.user_id1,
            "User id from auth method is not equal to user id from check method"
        )

    @pytest.mark.parametrize("condition",exl_param)
    def test_negative_auth_check(self, condition):
        url2 = 'https://playground.learnqa.ru/api/user/auth'
        if condition=="no_cookie":
            resp2 = requests.get(url2,
                                 headers={"x-csrf-token": self.token})
        else:
            resp2 = requests.get(url2,
                                 cookies={"auth_sid": self.auth_sid})

        Assertions.assert_json_value_by_name(
            resp2,
            "user_id",
            0,
            f"User is authorized with condition '{condition}'"
        )
