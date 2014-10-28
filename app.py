import ConfigParser
from flask import *
import srcds.rcon
import rconparser
import json
import socket
import hashlib

# Prepare Flask
app = Flask(__name__)

# Load config
servers_config = ConfigParser.ConfigParser()
servers_config.read('servers.ini')
with open('maps.txt') as f:
    MAPS = filter(lambda l: not l.startswith('#'), f.read().split('\n'))
users_config = ConfigParser.ConfigParser()
users_config.read('users.ini')

# Set up Rcon connections
RCONS = {}

def refresh_rcons():
    for section in servers_config.sections():
        try:
            RCONS[section] = srcds.rcon.RconConnection(
                servers_config.get(section, 'address', ''),
                servers_config.get(section, 'port', 27015),
                servers_config.get(section, 'password', '')
            )
        except srcds.rcon.RconError as e:
            print("Invalid server config section '%s': %s" % (section, e))

refresh_rcons();

# Routes
@app.route("/")
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    try:
        statuses = { name : rconparser.get_status(RCONS[name]) for name in RCONS }
    except socket.error:
        refresh_rcons()
        return index()
    return render_template('index.htm', statuses=statuses)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.htm')
    if request.method == 'POST':
        user = request.form['username']
        if users_config.has_section(user):
            m = hashlib.sha256()
            m.update(users_config.get(user, 'salt', ''))
            m.update(request.form['password'])
            if m.hexdigest() == users_config.get(user, 'hash', ''):
                session['username'] = user
                return redirect(url_for('index'))
            else:
                return render_template('login.htm', invalid=True)
        else:
            return render_template('login.htm', invalid=True)

@app.route("/status")
def status():
    try:
        statuses = { name : rconparser.get_status(RCONS[name]) for name in RCONS }
    except socket.error:
        refresh_rcons()
        return status()
    return json.dumps(statuses)

@app.route("/command", methods=['POST'])
def command():
    if 'username' not in session:
        abort(401)
    server = request.form['server']
    if server not in RCONS:
        return json.dumps({'success': False, 'error': 'Invalid server name'})
    command = request.form['command']
    if command.strip() == "":
        return json.dumps({'success': True, 'result': ''})

    try:
        rconparser.get_status(RCONS[server])
    except socket.error:
        refresh_rcons()
        
    try:
        result = RCONS[server].exec_command(command)
    except RconError as e:
        return json.dumps({'success': False, 'error': str(e)})
    
    return json.dumps({'success': True, 'result': result})

@app.route("/maps")
def maps():
    return json.dumps(MAPS)

if __name__ == "__main__":
    try:
        app.secret_key = open('appsecret').read()
        app.run()
    except IOError:
        print('You need to create an "appsecret" file! Read the readme for more information.')
    