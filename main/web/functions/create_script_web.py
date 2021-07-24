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
        page = page.replace('{to_replace_text}', self.add_element())
        page = replace_dashboard_title(page=page, name='Create Script')
        return page

    def read_page(self):
        template = render_template('dashboard.html')
        return template

    def add_element(self):
        html_text = '''
        <form class="form-inline" method="POST" action="/create_script_conf" id="create_script_conf_form">
      <div class="form-group mb-2">
        <label class="sr-only">LHost</label>
        <input type="text" class="form-control" id="localhost_create_script" placeholder="LHost" required>
      </div>
      <div class="form-group mb-2">
        <label class="sr-only">LPort</label>
        <input type="text" class="form-control" id="localport_create_script" placeholder="LPort" required>
      </div>
      
    <select class="form-control create_script_lang">
        <option value="python">Python</option>
        <option value="go">Go</option>
    </select>
      <button class="btn btn-success mb-2 my-3 event_create_script">Create Script</button>
    </form>

    <div class="server_create_script_response my-5"></div>
            '''
        return html_text
