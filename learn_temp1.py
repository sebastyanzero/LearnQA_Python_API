from json.decoder import JSONDecodeError
import requests
"""
resp=requests.get("https://playground.learnqa.ru/api/get_text")
print(resp.text)

try:
    pars_resp_t=resp.json()
    print(pars_resp_t)
except JSONDecodeError:
    print("Response is not JSON format")

""" #2
resp=requests.get("https://playground.learnqa.ru/api/hello", params={"name":"Rootadmin"})
print(resp)

pars_resp_t=resp.json()
print(pars_resp_t["answer"])
"""

""" #1
#payload={"name":"User"}
#resph=requests.get("https://playground.learnqa.ru/api/hello", params=payload)
#print(resph.text)
#"""