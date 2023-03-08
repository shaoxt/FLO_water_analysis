#!/usr/bin/python
import RPi.GPIO as GPIO
import time, sys
import requests

FLOW_SENSOR_GPIO = 22
#MQTT_SERVER = "192.168.1.220"

GPIO.setmode(GPIO.BCM)
GPIO.setup(FLOW_SENSOR_GPIO, GPIO.IN, pull_up_down = GPIO.PUD_UP)

global count
count = 0


def count_pulse(channel):
   global count
   if start_counter == 1:
      count = count+1


def send_data(value, sensor_name):
    r = requests.post("http://192.168.1.30:8082/api/v1/sensor?value=" + str(value) + "&sensor=" + sensor_name)
    print("Status Code:" + str(r.status_code))
    time.sleep(1)
    r.close()

GPIO.add_event_detect(FLOW_SENSOR_GPIO, GPIO.FALLING, callback=count_pulse)

while True:
    try:
        start_counter = 1
        time.sleep(1)
        start_counter = 0
        gpm = (count / 38) * 0.2642 # Pulse frequency (Hz) = 7.5Q, Q is flow rate in L/min.
        print("The flow is: %.3f Liter/min" % (gpm))
        if gpm > 0.001:
           send_data(gpm, "brio_water_dispenser")
           time.sleep(4)
        else:
           time.sleep(5)
        count = 0
    except KeyboardInterrupt:
        print('\nkeyboard interrupt!')
        GPIO.cleanup()
        sys.exit()