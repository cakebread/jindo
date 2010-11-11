

"""

utils.py
===========

Misc funcitions
---------------


"""

__docformat__ = 'restructuredtext'

import os



def get_rc_file():
    """
    Return location we store config files and data
    """
    rcpath = os.path.abspath("%s/.jindorc" % os.path.expanduser("~"))
    if os.path.exists(rcpath):
        return open(rcpath, 'r').read()
    print "Create ~/.jindorc and put this in it: api_key=YOUR API KEY"
    print "You can find your (mt) API key here: https://ac.mediatemple.net/api/index.mt"

