from machine import Pin
import time
import urequests as requests
import network

pir = Pin(22, Pin.IN, Pin.PULL_DOWN)
n = 0

print('Starting up the PIR Module')
time.sleep(1)
print('Ready')

ssid = "YOUR_SSID"
password = "YOUR_PASSWORD"


def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)

    if wlan.active() and wlan.isconnected():
        return
    wlan.active(True)
    wlan.connect(ssid, password)

    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...', wlan.status())
        time.sleep(3)

    if wlan.status() != 3:
        print(str(wlan.status()))
        raise RuntimeError('network connection failed' + str(wlan.status()))
    else:
        print('connected')
        status = wlan.ifconfig()
        print('ip = ' + status[0])


def send_data(value, sensor_name):
    r = requests.post("http://192.168.1.30:8082/api/v1/sensor?value=" + str(value) + "&sensor=" + sensor_name)
    print("Status Code:" + str(r.status_code))
    time.sleep(2)
    r.close()


last_value = 0
value = 0

while True:
    has_error = False
    if n % 9 == 0 or has_error:
        try:
            connect_wifi(ssid, password)
        except Exception as ex:
            print("Connecting wifi error", ex)
            has_error = True
        time.sleep(2)

    value = pir.value()
    if value == 1:
        if last_value == 1 and not has_error:
            send_data(2, "shared_bath_motion")
            print('Motion Detected, double', n)
            last_value = 0
        else:
            send_data(1, "shared_bath_motion")
            print('Motion Detected ', n)
            last_value = value
            if has_error:
                print('Motion Detected but wifi has error ', n)

    last_value = value
    n = n + 1
    time.sleep(2)
