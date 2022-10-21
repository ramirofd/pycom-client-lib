import socket
from time import sleep
from typing import List

from zeroconf import ServiceBrowser, ServiceListener, Zeroconf

from .nodes import PycomNode
from .nodes import SimplePycomNode


def find_pycom_nodes(timeout: int = 10, service_name: str = 'pycom_edu_api') -> List[PycomNode]:
    devices = []

    class MyListener(ServiceListener):

        def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
            print(f"Service {name} updated")

        def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
            print(f"Service {name} removed")

        def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
            info = zc.get_service_info(type_, name)
            devices.append(PycomNode(socket.inet_ntoa(info.addresses[0]), info.port))

    zeroconf = Zeroconf()
    listener = MyListener()
    browser = ServiceBrowser(zeroconf, f"_{service_name}._tcp.local.", listener)
    try:
        print('Searching for Pycom Devices on network.')
        elapsed = 0
        while elapsed <= timeout:
            sleep(1)
            elapsed += 1
    finally:
        print(f'Found {len(devices)} device/s.')
        zeroconf.close()
        return devices


def find_simple_pycom_nodes(timeout: int = 10, service_name: str = 'pycom_edu_api') -> List[SimplePycomNode]:
    devices = find_pycom_nodes(timeout, service_name)
    simples = []
    for dev in devices:
        simples.append(SimplePycomNode(dev))
    return simples


class ImproperlyConfigured(Exception):
    pass
