import shlex

def get_status(rcon):
    status = rcon.exec_command('status')
    ret = {'users': []}
    for line in status.split('\n'):
        if line.startswith('#') and not line.startswith('# userid') and line != '#end':
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
            print user
    return ret