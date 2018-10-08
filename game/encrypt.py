"""
encrypt.py- encrypter for stickmanranger save files.
I want people to be able to mad this game, but i dont 
necessarily want people to be able to change it up 
super easily!"""
from cryptography.fernet import Fernet
from itertools import count
import os
import shutil
import time

if not os.name == 'nt':
    os.getlogin = lambda: __import__('pwd').getpwuid(os.getuid())[0]

CURRENT_TIME = time.asctime()
PATH = {
    'nt': 'C:\\Users\\{}\\.stickman_new_world\\save\\'.format(os.getlogin()),
    'posix': '/home/{}/.stickman_new_world/save/'.format(os.getlogin()),
}[os.name]

PATH_NUMERIC = os.path.join(PATH, '%s') + '\\' if os.name == 'nt' else '/'
print(PATH_NUMERIC)

if not os.path.exists(PATH):
    os.makedirs(PATH)

FILE = PATH + '.smr-save'
print(FILE)


def encrypt(string):
    if not os.path.exists(PATH):
        os.makedirs(PATH)

    prev_key = os.listdir(PATH)
    for f in prev_key:
        if not f in ('.smr-save', 'time'):
            os.remove(PATH + f)

    prev_dir = 0
    for number in count():
        if os.path.exists(PATH_NUMERIC % number):
            prev_dir = number

        else:
            # the system can't find this file, but it will only
            # be the first one it doesnt find.
            prev_dir = number
            break

    def_path = PATH
    # os.mkdir(def_path)

    key = Fernet.generate_key()
    # simply make a file with that name
    with open(def_path + key.decode(), 'w'):
        pass

    encrypter = Fernet(key)
    cipher = encrypter.encrypt(string.encode())

    with open(FILE, 'wb') as cipher_file:
        cipher_file.write(cipher)

    with open((os.path.join(def_path, 'time')), 'w') as time_file:
        time_file.write(CURRENT_TIME)
    return cipher


def decrypt(spec=None):
    prev_dir = spec

    if spec is None:
        prev_dir = 0
        for number in count():
            if os.path.exists(PATH_NUMERIC % number):
                prev_dir = number

            else:
                # the system can't find this file, but it will only
                # be the first one it doesnt find.
                break

    data = open(FILE, 'rb').read()
    key = os.listdir(PATH)
    key.pop(key.index('.smr-save'))
    key.pop(key.index('time'))
    key = key[0].encode()

    encrypter = Fernet(key)
    text = encrypter.decrypt(data).decode()

    saved_time = open(os.path.join(PATH, 'time')).read()

    return text, saved_time


if __name__ == '__main__':
    time = __import__('time').asctime()
    print(encrypt(open('misc\\shello.ini').read()))
    print(decrypt()[0], decrypt()[1], sep='\n\n\n')
