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
import ujson
import hmac
import hashlib
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
secret_key = ""

with open("ssid.txt", "r") as f:
    ssid = f.read()

with open("password.txt", "r") as f:
    password = f.read()
    
with open("secret_key.txt", "r") as f:
    secret_key = f.read()

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
while not wlan.isconnected():
    print("Waiting for Internet connection...")
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

dht_pin = Pin(28)
sensor = DHT11(dht_pin)

# open_meteo_wroclaw_url = "https://api.open-meteo.com/v1/forecast?latitude=51.10&longitude=17.03&hourly=temperature_2m,relativehumidity_2m&forecast_days=1"
# open_meteo_berlin_url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m,relativehumidity_2m&forecast_days=1"

server_base_address = "http://192.168.0.21:8080/api/v1/sampleReading/"
server_api_insert = "insert_single"

def http_get_request(url):
    response = urequests.get(url)
    return response.text

def get_current_date():
    current_time = time.localtime()
    current_time = "{}:{}:{}".format(current_time[3] + 1, current_time[4], current_time[5])
    return current_time;

def get_temperature_and_humidity():
    sensor.measure()
    return round(sensor._temperature, 1), round(sensor._humidity, 1)

global inside_temperature
global inside_humidity
global current_date

inside_temperature = 0
inside_humidity = 0
current_date = ""

def send_local_readings():
    url = server_base_address + server_api_insert
    temperature_text = str(inside_temperature)
    humidity_text = str(inside_humidity)
    body = ujson.dumps({ "temperature": temperature_text, "humidity": humidity_text})
    signature = hmac.new(bytes(secret_key, "utf-8"), digestmod=hashlib.sha256)
    signature.update("temperature".encode())
    signature.update(temperature_text.encode())
    signature.update("humidity".encode())
    signature.update(humidity_text.encode())
    signature = signature.digest()
    header = {"content-type": "application/json", "x-signature-sha256": signature.hex()}
    response = urequests.post(url, headers=header, data=body)
    print("Sent local readings to server, received response: " + str(response))

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
        send_local_readings()
        time.sleep(5)

while True:
    update_data()
