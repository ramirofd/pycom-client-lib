from copy import deepcopy

import requests
import json


def create_function(method, base_url, path, data):
    def funct(**kwargs):
        method_name = f'{method.lower()}_{path[1:]}'
        for argument in data['arguments'].keys():
            if argument not in kwargs.keys():
                raise Exception(f'Required {argument} on {method_name} method.')
        request_funct = getattr(requests, method.lower())
        response = request_funct(base_url + path)
        return json.loads(response.text)

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
                    self.__dict__[method_name] = create_function(method, self.base_url(), path, data)

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

