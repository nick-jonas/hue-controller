# import serial
from phue import Bridge

b = Bridge('192.168.0.199')

# If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
b.connect()

# Get the bridge state (This returns the full dictionary that you can explore)
b.get_api()

# Prints if light 1 is on or not
b.set_light([1, 2, 3, 4], 'off', True)