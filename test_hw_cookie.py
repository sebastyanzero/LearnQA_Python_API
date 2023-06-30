import requests
class Testhwcookie:
    def test_hw1(self):
        url='https://playground.learnqa.ru/api/homework_cookie'
        resp=requests.post(url)
        # print(resp.cookies)
        print(dict(resp.cookies)) # Выводим куки {'ключ': 'значение'} или print(resp.cookies.get_dict())
        # cookie_n = resp.cookies.keys() # получаем список с названием ключей
        # cookie_n1 = len(resp.cookies.keys()) # количество элементов в списке ключей
        cookie_name = resp.cookies.keys()[0] # получаем значение 1го элемента списка
        print("Ключ\t", cookie_name)
        # assert "HomeWork" in resp.cookies.keys(), f"Получено имя ключа {cookie_name} отличное от 'HomeWork'"
        assert cookie_name == "HomeWork", f"Получено имя ключа {cookie_name} отличное от 'HomeWork'"
        cookie_v = resp.cookies.get(cookie_name)
        print("Значение",cookie_v)
        assert cookie_v=="hw_value", f"Получено значение {cookie_v} отличное от 'hw_value' для ключа {cookie_name}"