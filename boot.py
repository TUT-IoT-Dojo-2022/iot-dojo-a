import time
import utime
import ujson
import network
import webrepl
import urequests
from machine import SoftI2C,Pin
from vl53l1x import VL53L1X

SSID_NAME = "iot-dojo"
SSID_PASS = "6a5jxurvjxha"
I2C_SCL_PIN = 22
I2C_SDA_PIN = 21
p5 = Pin(5,Pin.OUT)
p5.on()
i2c = SoftI2C(scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN))
distance = VL53L1X(i2c)

def send():
    url = 'http://192.168.2.100:5000/left'
    dist_data = []
    count = 0
    while count < 100:
        try:
            dist = distance.read()
            print("range: mm ", distance.read())
            dist_data.append(dist)
            count += 1
            time.sleep(0.01)
        except:
            count += 0

    sendData = {"device" : 1, "distance" : dist_data}
    header = {'Content-Type': 'application/json'}
    print("Measurements complete! Please step aside...")
    time.sleep(1)
    res = urequests.post(url, data=ujson.dumps(sendData).encode("utf-8"),headers=header)
    print("サーバからのステータスコード：", res.status_code)
    res.close()

def connect_wifi(ssid, passkey, timeout=10):
    wifi= network.WLAN(network.STA_IF)
    if wifi.isconnected():
        print('already Connected. connect skip')
        return wifi
    else :
        wifi.active(True)
        count = 0
        while count < 5:
            try:
                wifi.connect(ssid, passkey)
                break
            except:
                utime.sleep(3)
                count += 1
        while not wifi.isconnected() and timeout > 0:
            print('.')
            utime.sleep(1)
            timeout -= 1
    
    if wifi.isconnected():
        print('Connected')
        webrepl.start(password='1234')
        return wifi
    else:
        print('Connection failed!')
        return ''

if __name__ == '__main__':
    wifi_dojo = connect_wifi(SSID_NAME, SSID_PASS)
    while True:
        send()
        time.sleep(1)
