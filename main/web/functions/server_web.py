#!/usr/bin/env python3

'''
function for managing /server url
'''

from flask import render_template ,redirect
from main.web.functions.web_modules import replace_user ,check_login ,replace_dashboard_title

class ServerWebPage:

    def run(self):
        if not (check_login()): # check if user is logged in ,returns true if is logged in
            return redirect('/login' ,code=302)

        page = self.read_page()
        page = replace_user(page=page)
        page = page.replace('{to_replace_text}', self.add_element())
        page = replace_dashboard_title(page=page, name='Server')
        return page

    def read_page(self):
        template = render_template('dashboard.html')
        return template

    def add_element(self):
        html_text = '''
        <form class="form-inline" method="POST" action="/server_conf" id="server_conf_form">
      <div class="form-group mb-2">
        <label class="sr-only">Listening IP</label>
        <input type="text" class="form-control" id="lip" value="0.0.0.0" placeholder="Listening IP" required>
      </div>
      <div class="form-group mb-2">
        <label class="sr-only">Listening Port</label>
        <input type="text" class="form-control" id="lport" placeholder="Port Number" required>
      </div>
      <button class="btn btn-primary mb-2 start_server_event">Start</button>
      <button class="btn btn-danger mb-2 stop_server_event" disabled>Stop</button>
    </form>
    
    <div class="server_conf_response my-5"></div>
            '''
        return html_text
