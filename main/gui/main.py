#!/usr/bin/env python3

'''
Starting Main GUI Function
'''

import json
import tkinter as tk
from tkinter import ttk
from tkinter import *
import webbrowser
from modules.server import ServerModule
from PIL import Image, ImageTk


class C2ServerGUI:
    def __init__(self, main_win):
        with open('main/core/app_info.json') as app_info_json:
            data = json.load(app_info_json)
            self.app_version = data['app_version']  # read app version from file
            default_geometry = data['default_gui_geometry']
        # define GUI settings
        self.main_win = main_win  # main window for login
        self.main_win.title('C2X (Command & Control Toolkit)')
        self.main_win.geometry(default_geometry)
        self.main_win.configure(bg='#2b313b')
        self.main_win.resizable(1, 1)

        # set Frames and Tabs
        tab_control = ttk.Notebook(self.main_win)

        # Home Tab
        tab_home = tk.Frame(tab_control, bg='#2b313b')
        tab_control.add(tab_home, text='                  Home                  ')

        welcome_label_home = Label(tab_home, text='Welcome to C2X', fg='#3399ff', bg='#2b313b', font=('Tahoma', 30))
        welcome_label_home.pack()

        # create a separator
        home_page_separator = Label(tab_home, text='', bg='#2b313b')
        home_page_separator.pack()

        # C2X image
        image_c2x_home = Image.open("./main/gui/icons/c2x_logo_red.jpg")
        image_c2x_home_resize = ImageTk.PhotoImage(image_c2x_home.resize((230, 230), Image.ANTIALIAS))
        label_image_c2x_home = tk.Label(tab_home, image=image_c2x_home_resize)
        label_image_c2x_home.image = image_c2x_home_resize
        label_image_c2x_home.pack()

        # create a separator
        home_page_separator2 = Label(tab_home, text='', bg='#2b313b')
        home_page_separator2.pack()

        quick_tutorial_text_1 = '1) Go to Server tab and config your server'
        quick_tutorial_text_2 = '2) Then start the server'
        quick_tutorial_text_3 = '3) Go to Create Script tab and create a script for your bots to run and connect to your server'
        quick_tutorial_text_4 = '4) Wait for bots to connect to your server'
        quick_tutorial_text_5 = '5) Go to Terminal tab and play with bots :)'

        quick_tutorial_home_1 = Label(tab_home, text=quick_tutorial_text_1, fg='white', bg='#2b313b',
                                      font=('Tahoma', 20), anchor='w')
        quick_tutorial_home_1.pack(fill='both')
        quick_tutorial_home_2 = Label(tab_home, text=quick_tutorial_text_2, fg='white', bg='#2b313b',
                                      font=('Tahoma', 20), anchor='w')
        quick_tutorial_home_2.pack(fill='both')
        quick_tutorial_home_3 = Label(tab_home, text=quick_tutorial_text_3, fg='white', bg='#2b313b',
                                      font=('Tahoma', 20), anchor='w')
        quick_tutorial_home_3.pack(fill='both')
        quick_tutorial_home_4 = Label(tab_home, text=quick_tutorial_text_4, fg='white', bg='#2b313b',
                                      font=('Tahoma', 20), anchor='w')
        quick_tutorial_home_4.pack(fill='both')
        quick_tutorial_home_5 = Label(tab_home, text=quick_tutorial_text_5, fg='white', bg='#2b313b',
                                      font=('Tahoma', 20), anchor='w')
        quick_tutorial_home_5.pack(fill='both')

        # Server Tab
        tab_server = tk.Frame(tab_control, bg='#2b313b')
        tab_control.add(tab_server, text='                  Server                  ')

        listening_ip_server_label = Label(tab_server, text='  Listening IP  ', font=('Tahoma', 18),
                                          bg='#2b313b', fg='white', height=2)
        listening_ip_server_label.grid(row=0, column=0)
        self.listening_ip_server_entry = Entry(tab_server, font=('Ttahoma', 15), width=15)
        self.listening_ip_server_entry.grid(row=0, column=1)

        listening_port_server_label = Label(tab_server, text='    Port  ', font=('Tahoma', 18),
                                            bg='#2b313b', fg='white', height=2)
        listening_port_server_label.grid(row=0, column=2)
        self.listening_port_server_entry = Entry(tab_server, font=('Ttahoma', 15), width=7)
        self.listening_port_server_entry.grid(row=0, column=3)

        # create a separator between start button and port entry field
        separator_server_tab = Label(tab_server, text='           ', bg='#2b313b')
        separator_server_tab.grid(row=0, column=5)

        self.start_server_button = Button(tab_server)
        self.start_server_button.grid(row=0, column=6)
        self.start_server_button.config(text='  Start  ', font=('Tahoma', 18), state='normal',
                                        command=self.button_start_server)

        # create a separator between start button and stop button
        separator2_server_tab = Label(tab_server, text='           ', bg='#2b313b')
        separator2_server_tab.grid(row=0, column=7)

        self.stop_server_button = Button(tab_server)
        self.stop_server_button.grid(row=0, column=8)
        self.stop_server_button.config(text='  Stop  ', font=('Tahoma', 18), state='disabled', fg='Red',
                                       command=self.button_stop_server)

        # Create Script Tab
        tab_bot_script = tk.Frame(tab_control, bg='#2b313b')
        tab_control.add(tab_bot_script, text='               Create Script                ')

        lhost_create_script_label = Label(tab_bot_script, text='  LHost  ', font=('Tahoma', 18), bg='#2b313b',
                                          fg='white', height=2)
        lhost_create_script_label.grid(row=0, column=0)
        self.lhost_create_script_entry = Entry(tab_bot_script, font=('Ttahoma', 15), width=15)
        self.lhost_create_script_entry.grid(row=0, column=1)

        lport_create_script_label = Label(tab_bot_script, text='    LPort  ', font=('Tahoma', 18), bg='#2b313b',
                                          fg='white', height=2)
        lport_create_script_label.grid(row=0, column=2)
        self.lport_create_script_entry = Entry(tab_bot_script, font=('Ttahoma', 15), width=7)
        self.lport_create_script_entry.grid(row=0, column=3)

        # create a separator between start button and port entry field
        separator_create_script_tab = Label(tab_bot_script, text='           ', bg='#2b313b')
        separator_create_script_tab.grid(row=0, column=5)

        create_script_button = Button(tab_bot_script)
        create_script_button.grid(row=0, column=6)
        create_script_button.config(text='  Create  ', font=('Tahoma', 18), state='normal',
                                    command=self.button_create_script)

        # Zombies Tab
        self.tab_bots = tk.Frame(tab_control, bg='#2b313b')
        tab_control.add(self.tab_bots, text='                 Zombies                ')

        # create a separator
        bots_separator = Label(self.tab_bots)
        bots_separator.grid(row=0)
        bots_separator.config(bg='#2b313b', state='disabled', font=('Tahoma', 5))

        # Terminal Tab
        tab_terminal = tk.Frame(tab_control, bg='#2b313b')
        tab_control.add(tab_terminal, text='                  Terminal                  ')

        terminal_label = Label(tab_terminal, text='Terminal', font=('Tahoma', 20), bg='#2b313b', fg='white')
        terminal_label.pack()

        self.terminal_window_box = Text(tab_terminal)

        self.terminal_window_box.pack()
        self.terminal_window_box.config(width='72', height='20', bg='#1b1d23', state='normal', fg='white',
                                        font=('Tahoma', 15))
        self.push_text_in_terminal_box(text='!help for help')

        # create a separator between terminal box and command box
        terminal_separator_text_box = Text(tab_terminal)
        terminal_separator_text_box.pack()
        terminal_separator_text_box.config(width='108', height='0', bg='#2b313b', state='disabled')

        self.terminal_exec_command_box = Text(tab_terminal)
        self.terminal_exec_command_box.pack()
        self.terminal_exec_command_box.config(width='71', height='2', padx=5, pady=5, state='normal',
                                              font=('Tahoma', 15))

        # create a separator between command box and exec button
        terminal_separator_2 = Label(tab_terminal)
        terminal_separator_2.pack()
        terminal_separator_2.config(bg='#2b313b', state='disabled', font=('Tahoma', 1))

        self.terminal_exec_button = Button(tab_terminal)
        self.terminal_exec_button.pack()
        self.terminal_exec_button.config(text='   Exec   ', font=('Tahoma', 18), state='disabled', command=self.exec_command)

        # About Tab
        tab_about = tk.Frame(tab_control, bg='#2b313b')
        tab_control.add(tab_about, text='                  About                  ')
        # About Tab Content
        label_app_name = Label(tab_about, text='C2X (Command & Control Toolkit)', font=('Tahoma', 25),
                               bg='#2b313b', fg='white')
        label_app_name.pack()

        label_app_version = Label(tab_about, text='Version : ' + self.app_version, font=('Tahoma', 16),
                                  fg='#3399ff', bg='#2b313b')
        label_app_version.pack()

        # create a separator
        home_page_separator = Label(tab_about, text='', bg='#2b313b')
        home_page_separator.pack()

        # C2X image
        image_c2x_about = Image.open("./main/gui/icons/c2x_logo.jpg")
        image_c2x_about_resize = ImageTk.PhotoImage(image_c2x_about.resize((310, 310), Image.ANTIALIAS))
        label_image_c2x_home = tk.Label(tab_about, image=image_c2x_about_resize)
        label_image_c2x_home.image = image_c2x_about_resize
        label_image_c2x_home.pack()

        about_note_text = '''

C2X is a C2/Post-Exploitation Framework for Red Teaming and Ethical Hacking
        '''
        label_about_note = Label(tab_about, text=about_note_text, font=('Tahoma', 20), fg='#FF9933', bg='#2b313b')
        label_about_note.pack()

        def callback(url):
            webbrowser.open_new(url)

        label_githublink_about = Label(tab_about, text='𝙶̲𝚘̲ ̲𝚃̲𝚘̲ ̲ ̲𝙶̲𝚒̲𝚝̲𝚑̲𝚞̲𝚋̲', fg='#3399ff',
                                       font=('Tahoma', 16), cursor='hand2', bg='#2b313b')
        label_githublink_about.pack()
        label_githublink_about.bind("<Button-1>", lambda e: callback('https://github.com/nxenon/c2x'))

        tab_control.pack(expand=1, fill='both')

    # def buttons functions
    def button_start_server(self):
        self.server_module = ServerModule(lip=self.listening_ip_server_entry.get(),
                                          lport=self.listening_port_server_entry.get(),
                                          zombies_gui_tab=self.tab_bots)
        self.server_module.start_server()
        if self.server_module.connection_status:
            self.server_socket = self.server_module.server_socket
            self.stop_server_button.config(state='normal')
            self.start_server_button.config(state='disabled')

            self.terminal_exec_button.config(state='normal')

            self.push_text_in_terminal_box(text='--------Server Started--------')

    def button_stop_server(self):
        self.stop_server_button.config(state='disabled')
        self.start_server_button.config(state='normal')
        self.server_module.stop_server()

        self.terminal_exec_button.config(state='disabled')

        self.push_text_in_terminal_box(text='--------Server Stopped--------')

    def button_create_script(self):
        from modules.create_script import ScriptCreator
        lhost = self.lhost_create_script_entry.get()
        lport = self.lport_create_script_entry.get()
        script_creator = ScriptCreator(lhost=lhost, lport=lport)
        script_creator.create()

    def push_text_in_terminal_box(self, text):
        text = text.strip() + '\n'
        self.terminal_window_box.config(state='normal')
        self.terminal_window_box.insert(END, text)
        self.terminal_window_box.config(state='disabled')

    def exec_command(self):
        command_text = self.terminal_exec_command_box.get('1.0',END)
        self.terminal_exec_command_box.delete('1.0',END)
        self.terminal_window_box.config(state='normal')
        self.terminal_window_box.insert(END,command_text.strip() + '\n')
        self.terminal_window_box.config(state='disabled')
        self.server_module.send_command_from_terminal(self.terminal_window_box, command_text)

def main_gui_start():
    root = tk.Tk()
    photo = PhotoImage(file='./main/gui/icons/c2x_logo_black.png')
    root.iconphoto(False, photo)
    gui = C2ServerGUI(root)
    root.mainloop()
