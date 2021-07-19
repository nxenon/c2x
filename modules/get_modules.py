#!/usr/bin/env python3

'''
this script contains modules to get data from files and return desired values
'''

import json
import tkinter
from tkinter import messagebox

def get_config_value(main_key):

    '''
    this function is for reading main/core/config.json file and return value for desired key
    '''

    file = open('main/core/config.json')
    config_file = json.load(file)
    try :
        value = config_file[main_key]
    except :
        print('Error finding : ' + main_key + ' in config.json')
    else:
        return value

def push_text_in_terminal_module(is_from_gui, terminal_window_box, text):
    '''
    this function pushes text in terminal box gui window
    '''
    if not is_from_gui:
        return
    text = text.strip() + '\n'
    terminal_window_box.config(state='normal')
    terminal_window_box.insert(tkinter.END, text)
    terminal_window_box.config(state='disabled')

def show_error(message, is_from_gui, title='Error'):
    if not is_from_gui:
        return
    messagebox.showerror(title=title, message=message)
