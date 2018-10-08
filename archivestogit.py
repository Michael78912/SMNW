import zipfile
import tarfile
import gzip
import bz2
import os
import subprocess
import shutil
import glob
import json

GIT_SCRIPT = """
git clone https://michael78912/smnw-archives
cd smnw-archives
git init
echo copying archives...
cp ../Archives/* .
git add *
git push origin master
"""


def make_xz(file, dir='.'):
    """
    compresses file and saves it to
    [file].xz in the dir.
    """
    os.system('xz -k ' + os.path.join(dir, file))


def make_tarfile(source_dir):
    with tarfile.open(source_dir + '.tar', "w") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def make_gz(file, dir='.'):
    os.system('gzip -k ' + file)


def make_bz2(file, dir='.'):

    os.system('bzip2 -k ' + os.path.join(dir, file))


def make_zipfile(dir):
    print('writing xipfile')
    zipfile.main(['-c', dir + '.zip', dir])


def make_7z(dir):
    print('writeing 7z')
    try:
        os.remove('logs.7z')
    except:
        pass
    old = os.getcwd()
    os.chdir(dir)
    os.system('7z a %s -r' % dir)

    shutil.move('logs.7z', '..')
    os.chdir(old)


def get_ver():
    old_ver_file = json.load(open('/mnt/m/stickman\'s_new_world/game/config/config.json'))
    old_ver = old_ver_file['version']
    new_ver = input('old version: {}. new version: '.format(old_ver))
    old_ver_file['version'] = new_ver
    json.dump(old_ver_file, open('/mnt/m/stickman\'s_new_world/game/config/config.json'))
    with open('Archives/ver.txt', 'w') as verfile:
        verfile.write(new_ver)
    
    

def write_archive():
    for arc in glob.glob('stickman*.*'):
        os.remove(arc)

    for func in (make_zipfile, make_tarfile, make_7z):
        func('logs')

    for arc in glob.glob('logs.*'):
        os.rename(arc, 'stickman\'s new world.' + arc.split('.')[1])

    for func in (make_xz, make_bz2, make_gz):
        func('"stickman\'s new world.tar"')

    shutil.rmtree('Archives')
    os.mkdir('Archives')

    for arc in glob.glob('stickman*.*'):
        shutil.move(arc, 'Archives')
    get_ver()
    os.system('bash tmp.sh')


write_archive()
