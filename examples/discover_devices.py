from pycom import find_pycom_nodes

devices = find_pycom_nodes(timeout=3)

for dev in devices:
    dev.initialize()
    dev.help()

print('hola')
