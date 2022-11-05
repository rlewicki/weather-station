import machine
from grove_lcd import Grove_RGB_LCD

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
