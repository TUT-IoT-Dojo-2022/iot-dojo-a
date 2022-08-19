import time
import json
import requests

def send():
    url = 'http://192.168.2.109:5000/height'
    dist_data = []
    for i in range(10):
        dist = 100
        print("range: mm ", dist)
        dist_data.append(dist)
        time.sleep(0.1)

    device = ["legs", "head", "side"]
    sendData = {"device" : device[1], "distance" : dist_data}
    header = {'Content-Type': 'application/json'}
    res = requests.post(url, data=json.dumps(sendData).encode("utf-8"),headers=header)
    print("サーバからのステータスコード：", res.status_code)
    res.close()

send()