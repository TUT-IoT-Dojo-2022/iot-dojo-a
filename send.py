import time
import ujson
import urequests
from machine import I2C,Pin
from vl53l1x import VL53L1X

I2C_SCL_PIN = 22
I2C_SDA_PIN = 21
p5 = Pin(5,Pin.OUT)
p5.on()
i2c = I2C(scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN))
distance = VL53L1X(i2c)

def send():
    url = 'http://192.168.2.109:5000/height'
    dist_data = []
    count = 0
    while count < 200:
        try:
            dist = distance.read()
            print("range: mm ", distance.read())
            dist_data.append(dist)
            time.sleep(0.1)
            count += 1
        except:
            count += 0

    device = ["legs", "head", "side"]
    sendData = {"device" : device[1], "distance" : dist_data}
    header = {'Content-Type': 'application/json'}
    res = urequests.post(url, data=ujson.dumps(sendData).encode("utf-8"),headers=header)
    print("サーバからのステータスコード：", res.status_code)
    res.close()
    

send()