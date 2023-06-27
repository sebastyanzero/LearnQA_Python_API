import json
json_text='{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'
# Наша задача с помощью библиотеки “json”, которую мы показывали на занятии, распарсить нашу переменную json_text и
# вывести текст второго сообщения с помощью функции print.

obj=json.loads(json_text)
key0="messages"
position=1 # если укажем 0, то получим первое сообщение
key1="message" # если укажем timestamp, то получим дату и время сообщения

print(obj[key0][position][key1])


