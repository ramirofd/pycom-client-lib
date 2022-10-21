from pycom import PycomNode


# Uncomment and fill with IP and PORT
# device = PycomNode(ip='<IP>', port=<PORT>)
device.initialize()                 # Initializes the device
device.help()                       # Prints available methods
print(device.get_temperature())     # Prints the temperature read from the node.
device.post_color(color=0xFF0000)   # Changes the LED color
