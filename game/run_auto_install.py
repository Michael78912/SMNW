import subprocess
import platform
import os

if os.getcwd().endswith('game'):
    os.chdir('..{0}updater'.format('\\' if os.name == 'nt' else '/'))

CMD = {
    'Windows':
    'auto_install.exe'
    if os.path.exists('auto_install.exe') else ' python auto_install.py',
    'Linux':
    'auto_install'
    if os.path.exists('auto_installl') else '/usr/bin/python3 auto_install.py'
}[platform.system()].split()

subprocess.Popen(CMD)
# kill the current process
raise SystemExit
