#!/usr/bin/env python3

'''
This script will be run when --web argument is set instead of gui window
'''

from flask import Flask ,request ,redirect ,render_template, Response
import logging
from time import sleep
from threading import Thread
from modules.get_modules import get_config_value

# if you start the server for first time cookies will be cleared
reset_number = 1 # 1 is restarted and 0 is not restarted
UseSSL = None

def main_web_start(use_ssl):
    UseSSL = use_ssl
    template_folder_path ='main/web/templates/'
    static_folder_path = 'main/web/static/'
    app_main = Flask('__main__' ,template_folder=template_folder_path ,static_folder=static_folder_path)

    # disable flask url logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    @app_main.route('/')
    def index():
        from main.web.functions.index import index
        index = index()
        return index

    @app_main.route('/login')
    def login():
        from main.web.functions.login import login
        if (request.args.get('error')):
            login = login(error=request.args.get('error'))
        else:
            login = login()

        return login

    @app_main.route('/check_login' ,methods=['POST'])
    def check_login():
        from main.web.functions.check_login import CheckLogin
        if request.method == 'POST':
            check = CheckLogin(user=request.form['user'] ,user_pass=request.form['passw'])
            ret = check.run()
            return ret

    @app_main.route('/dashboard')
    def dashboard():
        from main.web.functions.dashboard import Dashboard
        dashboard = Dashboard()
        dashboard_ret = dashboard.run()
        return dashboard_ret

    @app_main.route('/server')
    def server_url():
        from main.web.functions.server_web import ServerWebPage
        server_web_page = ServerWebPage()
        server_ret = server_web_page.run()
        return server_ret

    # Find the last line of the server.txt file
    with open('main/web/static/files/server.txt', 'r') as file_server:
        global index_last_log_server
        index_last_log_server = len(file_server.readlines())

    def stream_server_file():
        # Read server.txt file and return lines
        global index_last_log_server
        while True:
            with open('main/web/static/files/server.txt', 'r') as server_txt_file:
                try:
                    yield server_txt_file.readlines()[index_last_log_server] + '<br>'
                    index_last_log_server += 1
                    sleep(0.2)  # delay to show log in template
                except Exception:
                    continue

    @app_main.route('/server_conf', methods=['POST', 'GET'])
    def server_conf_url():
        if not check_login:
            return redirect('/login' ,code=302)
        elif request.method == 'POST':
            return 'heyyyyyyy'
        elif request.method == 'GET':
            return Response(stream_server_file(), mimetype="text/plain", content_type="text/event-stream")

    @app_main.route('/create_script')
    def create_script_url():
        from main.web.functions.create_script_web import CreateScriptWeb
        create_script_web_ret = CreateScriptWeb().run()
        return create_script_web_ret

    @app_main.route('/zombies')
    def zombies_url():
        from main.web.functions.zombies_web import ZombiesWeb
        zombies_web_ret = ZombiesWeb().run()
        return zombies_web_ret

    @app_main.route('/terminal')
    def terminal_url():
        from main.web.functions.terminal_web import TerminalWeb
        terminal_web_ret = TerminalWeb().run()
        return terminal_web_ret

    @app_main.route('/logout')
    def logout():
        from main.web.functions.logout import logout
        return logout()

    @app_main.route('/forgotpass')
    def forgot_password():
        return redirect('https://github.com/nxenon/c2x/blob/master/docs/forgotpass.md' ,code=302)

    @app_main.route('/docs')
    def docs():
        from main.web.functions.docs import docs
        return docs()

    @app_main.errorhandler(404)
    def page_not_found(e):
        return render_template('404_error.html'), 404

    @app_main.errorhandler(500)
    def internal_error(e):
        msg = '''
        <h1 style="text-align:center">Internal Server Error (500)</h1>
        <br>
        <h2 style="text-align:center">This might be for bad arguments or bad configuration</h2>
        <br>
        <h2 style="text-align:center">You can restart the script</h2>
        '''
        return msg ,500

    @app_main.after_request
    def add_header(response):
        response.headers['Cache-Control'] = 'no-cache'  # tell browser not to cache contents
        return response

    def check_reset():
        # if server is restarted then the cookies are cleared
        global reset_number
        if (reset_number == 1):
            reset_number = 0
            if (request.cookies.get('logged_in') or (request.cookies.get('user'))):
                return logout()
        else:
            return ''

    def print_url_banner():
        sleep(1)
        flask_url_msg = '\n\tWeb interface running on http://' + str(listening_ip) + ':' + str(listening_port) + '/'
        if UseSSL:
            flask_url_msg = flask_url_msg.replace('http', 'https')
        print(flask_url_msg)
        print()

    listening_ip = get_config_value(main_key='web_listen_ip')
    listening_port = get_config_value(main_key='web_listen_port')

    Thread(target=print_url_banner).start()  # start a thread to print http url after flask headers
    ssl_context = None
    if UseSSL:
        ssl_context = 'adhoc'
    app_main.run(port=listening_port, host=listening_ip, ssl_context=ssl_context)
