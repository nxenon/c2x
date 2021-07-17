#!/usr/bin/env python3

'''
this script checks the login information
'''

from flask import redirect,make_response
from modules.get_modules import get_config_value
import datetime
from random import randint
from hashlib import md5
from colorama import Fore

class CheckLogin:
    def __init__(self ,user ,user_pass):
        # data user entered
        self.username_in_login = user
        self.password_in_login = user_pass
        # user and password stored in config.json
        self.username_in_app = None
        self.password_in_app = None

    def run(self):
        ret = self.read_login()
        if (ret):
            return ret
        else :
            return self.check_login()

    def read_login(self):
        self.username_in_app = get_config_value(main_key='web_user')
        self.password_in_app = get_config_value(main_key='web_pass')
        if ((self.username_in_app) and (self.password_in_app)):
            pass
        else:
            print(Fore.RED + '[!]' + Fore.RESET + ' web login failed')
            return redirect('/login?error=nof') # nof is for no credential found in config.json

    def check_login(self):
        if ((self.username_in_app.lower() == self.username_in_login.lower()) and (self.password_in_app == self.password_in_login)):
            print(Fore.GREEN + '[+]' + Fore.RESET + ' web login succeeded')
            response = make_response(redirect('/dashboard' ,code=302))
            created_token = self.create_random_token()
            self.save_token(token=created_token)
            response.set_cookie('token' ,created_token ,expires=datetime.datetime.now() + datetime.timedelta(days=30))
            response.set_cookie('user' ,self.username_in_app ,expires=datetime.datetime.now() + datetime.timedelta(days=30))
            response.set_cookie('logged_in' ,'yes' ,expires=datetime.datetime.now() + datetime.timedelta(days=30))
            return response
        else:
            print(Fore.RED + '[!]' + Fore.RESET + ' web login failed')
            return redirect('login?error=lf' ,code=302)

    def create_random_token(self):
        # creates a random token for logged in user
        user = self.username_in_app
        random_number1 = str(randint(1,1000000))
        random_number2 = str(randint(1,1000000))
        combined = random_number1 + user + random_number2
        my_hash = md5()
        my_hash.update(combined.encode())
        return my_hash.hexdigest()

    def save_token(self ,token):
        # saves the token in token.txt file
        with open('main/web/token.txt' ,'w') as token_text_file:
            token_text_file.write(token)
