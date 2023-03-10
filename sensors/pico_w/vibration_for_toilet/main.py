from machine import Pin
import time
import urequests as request
import network

# Define the pin connected to the vibration sensor
vibration_sensor_pin = Pin(22, Pin.IN)

led_pin = Pin(19, Pin.OUT)
ssid = 'Bolango'
password = 'shaoyourui071'

global has_error
has_error = False


def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    if not has_error and (wlan.active() and wlan.isconnected()):
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
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        print('ip = ' + status[0])


# Define the callback function to trigger when the vibration sensor is triggered
def on_vibration_triggered(pin):
    global has_error
    try:
        led_pin.on()
        send_data(1, "guest_bath_toilet")
        has_error = False
    except:
        has_error = True
        print("Sending data error")

    print("Vibration detected!" + str(time.time_ns()))


def send_data(value, sensor_name):
    r = request.post("http://192.168.1.30:8082/api/v1/sensor?value=" + str(value) + "&sensor=" + sensor_name)
    print("Status Code:" + str(r.status_code))
    time.sleep(2)
    r.close()


# Set up the vibration sensor pin to trigger the callback function on rising edge
vibration_sensor_pin.irq(trigger=Pin.IRQ_RISING, handler=on_vibration_triggered)

# Run an infinite loop to keep the program running
n = 0
while True:
    try:
        led_pin.off()
    except:
        print("Turning off led error")
    time.sleep(2)
    if n % 11 == 0 or has_error:
        try:
            connect_wifi(ssid, password)
            has_error = False
        except Exception as ex:
            print("Connecting wifi error", ex)
            has_error = True

    n += 1

