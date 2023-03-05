import RPi.GPIO as GPIO                       #Import GPIO library
import time                                   #Import time library
import requests

GPIO.setmode(GPIO.BOARD)                      #Set GPIO pin numbering

pir = 26                                      #Associate pin 26 to pir

GPIO.setup(pir, GPIO.IN)                      #Set pin as GPIO in

print("Waiting for sensor to settle")

time.sleep(2)                   #Waiting 2 seconds for the sensor to initiate

print("Detecting motion")

def send_data(value, sensor_name):
    r = requests.post("http://192.168.1.30:8082/api/v1/sensor?value=" + str(value) + "&sensor=" + sensor_name)
    print("Status Code:" + str(r.status_code))
    time.sleep(1)
    r.close()

while True:
    try:
        if GPIO.input(pir):             #Check whether pir is HIGH
            send_data(1, "guest_bath_motion")
            time.sleep(2)              #D1- Delay to avoid multiple detection
    except Exception as ex:
        print(ex)

    time.sleep(0.1)  #While loop delay should be less than detection dela
