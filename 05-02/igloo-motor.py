from machine import Pin, ADC
import network
import random
import socket
import time

motor1a = Pin(14, Pin.OUT)
motor1b = Pin(15, Pin.OUT)

motor2a = Pin(10, Pin.OUT)
motor2b = Pin(11, Pin.OUT)

ssid = "Igloo"
password = "1glooVision"

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
    # print('ip = ' + status[0])


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


commands = {
    "1": stop,
    "2": forward,
    "3": right_forward,
    "4": left_forward,
    "5": right_backward,
    "6": left_backward,
    "7": backward,
}

while True:
    ai = socket.getaddrinfo("192.168.1.115", 80)  # Address of Web Server
    addr = ai[0][-1]

    # Create a socket and make a HTTP request
    s = socket.socket()  # Open socket
    s.connect(addr)
    s.send(b"Anything")  # Send request
    ss = s.recv(512).decode()  # Store reply
    # Print what we received
    try:
        commands[ss]()
    except KeyError:
        commands["1"]()

    # Set RGB LED here
    s.close()  # Close socket
    time.sleep(0.2)  # wait
