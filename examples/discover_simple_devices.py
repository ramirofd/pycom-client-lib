from pycom import find_simple_pycom_nodes

devices = find_simple_pycom_nodes(timeout=3)

for dev in devices:
    dev.help()
    print(dev.get('temperature'))
    dev.post('color', color=0x0000FF)
