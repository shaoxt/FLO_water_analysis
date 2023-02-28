from machine import Pin, I2C
import time
import urequests as request
import network
import dht

humidity_sensor = dht.DHT22(Pin(4))

# Define the pin connected to the vibration sensor
# vibration_sensor_pin = Pin(22, Pin.IN)

led_pin = Pin(2, Pin.OUT)
ssid = 'YOUR_SSID'
password = 'YOUR_SSID_PASSWORD'


def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)

    if wlan.active():
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


# Define the callback function to trigger when the vibration sensor is triggered
def on_vibration_triggered(pin):
    led_pin.on()
    send_data(1, "master-bath")
    print("Vibration detected!" + str(time.time_ns()))


def send_data(value, sensor_name):
    r = request.post("http://192.168.1.30:8082/api/v1/sensor?value=" + str(value) + "&sensor=" + sensor_name)
    print("Status Code:" + str(r.status_code))
    time.sleep(1)
    r.close()


def send_humidity_sensor():
    humidity_sensor.measure()
    h = humidity_sensor.humidity()
    if h > 50.0:
        print("Humidity: {}".format(h))
        send_data(h, "shared_bath_humidity")


# Set up the vibration sensor pin to trigger the callback function on rising edge
# vibration_sensor_pin.irq(trigger=Pin.IRQ_RISING, handler=on_vibration_triggered)

# Run an infinite loop to keep the program running
index = 0
while True:
    if index % 5 == 0:
        error = False
        try:
            connect_wifi(ssid, password)
        except:
            print("Connecting wifi error")
            error = True

        if not error:
            try:
                send_humidity_sensor()
            except:
                print("Sending humidity error")

    try:
        led_pin.off()
    except:
        print("Turning off led error")

    index += 1
    time.sleep(1)
