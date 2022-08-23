import time
import json
import requests

def send():
    url = ['http://localhost:5000/head', 'http://localhost:5000/legs', 'http://localhost:5000/wleft', 'http://localhost:5000/wright', 'http://localhost:5000/sleft', 'http://localhost:5000/sright']
    to_sv = url[2]
    dist_data = []
    for i in range(10):
        dist = 180
        dist_data.append(dist)
        time.sleep(0.1)

    sendData = {"distance" : dist_data}
    header = {'Content-Type': 'application/json'}
    res = requests.post(to_sv, data=json.dumps(sendData).encode("utf-8"),headers=header)
    print("宛先：", to_sv)
    print("サーバからのステータスコード：", res.status_code)
    res.close()

send()