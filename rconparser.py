import shlex
import re

"""
hostname: [AUS] [Duel] Rissole's Blade Symphony #2
version : 1.0.0.0/1000 5828 secure  
build   : 0.01.03441/103441
udp/ip  :  172.31.21.67:27015 os(Linux) type(dedicated)
map     : duel_monastery
players : 1 humans, 0 bots (8 max) (not hibernating)

# userid name uniqueid connected ping loss state rate adr
# 174 1 "Rissole" STEAM_1:0:16217997 00:31 76 0 active 30000 220.238.50.130:27005
#end
"""
def get_status(rcon):
    status = rcon.exec_command('status')
    ret = {'users': []}
    for line in status.split('\n'):
        if len(line.strip()) == 0 or line.startswith('# user') or line.startswith('#end'):
            continue
        if line.startswith('#'):
            user = shlex.split(line)[1:]
            ret['users'].append({
                'user': user[0],
                'id': user[1],
                'name':   user[2],
                'uniqueid': user[3],
                'connected': user[4],
                'ping': user[5],
                'loss': user[6],
                'state': user[7],
                'rate': user[8],
                'adr': user[9]
            })
            continue
        if ':' not in line:
            continue
        parts = line.split(":", 1)
        keyword = parts[0].strip()
        value = parts[1].strip()
        if keyword == "version":
            ret['version'] = value
        elif keyword == "map":
            ret['map'] = value
        elif keyword == "udp/ip":
            ip_os_type = value.split(' ')
            ret['ip'], ret['port'] = ip_os_type[0].split(':')
            ret['os'] = ip_os_type[1].replace('os', '')[1:-1]
            ret['dedicated'] = ip_os_type[2] == 'type(dedicated)'
        elif keyword == "hostname":
            ret['hostname'] = value
        elif keyword == "players":
            humans_bots_max = re.match(r'(\d+) humans, (\d+) bots \((\d+) max\)', value)
            ret['players_humans'] = int(humans_bots_max.group(1))
            ret['players_bots'] = int(humans_bots_max.group(2))
            ret['players_max'] = int(humans_bots_max.group(3))

    return ret