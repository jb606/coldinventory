#!/usr/bin/env python3
import os
import json
import subprocess
import requests

url = "http://localhost:8000/hardware/"
cert = "my.crt"
key = "my.key"

class ColdInventory(object):
    def __init__(self):
        self.inventory = {}
        self.read_cli_args()
        if self.args.list:
            self.inventory = self._get_inventory_all()


    def _get_inventory_all(self):
        hostvars = {}
        ungrouped = []
        response = requests.get(url)
        if response.status_code == 200:
        # Parse the JSON response
            data = response.json()
            for d in data:
                name = d['device_name']
                address = d['ip']
                if name not in ungrouped:
                    ungrouped.append(name)
                if name not in hostvars:
                    hostvars[name] = { 'ansible_host': '', 'mac': ''}

                hostvars[name]['ansible_host'] = address
                hostvars[name]['mac'] = d['mac']
            ans_data = {
                '_meta': {
                 'hostvars': hostvars
                },
               'all': {
                    'children': [
                       'ungrouped'
                    ]
                 },
                 'ungrouped': {
                   'hosts': ungrouped
                 }
            }
            print(json.dumps(ans_data, indent=2))
        else:
            print(f"Error: {response.status_code} - {response.text}")

    def read_cli_args(self):
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action='store_true')
        parser.add_argument('--host', action='store')
        self.args = parser.parse_args()
        
ColdInventory()
