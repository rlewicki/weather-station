# Weather Station
This is a home made weather station using Raspberry Pi Pico controller using DHT11 sensor. The controller is connected to home network and is sending temperature and humidity readings to my home lab server.

# Architecture
![architecture](WeatherStationArchitecture.jpg)

# Circuit
![pico-schematic](pico_schematic.png)

# File structure
Each component of the application is in it's respective directory:
- `pico` contains MicroPython code for the Raspberry Pi Pico microcontroller
- `backend` contains backend code written in Java using Spring Boot framework
- `frontend` contains Vue.js project that runs single page app that uses API exposed by the backend server

# Setup

Backend requires a running instance of mongodb. I am running a stock docker image of mongodb for setup simplicity. In case of backend throwing a connection error it is most likely because mongodb instance is not running.

# External services
- Weather data powered by: https://open-meteo.com/en

# Diary

### 5 May 2023
As it turned out a lot of issues with not being able to read data from sensors were
related to the fact that the LCD display requires 5V while Pico can only supply 3.3V.
Due to this issue I have to disconnect the LCD display and most likely will
purchase an e-ink display that only requires 3.3V. However given that all data
will be available via web app this is not a necessity at the moment. Updated the
circuit diagram to match current state of the circuit. I also had to add a pull up
resistor to make the DHT11 sensor more stable.

### 2 June 2023
TBD