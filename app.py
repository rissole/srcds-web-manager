import ConfigParser
from flask import *
import srcds.rcon
import rconparser

# Prepare Flask
app = Flask(__name__)

# Load config
config = ConfigParser.ConfigParser()
config.read('config.ini')

# Set up Rcon connections
RCONS = {}
for section in config.sections():
    try:
        RCONS[section] = srcds.rcon.RconConnection(
            config.get(section, 'address', ''),
            config.get(section, 'port', 27015),
            config.get(section, 'password', '')
        )
    except srcds.rcon.RconError as e:
        print("Invalid config section '%s': %s" % (section, e))

# Routes
@app.route("/")
def status():
    statuses = { name : rconparser.get_status(RCONS[name]) for name in RCONS }
    return render_template('index.htm', statuses=statuses)

if __name__ == "__main__":
    app.run(debug=True)