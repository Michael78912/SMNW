# -*- coding: utf-8 -*-
"""
auto_installer.py
this file downloads the new version of stickmanranger and installs it
"""
__author__ = 'Michael Gill'
__version__ = '0.0'

from queue import Queue
from platform import system
import tkinter as tk
import threading
import json
import ctypes
import sys
import urllib.request
import shutil
import tarfile
import os

Q = Queue()
PRINT_LOCK = threading.Lock()


class InstallWindow(tk.Frame):
    destroyed = False

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        master.protocol("WM_DELETE_WINDOW", self.cancel_install)
        self.master = master
        master.title('auto-updater')
        self.but = tk.Button(
            master, text='cancel', command=self.cancel_install)
        self.but.pack()
        self.but.place(relx=0.4, rely=0.7)
        self.pack()

    def cancel_install(self):
        self.destroyed = True
        self.master.destroy()

    def check_queue(self):
        if Q.empty():
            return False

        data = Q.get()
        # the versions have been loaded
        print('is "data" a dict?:', isinstance(data, dict))
        print('data:', data)
        if data is None:
            self.label = tk.Label(self.master, text='No updates available')
            self.label.pack()
            self.label.place(relx=0.0, rely=0.1)
            self.but.destroy()
            close_but = tk.Button(
                self.master, text='close', command=self.cancel_install)
            close_but.pack()
            close_but.place(relx=0.4, rely=0.7)

        if isinstance(data, dict):
            data_string = 'current version: {current version} available version: {available version}'.format(
                **data)
            print('before tk.Label')
            self.label = tk.Label(self.master, text=data_string)
            print('after tk.Label')
            self.label.pack()
            self.label.place(relx=0.0, rely=0.1)
            print('hello')
            self.install_but = tk.Button(
                self.master, text='install', command=lambda: run(self))
            print('helo again')
            self.install_but.pack()
            self.install_but.place(relx=0.2, rely=0.7)
            print('howdy')

        elif isinstance(data, str):
            self.label.destroy()
            self.label = tk.Label(self.master, text=data)
            self.label.pack()
            self.label.place(relx=0.0, rely=0.1)


if system() not in ('Linux', 'Windows'):
    raise TypeError('Not made for this %a' % system())

VER_URL = "https://drive.google.com/uc?export=download&id=17KGPTgF6xWKH3dk7Sd74niL548WU6Tts"
ARCHIVE_URL = "https://github.com/Michael78912/smnw-archives/blob/master/stickman's%20new%20world.tar.gz"
# temporary directory. use os.environ because it changes in windows
TEMP_PATH = '/tmp' if system() == 'Linux' else os.environ['TMP']
INSTALL_PATH = os.path.join(
    os.environ['HOME'], '.stickman\'s new world/') if system(
    ) == 'Linux' else "C:\\Program Files (x86)\\stickman\'s new world\\"


def run(obj):
    obj.install_but.destroy()
    obj.but.destroy()
    threading.Thread(target=main, daemon=True).start()


def main():

    Q.put('fetching stickmanranger.tar.gz...')
    with urllib.request.urlopen(ARCHIVE_URL,) as response, \
     open(os.path.join(TEMP_PATH, 'stickmanranger.tmp.tar.gz'), 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

    if os.path.exists(INSTALL_PATH + 'game'):
        Q.put('removing previous installation')
        shutil.rmtree(INSTALL_PATH + 'game')

# extract all contents to the path
    Q.put('extracting contents')
    tarfile.open(os.path.join(
        TEMP_PATH,
        'stickmanranger.tmp.tar.gz')).extractall(INSTALL_PATH + 'game')
    Q.put('installation complete\nplease restart stickmans new world.')


def check():
    data = {}
    # VER_URL is a shared google drive link that has the current version of stickmanranger
    with urllib.request.urlopen(VER_URL) as response:
        version = response.read().decode()
    # decode the current version from "settings.json"
    current_version = json.JSONDecoder().decode(
        open('..{0}game{0}config{0}linux_config.json'.format(
            '\\' if os.name == 'nt' else '/')).read())['version']
    # if the version is the same
    with PRINT_LOCK:
        print(current_version, version)
    data['current version'] = current_version
    data['available version'] = version

    if data['current version'] == data['available version']:
        Q.put(None)
    else:
        Q.put(data)

    if current_version == version:
        with PRINT_LOCK:
            print('no new updates')
        return False


def start_thread():
    """
	starts the thread for the actual installation,
	and use main thread for window.
	"""
    root = tk.Tk()
    root.geometry('300x200')
    window = InstallWindow(root)
    # create thread for window, as mainloop cannot run other code at the same time
    install_thread = threading.Thread(target=check, daemon=True)
    install_thread.start()
    while not window.destroyed:
        try:
            window.check_queue()
        except:  # 'cancel' button has been clicked, continue
            ...
        if not window.destroyed: root.update()


def is_admin():
    """
	return true if the program was run as an  administrator
	code not by me. thanks Martín De la Fuente!
	https://stackoverflow.com/questions/130763/request-uac-elevation-from-within-a-python-script
	"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def name_main(started_from_main_=False):
    global started_from_main
    started_from_main = started_from_main_
    if __name__ == '__main__':
        if system() == 'Windows':
            if is_admin():
                start_thread()

            else:
                # Re-run the program with admin rightsos.getlogin = lambda: pwd.getpwuid(os.getuid())[0]
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, __file__, None, 1)
        if system() == 'Linux':
            start_thread()


name_main()
