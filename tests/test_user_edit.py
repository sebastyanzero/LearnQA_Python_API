from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserEdit(BaseCase):

#python -m pytest -s tests/test_user_edit.py

    def test_edit_just_created_user(self):
        #register
        register_data= self.prepare_reg_data()
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


    #Попытаемся изменить данные пользователя, будучи неавторизованными
    #python -m pytest -s tests/test_user_edit.py -k "test_edit_user_as_noauth"
    def test_edit_name_user_as_noauth(self):
        #creat user
        register_data = self.prepare_reg_data()
        resp1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(resp1, 200)
        Assertions.assert_json_has_key(resp1, "id")
        password = register_data['password']
        first_name = register_data['firstName']
        email = register_data['email']
        user_id = self.get_json_value(resp1, "id")
        usernames = register_data['username']

        #edit
        new_name="Changed Name"

        resp3 =MyRequests.put(f"/user/{user_id}", data={"username":new_name})
        Assertions.assert_code_status(resp3, 400)
        assert resp3.content.decode("utf-8") == "Auth token not supplied", f"Unexpected response content {resp3.content}"
        print(resp3.status_code)

        # get
        resp4 = MyRequests.get(f"/user/{user_id}")
        print(resp4.status_code)
        print(resp4.content)
        Assertions.assert_json_has_key(resp4, "username")
        Assertions.assert_code_status(resp4,200)
        #То что старое значение
        Assertions.assert_json_value_by_name(resp4,"username",usernames,"Ошибка! Значение username изменилось." )

    def test_edit_user_as_noauth2(self):
        # creat user
        register_data = self.prepare_reg_data()
        resp1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(resp1, 200)
        Assertions.assert_json_has_key(resp1, "id")
        password = register_data['password']
        first_name = register_data['firstName']
        email = register_data['email']
        user_id = self.get_json_value(resp1, "id")
        usernames = register_data['username']

        # edit
        new_value = "Changed Name"

        resp3 = MyRequests.put(f"/user/{user_id}", data={"first_name": new_value})
        Assertions.assert_code_status(resp3, 400)
        assert resp3.content.decode(
            "utf-8") == "Auth token not supplied", f"Unexpected response content {resp3.content}"
        print(resp3.status_code)

        # авторизуемся, чтобы увидеть все поля
        login_data={
            'email':email,
            'password':password
        }
        resp2=MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(resp2, "auth_sid")
        token = self.get_header(resp2, "x-csrf-token")

        # get
        resp4 = MyRequests.get(f"/user/{user_id}",
                            headers={"x-csrf-token": token},
                            cookies={"auth_sid": auth_sid})
        print(resp4.status_code)
        print(resp4.content)
        Assertions.assert_code_status(resp4, 200)
        # То что старое значение
        Assertions.assert_json_value_by_name(resp4, "firstName", first_name, "Ошибка! Значение username изменилось.")

    #Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем
#python -m pytest -s tests/test_user_edit.py -k "test_edit_user_as_auth_another_user"
    def test_edit_user_as_auth_another_user(self):
        #{"id":"76064","username":"learnqa","email":"learnqa07192023164849@example.com","firstName":"learnqa","lastName":"learnqa"}

        # creat user, которого будем изменять
        register_data = self.prepare_reg_data()
        resp1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(resp1, 200)
        Assertions.assert_json_has_key(resp1, "id")
        user_id = self.get_json_value(resp1, "id")
        # login
        login_data = {
            'email': "learnqa07192023164849@example.com",
            'password': '123'
        }
        resp2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(resp2, "auth_sid")
        token = self.get_header(resp2, "x-csrf-token")

        # edit
        new_name = "Changed Name"

        resp3 = MyRequests.put(f"/user/{user_id}",
                               headers={"x-csrf-token": token},
                               cookies={"auth_sid": auth_sid},
                               data={"firstName": new_name})
        #Assertions.assert_code_status(resp3, 200)
        print(resp3.status_code)
        print(resp3.text)

        # login авторизуемся под тем, кого изменяли
        login_data = {
            'email': register_data['email'],
            'password': register_data['password']
        }
        resp4 = MyRequests.post("/user/login", data=login_data)
        auth_sid4 = self.get_cookie(resp4, "auth_sid")
        token4 = self.get_header(resp4, "x-csrf-token")

        # get
        resp5 = MyRequests.get(f"/user/{user_id}",
                               headers={"x-csrf-token": token4},
                               cookies={"auth_sid": auth_sid4})

        #print(resp5.status_code)
        #print(resp5.text)
        Assertions.assert_code_status(resp5,200)
        Assertions.assert_json_value_by_name(resp5,
                                             "firstName",
                                             register_data['firstName'],
                                             "The firstName has changed after edit")

   ##python -m pytest -s tests/test_user_edit.py -k "test_edit_uncor_email_created_user"
    #Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @
    def test_edit_uncor_email_created_user(self):
        #register
        register_data= self.prepare_reg_data()
        resp1=MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(resp1, 200)
        Assertions.assert_json_has_key(resp1,"id")
        password = register_data['password']
        email = register_data['email']
        user_id = self.get_json_value(resp1,"id")
        #login
        login_data={
            'email':email,
            'password':password
        }
        resp2=MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(resp2, "auth_sid")
        token = self.get_header(resp2, "x-csrf-token")

        #edit
        new_email="Changed.email"

        resp3 =MyRequests.put(f"/user/{user_id}",
                            headers={"x-csrf-token": token},
                            cookies={"auth_sid": auth_sid},
                            data={"email":new_email})
        Assertions.assert_code_status(resp3, 400)
        assert resp3.content.decode('utf-8')=='Invalid email format', f"Text: Invalid email format {new_email}"
        #get
        resp4=MyRequests.get(f"/user/{user_id}",
                            headers={"x-csrf-token": token},
                            cookies={"auth_sid": auth_sid})
        #print(resp4.status_code)
        #print(resp4.text)
        Assertions.assert_code_status(resp4,200)
        Assertions.assert_json_value_by_name(resp4,
                                             "email",
                                             email,
                                             "Email changed after edits")

#python -m pytest -s tests/test_user_edit.py -k "test_edit_short_name_user"
    #Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем, на очень короткое значение в один символ
    def test_edit_short_name_user(self):
        # register
        register_data = self.prepare_reg_data()
        resp1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(resp1, 200)
        Assertions.assert_json_has_key(resp1, "id")
        password = register_data['password']
        email = register_data['email']
        user_id = self.get_json_value(resp1, "id")
        # login
        login_data = {
            'email': email,
            'password': password
        }
        resp2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(resp2, "auth_sid")
        token = self.get_header(resp2, "x-csrf-token")

        # edit
        newfirstname = "q"

        resp3 = MyRequests.put(f"/user/{user_id}",
                               headers={"x-csrf-token": token},
                               cookies={"auth_sid": auth_sid},
                               data={"firstName": newfirstname})
        Assertions.assert_code_status(resp3, 400)
        assert resp3.content.decode('utf-8') == '{"error":"Too short value for field firstName"}',\
            f"Text: Too short value for field firstName: {newfirstname}"
        # get
        resp4 = MyRequests.get(f"/user/{user_id}",
                               headers={"x-csrf-token": token},
                               cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(resp4, 200)
        Assertions.assert_json_value_by_name(resp4,
                                             "firstName",
                                             register_data['firstName'],
                                             "Too short value for field firstName")