"""settings.py- displays and changes the settings
for stickman's new world.
if the user settings
"""
import tkinter as tk
import os
import json
import platform
try:
    import pwd
except ImportError:
    # the OS is not linux
    pass

__all__ = ['main', 'load_settings', 'save']

if platform.system() == 'Linux':
    os.getlogin = lambda: pwd.getpwuid(os.getuid())[0]

DEF_NAME = 'settings.json'
USR_NAME = '.stickman_new_world{0}user_settings.json'.format(
    '\\' if os.name == 'nt' else '/')
HOME = 'C:\\Users\\{}\\'.format(
    os.getlogin()) if os.name == 'nt' else '/home/{}/'.format(os.getlogin())
print(HOME)
print()

SETTINGS_FILE_PATH = {
    'posix':
    HOME + USR_NAME if os.path.exists(HOME + USR_NAME) else 'settings.json',
    'nt':
    HOME + USR_NAME if os.path.exists(HOME + USR_NAME) else 'settings.json'
}[os.name]

SETTINGS_FILE = open(SETTINGS_FILE_PATH).read()

USR_SAVE_PATH = HOME + '{0}.stickman_new_world{0}'.format(
    '\\' if os.name == 'nt' else '/')
USR_SAVE_FILE = HOME + USR_NAME

print(USR_SAVE_PATH)
print(SETTINGS_FILE_PATH)


def load_settings():
    settings = json.JSONDecoder().decode(SETTINGS_FILE)
    return settings


def main():
    root = tk.Tk()
    root.geometry('300x200')
    root.title('settings')
    root.protocol('WM_DELETE_WINDOW', lambda: save(usr_settings, root))

    settings = load_settings()
    settings_ = {}
    print(settings)
    for key, value in zip(settings, settings.values()):
        if isinstance(value, bool):
            settings_[key] = value
    settings = settings_
    print(settings)
    usr_settings = settings.copy()

    for i in usr_settings:
        var = tk.IntVar()
        var.set(usr_settings[i])
        usr_settings[i] = var

    for key, value, num in zip(settings, settings.values(), range(
            len(settings))):
        print(key, value, usr_settings)
        tk.Checkbutton(
            root, text=key, variable=usr_settings[key]).grid(
                row=num, sticky=tk.W)

    tk.mainloop()


def save(settings, win):

    for i in settings:
        # the settings are still IntVars
        var = bool(settings[i].get())
        # change them to normal ints
        settings[i] = var

    win.destroy()

    if not os.path.exists(USR_SAVE_PATH):
        os.mkdir(USR_SAVE_PATH)

    # i like having an indent, for when i look at it :)
    json_settings = json.dumps(settings, indent=4)

    with open(USR_SAVE_FILE, 'w') as settings_file:
        settings_file.write(json_settings)


main()
