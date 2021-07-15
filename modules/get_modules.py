#!/usr/bin/env python3

'''
this script contains modules to get data from files and return desired values
'''

import json

def get_config_value(main_key):

    '''
    this function is for reading main/core/config.json file and return value for desired key
    '''

    file = open('main/core/config.json')
    config_file = json.load(file)
    try :
        value = config_file[main_key]
    except :
        print('Error finding : ' + main_key + ' in config.json')
    else:
        return value
