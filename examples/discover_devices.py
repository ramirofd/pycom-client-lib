from pycom import find_pycom_nodes
from pycom import SimplePycomParser

devices = find_pycom_nodes(timeout=3)

for dev in devices:
    dev.initialize()
    dev.help()
    print(SimplePycomParser.get_value(device.get_temperature()))
