#!/usr/bin/env python3

'''
this is the script for parsing arguments
'''

import argparse

def start_gui():
    from main.gui.main import main_gui_start
    main_gui_start()

def start_web(use_ssl):
    from main.web.main_web import main_web_start
    main_web_start(use_ssl=use_ssl)

def parse_args():
    parser = argparse.ArgumentParser(usage='python3 %(prog)s --web or --gui' + '\n help: python3 %(prog)s --help'
                                           + '\n  Web: python3 %(prog)s --web' +
                                     '\n  GUI: python3 %(prog)s --gui')
    parser.add_argument('--gui', help='Start GUI Window', action='store_true')
    parser.add_argument('--web', help='Start Web Interface', action='store_true')
    parser.add_argument('--no-https', help='Disable HTTPS for Web Interface', action='store_true')

    args ,unknown = parser.parse_known_args()

    if (args.web):
        use_ssl = True # True if --no-https arg is not set
        if args.no_https:
            use_ssl = None
        start_web(use_ssl=use_ssl)
    elif (args.gui):
        start_gui()
    else:
        parser.print_help()
