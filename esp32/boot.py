import utime
import network
import webrepl

SSID_NAME = "iot-dojo"
SSID_PASS = "6a5jxurvjxha" 

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
    
wifi_dojo = connect_wifi(SSID_NAME, SSID_PASS)
