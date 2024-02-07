import time

from machine import Pin

motor1a = Pin(14, Pin.OUT)
motor1b = Pin(15, Pin.OUT)

motor2a = Pin(10, Pin.OUT)
motor2b = Pin(11, Pin.OUT)

print("Hello.")


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
