#!/usr/bin/env python3

'''
function for managing /server url
'''

from flask import render_template ,redirect, jsonify, Response
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
    
    <p class="show_server_status"></p>
    
    <button class="btn btn-dark my-1 clear_server_history">Clear Server History</button>
    
    <div class="server_conf_response my-5"></div>
            '''
        return html_text

def server_conn_check_func(server_module_var):
    if not check_login():
        return redirect('/login', code=302)

    if ((server_module_var is not None) and (server_module_var.connection_status)):
        temp_list = [server_module_var.listening_ip, server_module_var.listening_port]
        return jsonify(temp_list)

    return 'Server Check Request Sent'

def server_conf_url_func(streamer_function):
    # streamer_function param is for get lines from server.txt file

    if not (check_login()):  # check if user is logged in ,returns true if is logged in
        return redirect('/login', code=302)

    return Response(streamer_function(), mimetype="text/plain", content_type="text/event-stream")

