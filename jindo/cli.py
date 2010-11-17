# pylint: disable-msg=W0613,W0612,W0212,W0511,R0912,C0322,W0704
# W0511 = XXX (my own todo's)

"""

cli.py
======

Desc: Command-line tool for (mt) Media Temple API

Author: Rob Cakebread <rcakebread @ mediatemplet dawt net>

License : GNU General Public License Version 2 (See COPYING)


"""

__docformat__ = 'restructuredtext'
__revision__ = ''[11:-1].strip()

import sys
import optparse
import logging

#from jindo.jindolib import get_highest_version, Distributions
from jindo.utils import get_rc_file
from jindo.jindolib import fetch_service_details, print_service_details, fetch_services
from jindo.__init__ import __version__ as VERSION


#TODO: Use a real config parser

class Jindo(object):

    """
    Main class for jindo
    """

    def __init__(self):
        #PyPI project name with proper case
        self.options = None
        self.logger = logging.getLogger("jindo")
        self.api_key = get_rc_file().split("=")[1].strip()


    def set_log_level(self):
        """
        Set log level according to command-line options

        @returns: logger object
        """

        if self.options.debug:
            self.logger.setLevel(logging.DEBUG)
        elif self.options.quiet:
            self.logger.setLevel(logging.ERROR)
        else:
            self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())
        return self.logger

    def get_service_details(self, service):
        '''Return details for a specific service'''
        data, code, status = fetch_service_details(service, self.api_key)
        return data

    def get_services(self):
        '''Return list of all service ids'''
        data, code, status = fetch_services(self.api_key)
        return data

    def run(self):
        """
        Perform actions based on CLI options

        @returns: status code
        """
        opt_parser = setup_opt_parser()
        (self.options, remaining_args) = opt_parser.parse_args()
        logger = self.set_log_level()


        if (len(sys.argv) == 1 or len(remaining_args) > 2):
            opt_parser.print_help()
            return 2
        if self.options.service:
            json_data = self.get_service_details(self.options.service)
            print_service_details(json_data, self.options.format)
        elif self.options.service_ids:
            json_data = self.get_services()
            print "Service IDs: %s" % json_data
        else:
            opt_parser.print_help()
            return 2

    def jindo_version(self):
        """
        Show jindo's version

        @returns: 0
        """
        self.logger.info("jindo version %s (rev. %s)" % (VERSION, __revision__))
        return 0


def setup_opt_parser():
    """
    Setup the optparser

    @returns: opt_parser.OptionParser

    """
    #pylint: disable-msg=C0301
    #line too long

    usage = "usage: %prog [options]"
    opt_parser = optparse.OptionParser(usage=usage)

    opt_parser.add_option("--version", action='store_true', dest=
                          "jindo_version", default=False, help=
                          "Show jindo version and exit.")

    opt_parser.add_option("--debug", action='store_true', dest=
                          "debug", default=False, help=
                          "Show debugging information.")

    opt_parser.add_option("-q", "--quiet", action='store_true', dest=
                          "quiet", default=False, help=
                          "Show less output.")

    opt_parser.add_option("-f", "--format", action='store',
                          dest="format",
                          default="text", help= "json OR text")

    opt_parser.add_option("-d", "--get-service-details", action='store',
                          dest="service",
                          default=False, help= "Get details for a service.")

    opt_parser.add_option("-i", "--service-ids", action='store_true',
                          dest="service_ids",
                          default=False, help=
                          "Get list of all services for your account.")

    return opt_parser



def main():
    """
    Let's do it.
    """
    my_jindo = Jindo()
    my_jindo.run()

if __name__ == "__main__":
    sys.exit(main())

