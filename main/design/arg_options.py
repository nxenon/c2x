#!/usr/bin/env python3

'''
this is the script for parsing arguments
'''

import argparse

def start_gui():
    from main.gui.main import main_gui_start
    main_gui_start()

def start_web():
    from main.web.main_web import main_web_start
    main_web_start()

def parse_args():
    parser = argparse.ArgumentParser(usage='python3 %(prog)s --web or --gui' + '\n help: python3 %(prog)s --help'
                                           + '\n  Web: python3 %(prog)s --web' +
                                     '\n  GUI: python3 %(prog)s --gui')
    parser.add_argument('--gui', help='Start GUI Window', action='store_true')
    parser.add_argument('--web', help='Start Web Interface', action='store_true')

    args ,unknown = parser.parse_known_args()

    if (args.web):
        start_web()
    elif (args.gui):
        start_gui()
    else:
        parser.print_help()
