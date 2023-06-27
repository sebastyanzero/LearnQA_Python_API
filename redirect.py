#Необходимо написать скрипт, который создает GET-запрос на метод: https://playground.learnqa.ru/api/long_redirect
#С помощью конструкции response.history необходимо узнать, сколько редиректов происходит
# от изначальной точки назначения до итоговой. И какой URL итоговый.
import requests
head= {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.2.625 Yowser/2.5 Safari/537.36"}
resp=requests.get("https://playground.learnqa.ru/api/long_redirect", headers=head, allow_redirects=True)
count_redir=len(resp.history) #считаем количество
#Перебираем все исторические записи
for i in range(count_redir):
    print(f"{i+1}-й", resp.history[i].status_code, resp.history[i].url)
#Выводим результат
print(f"Всего редиректов {count_redir}, итоговый URL {resp.url}")

