from machine import Pin
import time
import urequests as requests
import network

pir = Pin(22, Pin.IN, Pin.PULL_DOWN)
n = 0

ssid = "Bolango"
password = "shaoyourui071"


def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    if wlan.isconnected() == False:

        print("wlan deinit")
        wlan.deinit()
        print("wlan scan")
        wlan.scan()
        print("wlan active")
        wlan.active(True)
        print(wlan)
        print(wlan.scan())
        print(wlan)
        wlan.connect(ssid, password)
        second = 0
        while wlan.isconnected() == False:
            print("wait for isconnected " + str(second))
            time.sleep(1)
            second += 1
            if second > secondstrywificonnect:
                print("reboot")
                machine.reset()
    else:
        print("wlan already active")

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
    time.sleep(1)
    r.close()


print('Starting up the PIR Module')

has_error = False
try:
    connect_wifi(ssid, password)
except Exception as ex:
    print("Connecting wifi error", ex)
    has_error = True
time.sleep(5)
print('Ready')

last_value = 0
value = 0

wait = 2
while True:
    has_error = False
    if n % 19 == 0 or has_error:
        try:
            connect_wifi(ssid, password)
        except Exception as ex:
            print("Connecting wifi error", ex)
            has_error = True
        time.sleep(3)

    value = pir.value()
    if value == 1:
        if last_value == 1 and not has_error:
            send_data(2, "guest_bath_motion")
            print('Motion Detected ', n)
            last_value = 0
        else:
            send_data(1, "guest_bath_motion")
            last_value = value
            wait = 2
            if has_error:
                print('Motion Detected but wifi has error ', n)
    else:
        wait = 2
        last_value = value

    n = n + 1
    time.sleep(wait)
