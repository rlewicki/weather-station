import time
from machine import Pin
from grove_lcd import Grove_RGB_LCD
from dht11 import DHT11
from base64 import b64encode
import network
import ntptime

def http_get(url):
    import socket
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()
    
should_display_time = False

def switch_display_callback(pin):
    global should_display_time
    should_display_time = not should_display_time

print("Booting up")

lcd = Grove_RGB_LCD(16, 2, 0)
lcd.home()
lcd.noBlink()
lcd.noCursor()
lcd.print("Booting up")

time.sleep(1)

lcd.clear()
lcd.setCursor(0, 0)
lcd.print("Network init")

ssid = ""
password = ""

with open("ssid.txt", "r") as f:
    ssid = f.read()

with open("password.txt", "r") as f:
    password = f.read()
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
while not wlan.isconnected():
    time.sleep(1)
print(wlan.ifconfig())

ntptime.settime()
current_time = time.localtime()
print("{}:{}:{}, {}/{}/{}".format(
    current_time[3] + 1, 
    current_time[4], 
    current_time[5], 
    current_time[2], 
    current_time[1], 
    current_time[0]))

degree_char = bytearray(0)
degree_char.append(0b00010)
degree_char.append(0b00101)
degree_char.append(0b00010)
degree_char.append(0b00000)
degree_char.append(0b00000)
degree_char.append(0b00000)
degree_char.append(0b00000)
degree_char.append(0b00000)
lcd.createChar(0, degree_char)

button_pin = Pin(13, Pin.IN, Pin.PULL_UP)
button_pin.irq(trigger=Pin.IRQ_FALLING, handler=switch_display_callback)

dht_pin = Pin(28, Pin.OUT, Pin.PULL_DOWN)
sensor = DHT11(dht_pin)
while True:
    time.sleep(1)
    if should_display_time:
        current_time = time.localtime()
        lcd.clear()
        lcd.setCursor(0, 0)
        lcd.print("{}:{}:{}".format(current_time[3] + 1, current_time[4], current_time[5]))
        lcd.setCursor(0, 1)
        lcd.print("{}/{}/{}".format(current_time[2], current_time[1], current_time[0]))
    else:
        sensor = DHT11(dht_pin)
        t = (sensor.temperature)
        h = (sensor.humidity)
        lcd.clear()
        lcd.setCursor(0, 0)
        lcd.print("T: {}".format(t))
        lcd.write(0)
        lcd.print("C")
        lcd.setCursor(0, 1)
        lcd.print("H: {}%".format(h))

