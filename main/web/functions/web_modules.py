#!/usr/bin/env python3

'''
this script contains modules for web
'''

from flask import request

def check_login():
    '''
    this function checks if user is logged in or not
    '''
    if (request.cookies.get('logged_in') == 'yes'):
        if (request.cookies.get('user') is not None):
            try:
                with open('main/web/token.txt') as token_file:
                    token = token_file.read()
                    if (request.cookies.get('token') == token):
                        return True
                    else:
                        return False
            except FileNotFoundError:
                return False

def replace_user(page):
    '''
    this function replaces username in template
    '''
    try:
        page = page.replace('{to_replace_username}' ,request.cookies.get('user').title())
    except:
        pass
    return page

def replace_dashboard_title(page ,name):
    '''
    this function replaces dashboard in the page
    '''

    page = page.replace('{replace_dashboard}' ,name)
    return page
