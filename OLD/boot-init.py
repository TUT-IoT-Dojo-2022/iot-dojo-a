import network
import webrepl
wifi=network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("iot-dojo", "6a5jxurvjxha")
print(wifi.isconnected())
### チェック
wifi.connect("iot-dojo", "6a5jxurvjxha")
print(wifi.isconnected())
webrepl.start(password="1234")
wifi.ifconfig()

wifi.disconnect()