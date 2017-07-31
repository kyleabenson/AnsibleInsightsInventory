#!/usr/bin/env python
# This file will pull down groups from Insights, then parse hostnames from that
import argparse
import ConfigParser
import os
import requests
import json


class InsightsInventory(object):
    def _empty_inventory(self):
        return {}
    def read_settings(self):
        """ Reads the settings from the insights_inventory.ini file """

        config = ConfigParser.SafeConfigParser()
        config.read(os.path.dirname(os.path.realpath(__file__)) + '/insights_inventory.ini')

        self.insights_group_url = config.get('insights', 'group_url')
        self.insights_system_url = config.get('insights', 'system_url')
        self.username = None
        self.password = None
        if config.has_option('insights', 'username'):
            self.username = config.get('insights', 'username')
        if config.has_option('insights', 'password'):
            self.password = config.get('insights', 'password')
        self.auth = (self.username, self.password)

    def parse_cli_args(self):
        ''' Command line argument processing '''

        parser = argparse.ArgumentParser(description='Produce an Ansible Inventory file based on Red Hat Insights')
        parser.add_argument('--list', action='store_true', default=True,
                           help='List systems in all groups (default: True)')
        parser.add_argument('--host', action='store',
                           help='Get all the variables about a specific instance')

        self.args = parser.parse_args()
    def _get_groups(self, inventory):
        self.r = requests.get(self.insights_group_url, auth=(self.username, self.password), verify=False)
        data = json.loads(self.r.content)

        for i in data:
            self.inventory[i["display_name"]] = {'group_id' : i['id'], 'hosts': []}
        return self.inventory

    def _get_group_systems(self, inventory):
        for key, value in self.inventory.items():
            group_id = value['group_id']
            insights_system_url = self.insights_system_url.replace("GROUP_ID", str(group_id))
            self.s = requests.get(insights_system_url, auth=(self.username, self.password), verify=False)
            system_data = json.loads(self.s.content)
            ## Need some sort of error handling here..

            if len(system_data["systems"]) < 1:
                pass
            for i in list(system_data['systems']):
                value['hosts'].append(i['toString'])

        return self.inventory

    def __init__(self):
        ''' Main execution path '''
        self.read_settings()
        self.parse_cli_args()
        self.inventory = self._empty_inventory()
        if self.args.host is not None:
            print json.dumps(self.inventory)
        else:
            self._get_groups(self.inventory)
            self._get_group_systems(self.inventory)
            print json.dumps(self.inventory, sort_keys=True, indent=4, separators=(',', ': '))

InsightsInventory()
