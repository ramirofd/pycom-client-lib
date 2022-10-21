from pycom import SimplePycomNode


# Uncomment and fill with IP and PORT
# device = SimplePycomNode(ip='<IP>', port=<PORT>)
device.help()                           # Prints available methods
print(device.get('temperature'))        # Prints the temperature read from the node.
device.post('color', color=0x0000FF)    # Changes the LED color
