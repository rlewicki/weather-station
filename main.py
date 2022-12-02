import time
from machine import Pin
from grove_lcd import Grove_RGB_LCD
from dht11 import DHT11
from base64 import b64encode

lcd = Grove_RGB_LCD(16, 2, 0)

lcd.home()
lcd.noBlink()
lcd.noCursor()
lcd.print("Initializing...")

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

pin = Pin(28, Pin.OUT, Pin.PULL_DOWN)
sensor = DHT11(pin)
while True:
    time.sleep(1)
    sensor = DHT11(pin)
    t = (sensor.temperature)
    h = (sensor.humidity)
    lcd.clear()
    lcd.setCursor(0, 0)
    lcd.print("T: {}".format(t))
    lcd.write(0)
    lcd.print("C")
    lcd.setCursor(0, 1)
    lcd.print("H: {}%".format(h))
