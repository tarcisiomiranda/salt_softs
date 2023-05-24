'''
    Author: Tarcisio Andrade Miranda
    Date: qua 24 2023
    Last Update: ----
    Description: This scripts must be run on Salt Master. A dictionary 
    with all data to create a Salt Minion all packeages will be returned. 
    Versions:
        - 0.1:
            - get minions from 'pkg.list_pkgs';
'''

import os
import sys
import salt.client
import time
import json
import argparse

class SaltInventory:

    def __init__(self, args):
        self.salt = salt.client.LocalClient()
        self.time_to_wait = os.getenv('TIMEOUT_SALT', 120)
        self.get_softs = args['get_softs']
        self.fullpath = os.path.abspath(os.path.dirname(__file__))
        print('Aguarde: {} segundos...', self.time_to_wait)

    def get_packages(self):
        '''
            This method will return pkg.list_pkgs
        '''
        try:
            if self.get_softs:
                jid = self.salt.cmd_async('*', ['pkg.list_pkgs'], [[]])
            time.sleep(self.time_to_wait)
            data = self.salt.get_cache_returns(jid)
            return {
                'data' : data
            }
        except Exception as err:
            print('Error : {}'.format(str(err)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Perform a Salt Minion innventory')
    parser.add_argument('-b','--get-softs',action='store_true',
                        help='Includes get_softs')
    parser.add_argument('-s','--syndic', 
                        help='Pass the syndic ID' )
    args = vars(parser.parse_args())
    si = SaltInventory(args)
    res = si.get_packages()
    output_file = open('{}/softs_{}.json'.format(si.fullpath, args['syndic']), 'w')
    output_file.write(json.dumps(res))
    output_file.close()
