import time
import ujson
import urequests
from machine import SoftI2C,Pin
from vl53l1x import VL53L1X

I2C_SCL_PIN = 22
I2C_SDA_PIN = 21
p5 = Pin(5,Pin.OUT)
p5.on()
i2c = SoftI2C(scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN))
distance = VL53L1X(i2c)

def send():
    url = 'http://192.168.2.105:5000/legs'
    dist_data = []
    count = 0
    while count < 100:
        try:
            dist = distance.read()
            #print("range: mm ", distance.read())
            dist_data.append(dist)
            count += 1
            time.sleep(0.1)
        except:
            count += 0

    sendData = {"device" : 2, "distance" : dist_data}
    header = {'Content-Type': 'application/json'}
    print("Measurements complete! Please step aside...")
    time.sleep(1)
    res = urequests.post(url, data=ujson.dumps(sendData).encode("utf-8"),headers=header)
    print("サーバからのステータスコード：", res.status_code)
    res.close()

if __name__ == '__main__':
    send()