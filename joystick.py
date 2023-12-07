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
        
    if y_increase and x_still:
        print(STRAIGHT_FORWARD)
        
    if y_decrease and x_still:
        print(STRAIGHT_BACKWARD)
        
    if y_increase and x_increase:
        print(LEFT_FORWARD)
        
    if y_increase and x_decrease:
        print(RIGHT_FORWARD)
        
    if y_decrease and x_increase:
        print(LEFT_BACKWARD)
        
    if y_decrease and x_decrease:
        print(RIGHT_BACKWARD)
        
    time.sleep(0.1)