import time
import json
import requests
import random

def send(n):
    url = ['http://localhost:5000/head', 'http://localhost:5000/legs', 'http://localhost:5000/wleft', 'http://localhost:5000/wright', 'http://localhost:5000/wfront', 'http://localhost:5000/wback', 'http://localhost:5000/sleft', 'http://localhost:5000/sright']    
    to_sv = url[n]
    dist_data = []
    for i in range(50):
        if n == 0:
            dist = random.randint(40,100)
        elif n == 1:
            dist = random.randint(300,400)
        elif n == 2 or n == 3:
            dist = random.randint(190,220)
        elif n == 4 or n == 5:
            dist = random.randint(290,320)
        dist_data.append(dist)
        print(dist)
        time.sleep(0.1)

    sendData = {"distance" : dist_data}
    header = {'Content-Type': 'application/json'}
    res = requests.post(to_sv, data=json.dumps(sendData).encode("utf-8"),headers=header)
    print("宛先：", to_sv)
    print("サーバからのステータスコード：", res.status_code)
    res.close()

n = int(input())
send(n)