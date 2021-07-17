#!/usr/bin/env python3

'''
this script is for /create_script page
'''

from flask import render_template,redirect
from main.web.functions.web_modules import check_login ,replace_user ,replace_dashboard_title

class CreateScriptWeb:

    def run(self):
        if not (check_login()):  # check if user is logged in ,returns true if is logged in
            return redirect('/login' ,code=302)

        page = self.read_page()
        page = replace_user(page=page)
        page = page.replace('{to_replace_text}' ,'')
        page = replace_dashboard_title(page=page, name='Create Script')
        return page

    def read_page(self):
        template = render_template('dashboard.html')
        return template
