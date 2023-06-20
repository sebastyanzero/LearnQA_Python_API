import requests

resp=requests.get("https://playground.learnqa.ru/api/get_text")
print(resp.text)