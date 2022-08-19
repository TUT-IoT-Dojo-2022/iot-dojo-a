import network
import webrepl
import network
wifi=network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("elecom2g-d44659", "6a5jxurvjxha")
print(wifi.isconnected())
wifi.ifconfig()
webrepl.start(password="1234")