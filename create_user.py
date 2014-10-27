import hashlib
import ConfigParser
import getpass

users_config = ConfigParser.ConfigParser()
users_config.read('users.ini')
m = hashlib.sha512()

user = raw_input('Username: ')

if not users_config.has_section(user):
    print('Will create NEW ACCOUNT "%s".' % (user,))
    users_config.add_section(user)
else:
    print('Will CHANGE PASSWORD for user "%s".' % (user,))
    
while True:
    pw1 = getpass.getpass('Enter password for user: ')
    pw2 = getpass.getpass('Confirm password: ')
    if pw1 == pw2:
        break
    else:
        print('Password mismatch.')

m.update(pw1)
users_config.set(user, 'hash', m.hexdigest())

with open('users.ini', 'wb') as configfile:
    users_config.write(configfile)
    
print('Success.')