#!/usr/bin/env python3

'''
this script is for starting program functions
'''

from main.design.banner import print_banner
from main.design.arg_options import parse_args

def start():
    print_banner()
    parse_args()
