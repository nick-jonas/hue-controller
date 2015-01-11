# https://github.com/studioimaginaire/phue

#!/usr/bin/env python
import time
import os
import RPi.GPIO as GPIO
import phue
import config
import logging
from phue import Bridge
from lights import Lights
from pot import Pot
from switch import Switch

logging.basicConfig()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
DEBUG = 1

# set up the SPI interface pins
GPIO.setup(config.SPIMOSI, GPIO.OUT)
GPIO.setup(config.SPIMISO, GPIO.IN)
GPIO.setup(config.SPICLK, GPIO.OUT)
GPIO.setup(config.SPICS, GPIO.OUT)

# define pots
pot_brightness = Pot('Brightness', 0)
pot_hue = Pot('Hue', 1)
pot_saturation = Pot('Saturation', 2)
pots_adc = [pot_brightness, pot_hue, pot_saturation]

# define switch
switch = Switch(3)

# create lights
lights = Lights()
lights.connect()



try: 
    while True:        
        isOn = switch.isOn()
        if(isOn):
            for pot in pots_adc:
                pot.read()
        # set Hue lights
        lights.setState(isOn, pot_brightness.value, pot_hue.value, pot_saturation.value)
        # hang out and do nothing for a half second
        time.sleep(0.05)

except (KeyboardInterrupt, SystemExit):
    lights.turn_off_led_indicate()
