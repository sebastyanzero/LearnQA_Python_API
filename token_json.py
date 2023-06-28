import requests
import json
import time
# Делаем первый запрос без токена
resp1=requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
obj=json.loads(resp1.text)
utoken=obj["token"] # записали значение токена
utime=obj["seconds"] # записали время
print(resp1.text)
token1={"token":utoken}
time.sleep(1) #можно убрать, просто сделал задержку в 1 секунду
# Делаем второй запрос с токеном до завершения задачи
resp1=requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=token1)
print(resp1.text)
time.sleep(utime+1) # +1 секунда про запас
# Делаем третий запрос с токеном после завершения задачи
resp1=requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=token1)
print(resp1.text)
status_val=json.loads(resp1.text)["status"]
result_val=json.loads(resp1.text)["result"]
if 'result' in resp1.text and status_val=="Job is ready":
    print(f"Успех! Поле result в ответе есть со значением={result_val} и статусом задачи '{status_val}'")
else:
    print("Что-то пошло не так")
"""
# Делаем четвёртый запрос с несуществующим токеном
resp4=requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token":"fake4token"})
print(resp4.text)
"""