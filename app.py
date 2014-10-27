import ConfigParser
from flask import *
import srcds.rcon
import rconparser
import json
import socket

# Prepare Flask
app = Flask(__name__)

# Load config
config = ConfigParser.ConfigParser()
config.read('config.ini')

# Set up Rcon connections
RCONS = {}

def refresh_rcons():
    for section in config.sections():
        try:
            RCONS[section] = srcds.rcon.RconConnection(
                config.get(section, 'address', ''),
                config.get(section, 'port', 27015),
                config.get(section, 'password', '')
            )
        except srcds.rcon.RconError as e:
            print("Invalid config section '%s': %s" % (section, e))

refresh_rcons();

# Routes
@app.route("/")
def status():
    try:
        statuses = { name : rconparser.get_status(RCONS[name]) for name in RCONS }
    except socket.error:
        refresh_rcons()
        return status()
    return render_template('index.htm', statuses=statuses)

@app.route("/command", methods=['POST'])
def command():
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

if __name__ == "__main__":
    app.run(debug=True)