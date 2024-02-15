import socket
import time

import network
from machine import ADC, Pin

HIGH = 35000
LOW = 30000


def is_still(val):
    return val > LOW and val < HIGH


def increase(val):
    return val > HIGH


def decrease(val):
    return val < LOW


joystick_y = ADC(Pin(26))
joystick_x = ADC(Pin(27))
led = Pin("LED", Pin.OUT)

STOP = 1
STRAIGHT_FORWARD = 2
RIGHT_FORWARD = 3
LEFT_FORWARD = 4
RIGHT_BACKWARD = 5
LEFT_BACKWARD = 6
STRAIGHT_BACKWARD = 7

ssid = "TP-Link_ABDD"
password = "65298190"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print("waiting for connection...")
    time.sleep(1)
# Handle connection error
if wlan.status() != 3:
    raise RuntimeError("network connection failed")
else:
    print("connected")
    status = wlan.ifconfig()
    print('ip = ' + status[0])
    led.on()
    

# Open socket
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print("listening on", addr)

while True:
    try:
        cl, addr = s.accept()
        request = cl.recv(1024)
        print("request", request)

        # print("loop")
        x_val = joystick_x.read_u16()
        y_val = joystick_y.read_u16()

        x_still = is_still(x_val)
        y_still = is_still(y_val)

        x_increase = increase(x_val)
        y_increase = increase(y_val)

        x_decrease = decrease(x_val)
        y_decrease = decrease(y_val)

        if x_still and y_still:
            print(STOP)
            cl.send(str(STOP))

        if y_increase and x_still:
            print(STRAIGHT_FORWARD)
            cl.send(str(STRAIGHT_FORWARD))

        if y_decrease and x_still:
            print(STRAIGHT_BACKWARD)
            cl.send(str(STRAIGHT_BACKWARD))

        if y_increase and x_increase:
            print(LEFT_FORWARD)
            cl.send(str(LEFT_FORWARD))

        if y_increase and x_decrease:
            print(RIGHT_FORWARD)
            cl.send(str(RIGHT_FORWARD))

        if y_decrease and x_increase:
            print(LEFT_BACKWARD)
            cl.send(str(LEFT_BACKWARD))

        if y_decrease and x_decrease:
            print(RIGHT_BACKWARD)
            cl.send(str(RIGHT_BACKWARD))

        cl.close()

    except Exception as e:
        print(e)
        cl.close()
        print("connection closed")

    time.sleep(0.1)
