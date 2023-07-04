import pytest
import requests
import json

class TestParam:
    # Порядок (agent, (platform, browser, device))
    uagent=[
        ('Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
         ('Mobile', 'No', 'Android')),
        ('Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1',
         ('Mobile', 'Chrome','iOS')),
        ('Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
         ('Googlebot','Unknown','Unknown')),
        ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0',
         ('Web','Chrome','No')),
        ('Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
         ('Mobile', 'No', 'iPhone'))]

    # 2, 3, 5 не тот ожидаемый результат
    @pytest.mark.parametrize('agent, expected_val',uagent)
    def test_param_user_agent(self,agent, expected_val):
        url='https://playground.learnqa.ru/ajax/api/user_agent_check'
        head={"User-Agent": agent}
        resp=requests.get(url, headers=head)
        print("\n")
        print(expected_val[0], expected_val[1], expected_val[2]) #что ожидаем (platform, browser, device)
        obj = json.loads(resp.text)
        print(obj["platform"], obj["browser"], obj["device"])  # что получили (platform, browser, device)
        assert "platform" in obj, "В ответе отсутствует параметр platform"
        assert "browser" in obj, "В ответе отсутствует параметр browser"
        assert "device" in obj, "В ответе отсутствует параметр device"

        assert expected_val[0] == obj["platform"], f'Для {agent} по platform получено неверное значение "{obj["platform"]}", ожидаемое "{expected_val[0]}"'
        assert expected_val[1] == obj["browser"], f'Для {agent} по browser получено неверное значение "{obj["browser"]}", ожидаемое "{expected_val[1]}"'
        assert expected_val[2] == obj["device"], f'Для {agent} по device получено неверное значение "{obj["device"]}", ожидаемое "{expected_val[2]}"'