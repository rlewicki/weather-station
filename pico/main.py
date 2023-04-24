import time
from machine import Pin
from grove_lcd import Grove_RGB_LCD
from dht11 import DHT11
from dht11 import InvalidChecksum
from dht11 import InvalidPulseCount
from base64 import b64encode
import network
import socket
import ntptime
import _thread
import urequests
import json
    
should_display_time = False

def switch_display_callback(pin):
    global should_display_time
    should_display_time = not should_display_time

print("Booting up")
time.sleep(1)
print("Network init")

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

button_pin = Pin(13, Pin.IN, Pin.PULL_UP)
button_pin.irq(trigger=Pin.IRQ_FALLING, handler=switch_display_callback)

dht_pin = Pin(28)
sensor = DHT11(dht_pin)

host_addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
http_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
http_socket.bind(host_addr)
http_socket.listen(1)

open_meteo_wroclaw_url = "https://api.open-meteo.com/v1/forecast?latitude=51.10&longitude=17.03&hourly=temperature_2m,relativehumidity_2m&forecast_days=1"
open_meteo_berlin_url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m,relativehumidity_2m&forecast_days=1"

def http_get_request(url):
    response = urequests.get(url)
    return response.text


def get_current_date():
    current_time = time.localtime()
    current_time = "{}:{}:{}".format(current_time[3] + 1, current_time[4], current_time[5])
    return current_time;

def get_temperature_and_humidity():
    sensor.measure()
    return sensor._temperature, sensor._humidity

global inside_temperature
global inside_humidity
global current_date

inside_temperature = 0
inside_humidity = 0
current_date = ""

def get_city_temperature_and_humidity(url):
    response = http_get_request(url)
    data = json.loads(response)
    current_hour = 14
    t = data["hourly"]["temperature_2m"][current_hour]
    h = data["hourly"]["relativehumidity_2m"][current_hour]
    return t, h

def update_data():
    global inside_temperature
    global inside_humidity
    global current_date
    while True:
        current_date = get_current_date()
        try:
            inside_temperature, inside_humidity = get_temperature_and_humidity()
        except InvalidChecksum as e:
            pass
        except InvalidPulseCount as e:
            pass
        time.sleep(5)

global wroclaw_temperature
global wroclaw_humidity
global berlin_temperature
global berlin_humidity

def await_http_connection():
    try:
        cl, addr = http_socket.accept()
        print("client connected from", addr)
        request = cl.recv(1024)
        print(request)
        
        request = str(request)
        html = """<!DOCTYPE html>
        <html>
        <header>
        <meta charset="UTF-8">
        </header>
        <body>
        <h1>Pico Weather Station</h1>
        <h3>Time: {}</h3>
        <h3>Inside Temperature: {}°C</h3>
        <h3>Inside Humidity: {}%</h3>
        <h3>Wrocław Temperature: {}°C</h3>
        <h3>Wrocław Humidity: {}%</h3>
        <h3>Berlin Temperature: {}°C</h3>
        <h3>Berlin Humidity: {}%</h3>
        </body>
        </html>
        """.format(
            current_date,
            inside_temperature, 
            inside_humidity,
            wroclaw_temperature,
            wroclaw_humidity,
            berlin_temperature,
            berlin_humidity)
        response = html
        cl.send("HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n")
        cl.send(response)
        cl.close()
    except Exception as e:
        print(e)
        cl.close()

_thread.start_new_thread(update_data, ())

# This is fine for now but ideally we need to add a check whether weather info has already
# been fetched before and if there is any change. What this means basically is that we
# want to protect this from being called too often, so add delay of like 5 minutes or so.
wroclaw_temperature, wroclaw_humidity = get_city_temperature_and_humidity(open_meteo_wroclaw_url)
berlin_temperature, berlin_humidity = get_city_temperature_and_humidity(open_meteo_berlin_url)

while True:
    await_http_connection()
