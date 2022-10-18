# Pycom Client Library
This python package is intended to be used with Pycom boards that implements the [Server Library](https://github.com/ramirofd/pycom-server-lib).

## Usage
### 1 - Install 
####From test repository
~~~
pip install -i https://test.pypi.org/simple/ pycom-client-library
~~~

####From production repository
~~~
pip install pycom-client-library
~~~

### 2 - Code!
Discover available pycom devices running a server implemented with [this library](https://github.com/ramirofd/pycom-server-lib).
~~~
from pycom import find_pycom_nodes

devices = find_pycom_nodes(timeout=3)

for dev in devices:
    dev.initialize()    #initializes the device
    dev.help()          #prints available methods
~~~

Or if you know the ip address and port
~~~
from pycom import PycomNode

device = PycomNode(ip=<IP>, port=<PORT>)

device.initialize()     #initializes the device
device.help()           #prints available methods
~~~


## Extra (for developers)
*** Docs used to deploy python package ***

https://packaging.python.org/en/latest/tutorials/packaging-projects/

####To build:
~~~
py -m build
~~~

####To push package (test):
~~~
py -m twine upload --repository testpypi dist/*
~~~

####To push package (production) WARNING!!!:
~~~
py -m twine upload dist/*
~~~
