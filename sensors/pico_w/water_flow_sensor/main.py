from machine import Pin
import time
import urequests as request
import network

# Define the pin connected to the water flow sensor
sensor_pin = Pin(22, Pin.IN)

ssid = 'Bolango'
password = 'shaoyourui071'

global has_error
has_error = False

global count
count = 0


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


def count_pulse(pin):
    global count
    if start_counter == 1:
        count = count + 1


def send_data(value, sensor_name):
    r = request.post("http://192.168.1.30:8082/api/v1/sensor?value=" + str(value) + "&sensor=" + sensor_name)
    print("Status Code:" + str(r.status_code))
    time.sleep(2)
    r.close()


# Set up the water flow sensor pin to trigger the callback function on rising edge
sensor_pin.irq(trigger=Pin.IRQ_FALLING, handler=count_pulse)

# Run an infinite loop to keep the program running
has_error = False
n = 0
while True:
    if n % 11 == 0 or has_error:
        try:
            connect_wifi(ssid, password)
            has_error = False
        except Exception as ex:
            print("Connecting wifi error", ex)
            has_error = True

    n += 1

    try:
        start_counter = 1
        time.sleep(1)
        start_counter = 0
        gpm = (count / 38) * 0.2642  # Pulse frequency (Hz) = 7.5Q, Q is flow rate in L/min.
        print("The flow is: %.3f GPM" % (gpm))
        if gpm > 0.001 and not has_error:
            send_data(gpm, "water_purifier")
            time.sleep(2)
        else:
            time.sleep(5)
        count = 0
    except KeyboardInterrupt:
        print('\nkeyboard interrupt!')
        break
    except Exception as Ex:
        print('\nContinue')
        has_error = True


