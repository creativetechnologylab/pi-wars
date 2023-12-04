from machine import Pin, ADC
import time

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

STOP = 1
STRAIGHT_FORWARD = 2
RIGHT_FORWARD = 3
LEFT_FORWARD = 4
RIGHT_BACKWARD = 5
LEFT_BACKWARD = 6
STRAIGHT_BACKWARD = 7


while True:
    # print(joystick_y.read_u16(), joystick_x.read_u16())
    x = joystick_x.read_u16()
    y = joystick_y.read_u16()
    
    x_still = is_still(joystick_x.read_u16())
    y_still = is_still(joystick_y.read_u16())
    
    if x_still and y_still:
        print(STOP)
        
    if increase(y) and x_still:
        print(STRAIGHT_FORWARD)
        
    if decrease(y) and x_still:
        print(STRAIGHT_BACKWARD)
        
    if increase(y) and increase(x):
        print(LEFT_FORWARD)
        
    if increase(y) and decrease(x):
        print(RIGHT_FORWARD)
        
    if decrease(y) and increase(x):
        print(LEFT_BACKWARD)
        
    if decrease(y) and decrease(x):
        print(RIGHT_BACKWARD)
        
    time.sleep(0.1)