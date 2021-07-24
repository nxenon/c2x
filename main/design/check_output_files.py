#!/usr/bin/env python3

'''
check output files :
create them if they don't exist
'''

from os.path import exists

path_prefix = 'main/web/static/files/'
files_path = ['terminal.txt', 'server.txt', 'create_script.txt']

def check_files():
    for f in files_path:
        comp_path = path_prefix + f
        if not exists(comp_path):
            with open(comp_path, 'w') as created_file:
                pass
