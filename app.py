import ConfigParser
from flask import *
import srcds.rcon
import rconparser

# Prepare Flask
app = Flask(__name__)

# Load config
config = ConfigParser.ConfigParser()
config.read('config.ini')
RCON_ADDRESS  = config.get('RconInfo', 'address', '')
RCON_PORT     = config.get('RconInfo', 'port', 27015)
RCON_PASSWORD = config.get('RconInfo', 'password', '')

RCON = srcds.rcon.RconConnection(RCON_ADDRESS, RCON_PORT, RCON_PASSWORD)

@app.route("/")
def status():
    status = rconparser.get_status(RCON)
    return render_template('index.htm', users=status['users'])

if __name__ == "__main__":
    app.run(debug=True)