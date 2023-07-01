import requests
class Testhwhead:
    def test_hw2(self):
        url='https://playground.learnqa.ru/api/homework_header'
        resp=requests.post(url)
        print(resp.headers) # полное содержимое head ответа, ключ: значение
        """ # кол-во ключей
        resp_count = len(resp.headers) 
        print(resp_count)
        """
        resp_key_h = list(resp.headers.keys()) # список всех ключей
        # print(resp_key_h)  # выводим список всех ключей
        """ #Вывод ключей и их значений через цикл
        for i in resp_key_h:
            print(i," - ",resp.headers[i])
        """
        actual_key_n ="x-secret-homework-header"
        assert actual_key_n in resp_key_h, f"В заголовке ответа нет ключа '{actual_key_n}'"
        actual_key_v = "Some secret value"
        assert actual_key_v==resp.headers[actual_key_n], f"Значение '{resp.headers[actual_key_n]}' для ключа " \
                                                         f"'{actual_key_n}' не совпадает с '{actual_key_v}'"
        print(actual_key_n, " - ", resp.headers[actual_key_n])