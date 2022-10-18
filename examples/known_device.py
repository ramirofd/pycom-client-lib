from pycom import PycomNode
from pycom import SimplePycomParser

# Uncomment and fill with IP and PORT
# device = PycomNode(ip=<IP>, port=<PORT>)

device.initialize()     #initializes the device
device.help()           #prints available methods

print(SimplePycomParser.get_value(device.get_temperature()))