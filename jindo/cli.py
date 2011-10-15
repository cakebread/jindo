# pylint: disable-msg=W0613,W0612,W0212,W0511,R0912,C0322,W0704
# W0511 = XXX (my own todo's)

"""

cli.py
======

Desc: Command-line tool for (mt) Media Temple API

Author: Rob Cakebread <rcakebread @ mediatemplet dawt net>

License : BSD


"""

__docformat__ = 'restructuredtext'

import sys
import optparse
import logging

from jindo.utils import get_rc_file
from jindo.jindolib import JindoProxy
from jindo import __version__



class JindoCLI(object):

    """
    Main class for jindo
    """

    def __init__(self, api_key=None):
        #PyPI project name with proper case
        self.options = None
        self.logger = logging.getLogger("jindo")
        self.ansi = True
        if api_key:
            self.api_key = api_key
        else:
            #Obviously not going to work if we add more options.
            self.api_key = get_rc_file().split("=")[1].strip()
        self.jindo = JindoProxy()


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
        data, code, status = self.jindo.fetch_service_details(service, self.api_key)
        #TODO: Raise exceptions based on code/status?
        return data

    def get_services(self):
        '''Return list of all service ids'''
        data, code, status = self.jindo.fetch_services(self.api_key)
        #TODO: Raise exceptions based on code/status?
        return data

    def reboot_server(self, service):
        '''Reboots server'''
        data, code, status = self.jindo.reboot_server(service, self.api_key)
        #TODO: Raise exceptions based on code/status?
        return data

    def add_diskspace(self, service):
        '''Adds temp disk space'''
        data, code, status = self.jindo.add_temp_diskspace(service, self.api_key)
        return data

    def details_all_services(self, ansi=True):
        services = self.get_services()
        for service in services:
            print "Service: %s\n" % service
            json_data = self.get_service_details(service)
            self.jindo.print_service_details(json_data, self.options.format, ansi)
            print "\n"

    def run(self):
        """
        Perform actions based on CLI options

        @returns: status code
        """
        opt_parser = setup_opt_parser()
        (self.options, remaining_args) = opt_parser.parse_args()
        logger = self.set_log_level()

        if self.options.quiet:
            self.ansi = False

        if self.options.jindo_version:
            self.jindo_version()
            return

        if (len(sys.argv) == 1 or len(remaining_args) > 2):
            opt_parser.print_help()
            return 2
        if self.options.service:
            json_data = self.get_service_details(self.options.service)
            self.jindo.print_service_details(json_data, self.options.format, self.ansi)
            return 0
        if self.options.details_all_services:
            self.details_all_services(self.ansi)
            return 0
        elif self.options.service_ids:
            json_data = self.get_services()
            #TODO: Could be formatted better. Ideas? Go for it.
            if self.options.format == 'text':
                if self.options.quiet:
                    print str(json_data).strip(']').lstrip('[')
                else:
                    print "Service IDs: %s" % json_data
            else:
                print json_data
            return 0
        elif self.options.reboot:
            json_data = self.reboot_server(self.options.reboot)
            self.jindo.print_response_details(json_data, self.options.format)
            return 0
        elif self.options.diskspace:
            json_data = self.add_diskspace(self.options.diskspace)
            self.jindo.print_response_details(json_data, self.options.format)
            return 0
        else:
            opt_parser.print_help()
            return 2

    def jindo_version(self):
        """
        Show jindo's version

        @returns: 0
        """
        self.logger.info("Jindo version %s" % __version__)
        return 0


def setup_opt_parser():
    """
    Setup the optparser

    @returns: opt_parser.OptionParser

    """

    usage = "usage: %prog [options]"
    opt_parser = optparse.OptionParser(usage=usage)
    group_info = optparse.OptionGroup(opt_parser,
            "Information Options",
            "The following options perform queries but perform no actions on services:")
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
                          default="text", help= "json OR text (default)")

    group_info.add_option("-i", "--service-ids", action='store_true',
                          dest="service_ids",
                          default=False, help=
                          "Get list of all services for your account.")

    group_info.add_option("-s", "--service-details", action='store',
                          dest="service", metavar="SERVICE_ID",
                          default=False, help= "Get details for a service.")

    group_info.add_option("-l", "--details-all-services", action='store_true',
                          dest="details_all_services",
                          default=False, help=
                          "Get detailed list of all services for your account.")
    group_action = optparse.OptionGroup(opt_parser,
            "Action Options",
            "The following options perform actions on a service:")
    group_action.add_option("-R", "--reboot", action='store',
                          dest="reboot", metavar="SERVICE_ID",
                          default=False, help= "Reboot your server (dv)(ve)")
    group_action.add_option("-A", "--addspace", action="store",
                          dest="diskspace", metavar="SERVICE_ID",
                          default=False, help="Add 1GB of disk space for 6 hours (dv)(ve)")

    opt_parser.add_option_group(group_info)
    opt_parser.add_option_group(group_action)
    return opt_parser



def main():
    """
    Let's do it.
    """
    my_jindo = JindoCLI()
    my_jindo.run()

if __name__ == "__main__":
    sys.exit(main())

