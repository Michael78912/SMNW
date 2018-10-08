from py_compile import compile as compile_py
from argparse import ArgumentParser
from json import JSONDecoder
from glob import glob
import os
import sys

__version__ = '0.0'
__author__ = 'Michael Gill'


def version():
    """
    outputs version info to the screen.
    """
    print('compile_all version {__version__} by {__author__}.'.format(
        **globals()))


def main(
        dir=os.path.abspath('.'),
        outputdir='compiled',
        recurse_dirs=False,
        placeinsubdirs=False):
    """
    compiles all files ending in .py or .pyw to
    .pyc files, and places them in outputdir.
    if recurse_dirs == True, then it will be done to
    all subdirectories as well.
    """
    try:
        if glob(os.path.join(dir, '*.py')) + glob(os.path.join(dir,
                                                               '*.pyw')) == []:
            print(dir + ', no python source files found!')
        os.listdir(dir)
    except PermissionError:
        print(dir, 'permission denied!')
        return
    for file in os.listdir(dir):
        if os.path.isdir(os.path.join(dir, file)) and recurse_dirs:
            if placeinsubdirs:
                new_outputdir = os.path.join(outputdir, file)
            else:
                new_outputdir = outputdir
            print('entering', file)
            main(
                dir=os.path.join(dir, file),
                outputdir=new_outputdir,
                recurse_dirs=True,
                placeinsubdirs=placeinsubdirs)

        if not recurse_dirs and os.path.isdir(os.path.join(dir, file)):
            continue

        else:
            if file.endswith(('.py', '.pyw')):
                print('attempting to compile', os.path.join(dir, file))
                print(
                    compile_py(
                        os.path.join(dir, file),
                        os.path.join(outputdir,
                                     '.'.join(file.split('.')[:-1]) + '.pyc')),
                    'compiled.')


if __name__ == '__main__':
    parser = ArgumentParser(
        description='compiles all python files in directory.')
    parser.add_argument(
        '--directory',
        '-d',
        help='the input directory with your python files.')

    parser.add_argument(
        '--output-dir', '-o', help='the output directory for the files to go.')

    parser.add_argument(
        '--recurse-subdirs',
        '-r',
        help='recurse the subdirectories',
        action="store_true")
    parser.add_argument(
        '--place-subfiles-in-subdirs',
        '-p',
        help='store the files from sub-directories in the equivalent sub directories. must be used with the -r option.',
        action='store_true')
    parser.add_argument(
        '--version',
        '-v',
        help='output the version information and exit.',
        action='store_true')

    a = parser.parse_args()
    if a.output_dir is None:
        a.output_dir = os.path.join(os.path.abspath('.'), 'compiled')

    if a.directory is None:
        a.directory = os.path.abspath('.')

    if a.version:
        version()

    else:
        main(
            dir=a.directory,
            outputdir=a.output_dir,
            recurse_dirs=a.recurse_subdirs,
            placeinsubdirs=a.place_subfiles_in_subdirs,
        )
