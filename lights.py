import time
import threading
import RPi.GPIO as GPIO
import phue
import config
from phue import Bridge

class Lights:

    def turn_off_led_indicate(self):
        self.stop_led_timer()
        GPIO.output(self.SPI_LED, False)

    def on_led_interval(self):
        # if connected give steady light, otherwise blink
        if self.bridge is not None:
            GPIO.output(self.SPI_LED, True) ## Turn on GPIO pin 7
            time.sleep(60)
        else:
            GPIO.output(self.SPI_LED, True)
            time.sleep(self.BLINK_SPEED)
            GPIO.output(self.SPI_LED, False)
            # time.sleep(self.BLINK_SPEED)
        self.stop_led_timer()
        self.led_thread = threading.Timer(self.BLINK_SPEED, self.on_led_interval)
        self.led_thread.setDaemon(True)
        self.led_thread.start()

    def __init__(self):
        self.bridge = None # bridge gets set on connection
        self.MAX_BRI = 254.0
        self.MAX_HUE = 65535
        self.MAX_SAT = 255
        self.SPI_LED = 4 # bcm number
        self.BLINK_SPEED = 0.3 # seconds
        self.connect_thread = None
        self.led_thread = None
        # init LED indicator
        GPIO.setup(self.SPI_LED, GPIO.OUT) ## Setup GPIO Pin 7 (BCM 14) to OUT 
        GPIO.output(self.SPI_LED, False) ## Turn on GPIO pin 7
        # start LED thread
        self.on_led_interval()

    def stop_connect_timer(self):
        if self.connect_thread is not None:
            self.connect_thread.cancel()

    def stop_led_timer(self):
        if self.led_thread is not None:
            self.led_thread.cancel()

    def connect(self):
        print "Attempting connection..."
        try:
            self.bridge = Bridge('192.168.0.199')
            print "Connected to Hue Bridge"
            # If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
            self.bridge.connect()
            # indicate connection
            GPIO.output(self.SPI_LED, True) 
            # Get the bridge state (This returns the full dictionary that you can explore)
            self.bridge.get_api()
            self.stop_connect_timer()
            # get flat list of all lights
            self.lights = self.bridge.get_light_objects('list')

        except: # phue.PhueRegistrationException as err:
            print "Problem connecting, try pressing Bridge button."
            self.stop_connect_timer()
            self.connect_thread = threading.Timer(4, self.connect)
            self.connect_thread.setDaemon(True)
            self.connect_thread.start()

    def setState(self, isSwitchOn, bri, hue, sat):
        if self.bridge is not None and hasattr(self, 'lights'):

            # format brightness value
            bri = 1.0 - (bri / 100)
            bri_value = round(bri * self.MAX_BRI)
            bri_value = int(bri_value)

            # format hue value
            hue = 1.0 - (hue / 100)
            hue_value = round(hue * self.MAX_HUE)
            hue_value = int(hue_value)

            sat = 1.0 - (sat / 100)
            sat_value = round(sat * self.MAX_SAT)
            sat_value = int(sat_value)

            isOn = isSwitchOn
            if bri_value < 6:
                isOn = False
            
            # print bri_value, hue_value, sat_value

            # assign to all lights
            for light in self.lights:
                light.on = isOn
                if isOn:
                    light.brightness = bri_value
                    light.hue = hue_value
                    light.saturation = sat_value
