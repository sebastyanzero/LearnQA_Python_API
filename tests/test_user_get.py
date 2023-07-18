from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserGet(BaseCase):
    #python -m pytest -s tests/test_user_get.py -k "test_get_user_details_not_auth"
    def test_get_user_details_not_auth(self):
        #resp1=requests.get("https://playground.learnqa.ru/api/user/2")
        resp1=MyRequests.get("/user/2")
        #print(resp1.content)
        Assertions.assert_json_has_key(resp1, "username")
        Assertions.assert_json_has_not_key(resp1, "email")
        Assertions.assert_json_has_not_key(resp1, "firstName")
        Assertions.assert_json_has_not_key(resp1, "lastName")

    # python -m pytest -s tests/test_user_get.py -k "test_get_user_details_auth_as_same_user"
    def test_get_user_details_auth_as_same_user(self):
        data = {'email': 'vinkotov@example.com', 'password': '1234'}
        #resp1=requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        resp1=MyRequests.post("/user/login", data=data)
        auth_sid=self.get_cookie(resp1, "auth_sid")
        token=self.get_header(resp1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(resp1, "user_id")
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