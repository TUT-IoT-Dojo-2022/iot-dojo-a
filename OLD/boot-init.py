import network
import webrepl
wifi=network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("CDSL-A910-11n", "11n-j9$4zt3kch")
print(wifi.isconnected())
### チェック
wifi.connect("CDSL-A910-11n", "11n-j9$4zt3kch")
print(wifi.isconnected())
webrepl.start(password="1234")
wifi.ifconfig()


wifi=network.WLAN(network.STA_IF)
wifi.connect("iot-dojo", "6a5jxurvjxha")
webrepl.start(password="1234")

wifi.disconnect()