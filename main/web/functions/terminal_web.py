#!/usr/bin/env python3

'''
this script is for /terminal page
'''

from flask import render_template,redirect,Response
from main.web.functions.web_modules import check_login ,replace_user ,replace_dashboard_title

class TerminalWeb:

    def run(self):
        if not (check_login()):  # check if user is logged in ,returns true if is logged in
            return redirect('/login' ,code=302)

        page = self.read_page()
        page = replace_user(page=page)
        page = page.replace('{to_replace_text}', self.add_element())
        page = replace_dashboard_title(page=page, name='Terminal')
        return page

    def read_page(self):
        template = render_template('dashboard.html')
        return template

    def add_element(self):
        html_text = '''        
<div class="terminal" data-content="C2X Terminal">
    <div class="terminal-body">
  <p></p>
    </div>
</div>
<br>
<button class="btn btn-primary mb-2 clear_terminal_history">Clear Terminal History</button>

        '''
        return html_text

def terminal_get_output_url_func(streamer_function):
    # streamer_function is function for get terminal.txt file

    if not (check_login()):  # check if user is logged in ,returns true if is logged in
        return redirect('/login', code=302)

    return Response(streamer_function(), mimetype="text/plain", content_type="text/event-stream")
