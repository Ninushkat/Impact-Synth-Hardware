# -*- coding: utf-8 -*-
"""

 ~ Neurorack project ~
 GPIO : An example tutorial class for testing simple GPIO interactions
 
 This file is only a pedagogical draft for development.
 This allows to understand the basic principles of the GPIO in general.
 Here the functions are targeted to check the Jetson Nano specifically.

 Author               : Philippe Esling, Ninon Devis, Martin Vert
                        <{esling, devis}@ircam.fr>

"""
import time
import Jetson.GPIO as GPIO

class GPIOTutorial():    
    '''
        The class implements different tutorials to understand the GPIO. 
        It should work with any GPIO (Raspberry Pi), but here we target the Jetson Nano
    '''
    
    def __init__(self, 
            pin: list=[12], 
            debounce: int=250):
        '''
            Constructor - Creates a new instance of the Navigation class.
            Parameters:
                pins:       [int], optional
                            Specify GPIO pins that connect buttons [default: 11]
                debounce:   [int], optional
                            Debounce time to prevent multiple firings [default: 250ms]
        '''
        self._pin = pin
        self._debounce = debounce                                 
        self.setup_gpios()
    
    def setup_gpios(self):
        GPIO.setwarnings(False)                              
        GPIO.setmode(GPIO.BOARD)     
    
    def tuto_01_led(self):
        ''' A simple LED blinker with given sleep '''
        GPIO.setup(self._pin, GPIO.OUT, initial=GPIO.LOW)
        time.sleep(1)
        GPIO.output(self._pin, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(self._pin, GPIO.LOW)
        time.sleep(1)
        GPIO.output(self._pin, GPIO.HIGH)
        time.sleep(2)
        for i in range(10):
            GPIO.output(self._pin, GPIO.LOW)
            time.sleep(0.25)
            GPIO.output(self._pin, GPIO.HIGH)
            time.sleep(0.25)
        
    def tuto_02_led(self):
        ''' An eternal LED inverter system '''
        GPIO.setup(self._pin, GPIO.OUT, initial=GPIO.HIGH)
        curr_value = GPIO.HIGH
        try:
            while True:
                time.sleep(0.5)
                GPIO.output(self._pin, curr_value)
                curr_value ^= GPIO.HIGH
        finally:
            GPIO.cleanup()
        
    def tuto_03_button(self):
        ''' A button with dirty active waiting '''
        GPIO.setup(self._pin, GPIO.IN)
        prev_value = None
        try:
            while True:
                value = GPIO.input(self._pin)
                if value != prev_value:
                    if value == GPIO.HIGH:
                        value_str = "HIGH"
                    else:
                        value_str = "LOW"
                    print("Value read from pin {} : {}".format(self._pin, value_str))
                    prev_value = value
                time.sleep(1)
        finally:
            GPIO.cleanup()
        
    def tuto_04_button(self):
        ''' A slightly cleaner button with signal waiting '''
        GPIO.setup(self._pin, GPIO.IN)  # button pin set as input
        try:
            while True:
                print("Waiting for button event")
                GPIO.wait_for_edge(self._pin, GPIO.RISING)
                # event received when button pressed
                print("Button Pressed!")
                time.sleep(1)
        finally:
            GPIO.cleanup()
            
    def tuto_05_button(self):
        GPIO.setup(self._pin, GPIO.IN)
        GPIO.add_event_detect(self._pin, GPIO.BOTH, callback=self.callback, bouncetime=self._debounce)
        print("Starting demo now! Press CTRL+C to exit")
        try:
            while True:
                print("Main loop...")
                time.sleep(5)
        finally:
            GPIO.cleanup()
    
    def callback(self, channel: int):
        print("Button event - released")
        value = GPIO.input(channel)
        print(value)
        time.sleep(1)

    def __del__(self):
        '''
            Destructor - cleans up the GPIO.
        '''
        GPIO.cleanup()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='GPIO Tutorial')
    # Device Information
    parser.add_argument('--pin',        type=int,   default=12,     help='which pin to use')
    parser.add_argument('--tutorial',   type=int,   default=1,      help='which tutorial to check')
    # Parse the arguments
    args = parser.parse_args()
    # Create the tutorial class
    tutorial = GPIOTutorial()
    if (args.tutorial == 1):
        tutorial.tuto_01_led()
    elif (args.tutorial == 2):
        tutorial.tuto_02_led()
    elif (args.tutorial == 3):
        tutorial.tuto_03_button()
    elif (args.tutorial == 4):
        tutorial.tuto_04_button()
    elif (args.tutorial == 5):
        tutorial.tuto_05_button()