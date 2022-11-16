import time
from machine import Pin
from grove_lcd import Grove_RGB_LCD
from dht11 import DHT11

lcd = Grove_RGB_LCD(16, 2, 0)

lcd.home()
lcd.print("Hello world!")
heart = bytearray(0)
heart.append(0b01010)
heart.append(0b01110)
heart.append(0b11111)
heart.append(0b11111)
heart.append(0b01110)
heart.append(0b00100)
heart.append(0b00100)
heart.append(0b00000)
lcd.createChar(0, heart)
lcd.setCursor(1, 1)
lcd.write(0)

pin = Pin(28, Pin.OUT, Pin.PULL_DOWN)
sensor = DHT11(pin)
while True:
    time.sleep(1)
    sensor = DHT11(pin)
    t  = (sensor.temperature)
    h = (sensor.humidity)
    print("Temperature: {}".format(sensor.temperature))
    print("Humidity: {}".format(sensor.humidity))
    