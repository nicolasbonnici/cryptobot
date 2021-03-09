import json

import requests
from decouple import config

# requests/API platform abstraction layer
class Rest:
    def __init__(self):
        self.api_root = config('API_ROOT')
        self.client = requests
        self.headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

    def get(self, resource: str, data={}, headers={}):
        return self.client.get(self.build_url(resource), data=json.dumps(data), headers=self.build_headers(headers))

    def post(self, resource: str, data: dict, headers={}):
        return self.client.post(self.build_url(resource), data=json.dumps(data), headers=self.build_headers(headers))

    def put(self, resource: str, data: dict, headers={}):
        return self.client.put(self.build_url(resource), data=json.dumps(data), headers=self.build_headers(headers))

    def delete(self, resource: str, data: dict, headers={}):
        return self.client.delete(self.build_url(resource), headers=self.build_headers(headers))

    def build_url(self, resource: str):
        return self.api_root + resource

    def build_headers(self, headers: dict):
        return {
            **self.headers,
            **headers
        }
