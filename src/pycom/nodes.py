from copy import deepcopy

import requests
import json
import socket


def create_function(method, ip, port, path, data):
    def funct(**kwargs):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        method_name = f'{method.lower()}_{path[1:]}'
        for argument in data['arguments'].keys():
            if argument not in kwargs.keys():
                raise Exception(f'Required {argument} on {method_name} method.')
        sock.connect((ip, port))
        req = f'{method} {path} HTTP/1.1\r\nHost:{ip}\r\n\r\n{json.dumps(kwargs)}'
        sock.send(req.encode())
        response = sock.recv(4096).decode()
        body_start = response.find('\r\n\r\n')
        body = '{}'
        if body_start >= 0:
            body = response[body_start + 4:]
        return json.loads(body)

    return funct


class PycomNode:
    endpoints = None

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def base_url(self):
        return f'http://{self.ip}:{self.port}'

    def initialize(self):
        self.endpoints = json.loads(requests.get(f'{self.base_url()}/help').text)

        for method in self.endpoints.keys():
            for path in self.endpoints[method].keys():
                if 'help' not in path:
                    data = deepcopy(self.endpoints[method][path])
                    method_name = f'{method.lower()}_{path[1:]}'
                    self.__dict__[method_name] = create_function(method, self.ip, self.port, path, data)

    def help(self):
        if self.endpoints is None:
            from .utils import ImproperlyConfigured
            raise ImproperlyConfigured('First you have to call initialize method on this device.')

        print('The available operations on this device are:')
        for method in self.endpoints.keys():
            for path in self.endpoints[method].keys():
                if 'help' not in path:
                    data = self.endpoints[method][path]
                    method_name = f'{method.lower()}_{path[1:]}'
                    print(f'* {method_name}: {data["description"]}')
                    params_usage = ''
                    if len(data['arguments'].keys()) != 0:
                        print(f'\tParameters:')
                        for i, argument in enumerate(data['arguments'].keys(), start=1):
                            params_usage += f'{argument}=<value>{", " if i != len(data["arguments"].keys()) else ""}'
                            print(f'\t* {argument}: {data["arguments"][argument]}')
                    print(f'  Example: <device>.{method_name}({params_usage})\n')


class SimplePycomNode:

    def __init__(self, ip, port: int = None):
        if isinstance(ip, PycomNode):
            self.node = ip
        else:
            if port is None:
                raise Exception('Missing Port Parameter (int)')
            self.node = PycomNode(ip, port)
        self.node.initialize()

    def help(self):
        for method in self.node.endpoints.keys():
            for path in self.node.endpoints[method].keys():
                if 'help' not in path:
                    data = self.node.endpoints[method][path]
                    print(f'{data["description"]}')
                    params_usage = ''
                    if len(data['arguments'].keys()) != 0:
                        print(f'\tParameters:')
                        for i, argument in enumerate(data['arguments'].keys(), start=1):
                            params_usage += f'{argument}=<value>{", " if i != len(data["arguments"].keys()) else ""}'
                            print(f'\t\t* {argument}: {data["arguments"][argument]}')
                    print(f'\tExample: <device>.{method.lower()}(\'{path[1:]}\'{", " if len(params_usage)!=0 else ""}{params_usage})\n')

    def get(self, param, **kwargs):
        method = f'get_{param}'
        funct = getattr(self.node, method)
        return funct(**kwargs).get('value', None)

    def post(self, param, **kwargs):
        method = f'post_{param}'
        funct = getattr(self.node, method)
        return funct(**kwargs).get('value', None)

    def put(self, param, **kwargs):
        method = f'put_{param}'
        funct = getattr(self.node, method)
        return funct(**kwargs).get('value', None)

    def patch(self, param, **kwargs):
        method = f'patch_{param}'
        funct = getattr(self.node, method)
        return funct(**kwargs).get('value', None)

    def delete(self, param, **kwargs):
        method = f'delete_{param}'
        funct = getattr(self.node, method)
        return funct(**kwargs).get('value', None)

