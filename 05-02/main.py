import socket
import time

import network
from machine import Pin

motor1a = Pin(14, Pin.OUT)
motor1b = Pin(15, Pin.OUT)

motor2a = Pin(10, Pin.OUT)
motor2b = Pin(11, Pin.OUT)

print("Hello.")

ssid = "Igloo"
password = "1glooVision"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

html = """<!DOCTYPE html>
<html>
    <head> <title>Pico W</title> </head>
    <body> <h1>Pico W</h1>
        <p>%s</p>
    </body>
</html>
"""

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print("waiting for connection...")
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError("network connection failed")
else:
    print("connected")
    status = wlan.ifconfig()
    print("ip = " + status[0])

addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print("listening on", addr)

# Listen for connections


def right_forward():
    motor1a.value(0)
    motor1b.value(0)
    motor2a.value(0)
    motor2b.value(1)


def left_forward():
    motor2a.value(0)
    motor2b.value(0)
    motor1a.value(1)
    motor1b.value(0)


def right_backward():
    motor1a.value(0)
    motor1b.value(0)
    motor2a.value(1)
    motor2b.value(0)


def left_backward():
    motor2a.value(0)
    motor2b.value(0)
    motor1a.value(0)
    motor1b.value(1)


def forward():
    motor1a.value(1)
    motor1b.value(0)
    motor2a.value(0)
    motor2b.value(1)


def backward():
    motor1a.value(0)
    motor1b.value(1)
    motor2a.value(1)
    motor2b.value(0)


def stop():
    motor1a.value(0)
    motor1b.value(0)
    motor2a.value(0)
    motor2b.value(0)


while True:
    try:
        cl, addr = s.accept()
        print("client connected from", addr)
        request = cl.recv(1024)
        print(request)

        request = str(request)
        direction_forward = request.find("/direction/forward")
        direction_backward = request.find("/direction/backward")
        direction_stop = request.find("/direction/stop")
        print("forward = " + str(direction_forward))
        print("backward = " + str(direction_backward))
        print("stop = " + str(direction_stop))

        if direction_forward == 6:
            print("forward")
            forward()
            stateis = "Moving forward"

        if direction_backward == 6:
            print("backward")
            backward()
            stateis = "Moving backward"

        if direction_stop == 6:
            print("stop")
            stop()
            stateis = "Stop"

        response = html % stateis

        cl.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
        cl.send(response)
        cl.close()

    except OSError as e:
        cl.close()
        print("connection closed")
