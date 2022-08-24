import network
import webrepl
import network
wifi=network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("CDSL-A910-11n", "11n-j9$4zt3kch")
print(wifi.isconnected())
wifi.ifconfig()
webrepl.start(password="1234")

wifi=network.WLAN(network.STA_IF)
wifi.connect("CDSL-A910-11n", "11n-j9$4zt3kch")
webrepl.start(password="1234")