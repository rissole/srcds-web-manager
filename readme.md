SRCDS Server Manager
====================

A simple Source Dedicated Server manager written in *Python 2.7* with Flask.

Features
========

- Monitor status of all your servers
- Kick and ban scrubs from the comfort of your browser window
- Change the map and send messages to your underlings
- Fully functional console, including PER-SERVER history

Setup
=====

1. Install [Flask](http://flask.pocoo.org)
1. Install [pysrcds](https://github.com/pmrowla/pysrcds)
1. Create a `servers.ini` (see `example.ini` for structure)
1. Create an `appsecret` file. This file should simply contain a set of SECRET, random characters. `os.urandom(24)` works great.
1. Create some login credentials with `python create_user.py`. This repo comes included with one set of credentials, admin/admin.
1. `python app.py`, then visit http://localhost:5000/

Auth
====

How does auth in this weird thing work? Good question.

- User accounts are stored in `users.ini` as usernames and hashed passwords.
- To add a new account or change a password, use the provided `create_user.py`. It's pretty self explanatory.
- To delete an account, just edit `users.ini` in a text editor and delete the section of the appropriate user.

## appsecret

Once you're authed, a token is stored on the client as a cookie saying so. This is encrypted using the string in `appsecret`. It's important that it stays secret for this reason. Check out http://flask.pocoo.org/docs/0.10/quickstart/#sessions for more information.

Map Typeahead
=============

The "Change Map" feature includes autocomplete of map names. The list of maps it can autocomplete are stored in `maps.txt`. TF2, CS:GO, and Blade Symphony map names are included by default.
