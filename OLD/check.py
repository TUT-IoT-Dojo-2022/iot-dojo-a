import time
import json
import requests
import random

def send(n):
    n = 0
    url = ['http://192.168.2.100:5000/head', 'http://192.168.2.100:5000/legs', 'http://192.168.2.100:5000/left', 'http://192.168.2.100:5000/right']    
    while True:
        to_sv = url[n]
        dist_data = []
        for i in range(100):
            if n == 0:
                dist = random.randint(10,30)
            elif n == 1:
                dist = random.randint(100,300)
            elif n >= 2:
                dist = random.randint(200,400)
            dist_data.append(dist)
        
        n += 1
        if n > 3:
            n = 0

        sendData = {"distance" : dist_data}
        header = {'Content-Type': 'application/json'}
        res = requests.post(to_sv, data=json.dumps(sendData).encode("utf-8"),headers=header)
        print("宛先：", to_sv)
        print("サーバからのステータスコード：", res.status_code)
        res.close()

        time.sleep(0.1)

n = int(input())
send(n)