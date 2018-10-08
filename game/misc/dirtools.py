"""
dirtools.py
this modules aim is to do stuff.
"""
import os
import io


def gather_tree(dir='.', inputmethod=io.TextIOWrapper.read, previousdict=None):
    """
    gathers this tree into a dict.
    directories will become sub-dictionaries.
    files will become
