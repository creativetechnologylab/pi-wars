from machine import Pin
from time import sleep

led = Pin("LED", machine.Pin.OUT)
a = 0

while True:
    led.toggle()
    sleep(1)
    a += 20
    b = a * 3
    print(a, b)
    