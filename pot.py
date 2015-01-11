import RPi.GPIO as GPIO
import config

class Pot:
    def __init__(self, label, pin, tolerance = 5):
        self.label = label
        self.value = 0
        self.pin = pin
        self.last_read = 0
        self.tolerance = tolerance
        self.trim_pot_changed = False

    # read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
    def readadc(self, adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
            return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
            if (commandout & 0x80):
                GPIO.output(mosipin, True)
            else:
                GPIO.output(mosipin, False)
            commandout <<= 1
            GPIO.output(clockpin, True)
            GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
            GPIO.output(clockpin, True)
            GPIO.output(clockpin, False)
            adcout <<= 1
            if (GPIO.input(misopin)):
                adcout |= 0x1

        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

    def read(self):
        # we'll assume that the pot didn't move
        self.trim_pot_changed = False
        # read the analog pin
        trim_pot = self.readadc(self.pin, config.SPICLK, config.SPIMOSI, config.SPIMISO, config.SPICS)
        # how much has it changed since the last read?
        pot_adjust = abs(trim_pot - self.last_read)
        # check to see if it changed
        if ( pot_adjust > self.tolerance ):
            self.trim_pot_changed = True
        # if changed, set value
        if(self.trim_pot_changed):
            self.value = trim_pot / 10.24           # convert 10bit adc0 (0-1024) trim pot read into 0-100 volume level
            # self.value = round(self.value)          # round out decimal value
            self.value / 100
            # print '{label} Value = {value}%' .format(label= self.label, value = self.value)
        self.last_read = self.value
        return self.value
