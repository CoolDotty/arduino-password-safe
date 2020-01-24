#!/usr/bin/python3

######
#
# This is a helper script which converts exported safeboxes from
# Countermail into a readable directory for the arduino.
#
# Safebox files are a json array of objects where each value is encoded in
# base64 and then the whole thing is encoded in base64.
#
# Drop the safebox on an SD card and the script will unpack it for you.
#
# Tested on Python 3.6.9
#
######

from json import loads
from base64 import b64decode as decode
import os

SAFEBOX_FILE = 'countermail_safebox.asc'

def decodeDescription(cred):
    # Get the most out of the 8.3 filename limitation

    full = decode(cred['short_description']).decode('utf-8')
    if len(full) > 8:
        return full[:8] + '.' + full[8:11]
    else:
        return full

def decodePassword(cred):
    return decode(cred['password']).decode('utf-8')

print('Unpacking safebox file ...')
if not os.path.isfile(SAFEBOX_FILE):
    print ('... Error: new safebox file not found')
    exit(1)
with open(SAFEBOX_FILE, 'r') as cm_file:
    print('Decoding Json ...')
    encoded = cm_file.read()
    decoded = decode(encoded)
    json = loads(decoded)
    print ('... Done!')

    print('Removing deleted creds ...')
    credList = []
    for cred in json:
        credList.append(decodeDescription(cred))
    for fileName in os.listdir('.'):
        if os.path.isfile(os.path.join('.', fileName)):
            if (fileName not in credList and fileName != SAFEBOX_FILE):
                print('-', fileName)
                os.remove(fileName);
    print('... Done!')
    print('Unpacking new creds ...')
    for cred in json:
        description = decodeDescription(cred)
        password = decodePassword(cred)
        needsUpdate = True
        if os.path.isfile(os.path.join('.', description)):
            with open(description, 'r') as file:
                if file.read() == password:
                    needsUpdate = False
        if needsUpdate:
            print('+', description)
            with open(description, 'w') as out:
                out.write(password)
    print('... Done!')
    print('Deleting safebox ...')
    os.remove(SAFEBOX_FILE);
    print('... Done!')
exit(0)
