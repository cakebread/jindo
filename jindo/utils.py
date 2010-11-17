

"""

utils.py
===========

Misc funcitions
---------------


"""

__docformat__ = 'restructuredtext'

import os

def red(my_string):
     return '\033[0;34m%s\033[0m' % my_string

def get_rc_file():
    """
    Return location we store config files and data
    """
    rcpath = os.path.abspath("%s/.jindorc" % os.path.expanduser("~"))
    if os.path.exists(rcpath):
        return open(rcpath, 'r').read()
    print "Create ~/.jindorc and put this in it: api_key=YOUR API KEY"
    print "You can find your (mt) API key here: https://ac.mediatemple.net/api/index.mt"

def sinsert(original, new, pos):
    '''Inserts new string inside original string at pos'''
    return original[:pos] + new + original[pos:]


def camel_to_human(original):
#Index where capital letters are
    i = 0
    for s in original:
        if s.isupper():
            original = sinsert(original, " ", i)
            i += 1
        i += 1
    original = original.capitalize()
    return red(original)

