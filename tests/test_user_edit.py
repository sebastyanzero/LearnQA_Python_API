from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserEdit(BaseCase):

#python -m pytest -s tests/test_user_edit.py

    def test_edit_just_created_user(self):
        #register
        register_data= self.prepare_reg_data()
        #resp1=requests.post("https://playground.learnqa.ru/api/user/", data=register_data)
        resp1=MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(resp1, 200)
        Assertions.assert_json_has_key(resp1,"id")
        password = register_data['password']
        first_name = register_data['firstName']
        email = register_data['email']
        user_id = self.get_json_value(resp1,"id")
        #login
        login_data={
            'email':email,
            'password':password
        }
        #resp2=requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        resp2=MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(resp2, "auth_sid")
        token = self.get_header(resp2, "x-csrf-token")

        #edit
        new_name="Changed Name"

        resp3 =MyRequests.put(f"/user/{user_id}",
                            headers={"x-csrf-token": token},
                            cookies={"auth_sid": auth_sid},
                            data={"firstName":new_name})
        Assertions.assert_code_status(resp3, 200)

        #get
        resp4=MyRequests.get(f"/user/{user_id}",
                            headers={"x-csrf-token": token},
                            cookies={"auth_sid": auth_sid})
        #Assertions.assert_code_status(resp4,200)
        Assertions.assert_json_value_by_name(resp4,
                                             "firstName",
                                             new_name,
                                             "Wrong name of the user after edit")
