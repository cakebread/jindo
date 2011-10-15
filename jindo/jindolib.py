
import sys
import logging
try:
    import json
except:
    import simplejson as json
import httplib

from jindo.utils import camel_to_human



'''

jindolib.py
==========

Desc: Library for (mt) Media Temple's API


Author: Rob Cakebread <cakebread a t gmail d0t c0m>

License  : BSD

'''

__docformat__ = 'restructuredtext'

RESPONSE_CODES = {
        200: 'Success',
        201: 'Successfully Created',
        202: 'Request accepted but not yet processed',
        400: 'There was an error in the request input',
        401: 'Not Authorized. The authenticated user does not have permission to perform the operation',
        402: 'Permission Denied. The specified credentials are invalid',
        404: 'The specified resource was not found',
        409: 'The specified operation is already in progress.',
        500: 'Internal Server Error',
        503: 'Service Unavailable'
}

RESPONSE_KEYS = [
        'statusCode',
        'timeStamp',
        'date',
        'errors',
        'custom'
]

SERVICE_KEYS= ['accessDomain',
        'addons',
        'billingStatus',
        'billingStatusText',
        'hostServer',
        'ipAddresses',
        'operatingSystem',
        'operatingSystemName',
        'primaryDomain',
        'serviceType',
        'serviceTypeName',
]

logger = logging.getLogger('jindo')
logger.setLevel(logging.INFO)


class JindoProxy(object):

    '''
    Class for jindo XML-RPC proxy

    '''

    def __init__(self):
        '''init great?'''
        pass

    def print_service_details(self, json_data, format='text', ansi=True):
        '''Print details of a service
        format: text OR json
        ansi: True OR False (ansi colored text)
        '''
        if format == 'json':
            print json_data
            return
        elif format == 'text':
            for key in SERVICE_KEYS:
                if key == 'ipAddresses':
                    print camel_to_human(key, ansi) + ":"
                    for ip in json_data['service']['ipAddresses']:
                        print "    " + ip
                elif key == 'addons':
                    print camel_to_human(key, ansi) + ":"
                    for addon in json_data['service']['addons']:
                        print "    " + addon['description']

                elif key == 'billingStatus' or key == 'serviceType' or key == 'operatingSystem':
                    #These are integers, we show the text instead
                    #We'll only show if ---debug
                    logger.debug(camel_to_human(key, ansi) + ":")
                    logger.debug(json_data['service'][key])
                else:
                    if json_data['service'][key]:
                        print camel_to_human(key, ansi) + ":"
                        print '    ' + json_data['service'][key]
                    else:
                        #We are skipping a field that doesn't apply, such as
                        #alternateDomain for a (dv) Dedicated-Virtual Server
                        #DEBUG
                        pass
        else:
            print "Error: No such format: %s" % format

    def print_response_details(self, json_data, format='text', ansi=True):
        '''Prints the response all pretty like'''
        if format == 'json':
            print json_data
            return
        elif format == 'text':
            for key in RESPONSE_KEYS:
                if key == 'statusCode':
                    print camel_to_human(key, ansi) + ":"
                    print "    " + str(json_data['response'][key]) + " " + RESPONSE_CODES[json_data['response'][key]]

                elif key == 'timeStamp':
                   self.logger.debug(camel_to_human(key) + ":", ansi)
                   self.logger.debug(json_data['response'][key])

                elif key == 'errors':
                    print camel_to_human(key, ansi) + ":"
                    for error in json_data['response']['errors']:
                        print "    " + error['message']

                elif key == 'custom':
                    pass

                else:
                    if json_data['response'][key]:
                        print camel_to_human(key, ansi) + ":"
                        print '    ' + json_data['response'][key]
                    else:
                        pass
        else:
            print "Error: No such format: %s" % format

    def add_temp_diskspace(self, service, api_key):
        '''Adds 1 GB temporary disk space for 6 hours'''

        c = httplib.HTTPSConnection("api.mediatemple.net")
        c.request("POST", "/api/v1/services/%s/disk/temp.json?apikey=%s" % (service, api_key))
        response = c.getresponse()
        json_data = json.loads(response.read())

        if response.status == 403:
            print "The service may not be associated with this API key."
            #Blah blah, exception handling, blah blah, refactor code
            sys.exit(2)
        return json_data, response.status, response.reason


    # By service ID:
    # c.request("POST", "/api/v1/services/%s/disk/temp.json?apikey=%s" % (service, api_key))
    # c.request("POST", "/api/v1/services/%s/reboot.json?apikey=%s" % (service, api_key))
    # c.request("GET", "/api/v1/services/%s.json?apikey=%s" % (service, api_key))

    # Only by API key
    # c.request("GET", "/api/v1/services/ids.json?apikey=%s" % api_key)



    def make_request(self, api_key, action, service=None):
        '''

        Make an HTTP request to the API server and return results or raise exception

        '''

        conn = httplib.HTTPSConnection("api.mediatemple.net")
        if service:
            conn.request("POST", "/api/v1/services/%s/%s.json?apikey=%s" % (service, action, api_key))
        else:
            #Used to get list of service IDs etc
            conn.request("POST", "/api/v1/services/%s.json?apikey=%s" % (action, api_key))
        response = conn.getresponse()
        json_data = json.loads(response.read())

        if response.status == 403:
            print "The service may not be associated with this API key."
            #He'll work on exception handling when he refactors the httplib code
            sys.exit(2)
        return json_data, response.status, response.reason

    def reboot_server(self, service, api_key):
        '''Reboots your server. Returns response if successful'''

        #response = make_request(id, service, action)
        c = httplib.HTTPSConnection("api.mediatemple.net")
        c.request("POST", "/api/v1/services/%s/reboot.json?apikey=%s" % (service, api_key))
        response = c.getresponse()
        json_data = json.loads(response.read())

        if response.status == 403:
            print "The service may not be associated with this API key."
            #He'll work on exception handling when he refactors the httplib code
            sys.exit(2)
        return json_data, response.status, response.reason

    def fetch_services(self, api_key):
        '''Returns list of services associated with an account'''
        c = httplib.HTTPSConnection("api.mediatemple.net")
        c.request("GET", "/api/v1/services/ids.json?apikey=%s" % api_key)
        response = c.getresponse()
        json_data = json.loads(response.read())

        if not json_data.has_key('serviceIds'):
            print response.status, response.reason
            if response.status == 403:
                print "The service may not be associated with this API key."
            #I'll work on exception handling when I refactor the httplib code
            sys.exit(2)
        return json_data['serviceIds'], response.status, response.reason

    def fetch_service_details(self, service, api_key, debug=False):
        '''param: json_data - JSON data
        param: format - text or json
        rtype: None
        '''

        c = httplib.HTTPSConnection("api.mediatemple.net")
        c.request("GET", "/api/v1/services/%s.json?apikey=%s" % (service, api_key))

        response = c.getresponse()
        json_data = json.loads(response.read())
        if not json_data.has_key('service'):
            print response.status, response.reason
            if response.status == 403:
                print "The service may not be associated with this API key."
            #I'll work on exception handling when I refactor the httplib code
            sys.exit(2)

        if debug:
            if response.status:
                print response.status
            if response.reason:
                print response.reason
        return json_data, response.status, response.reason

    def parse_json(self, result):
        '''Simply loads a string into JSON'''
        return json.loads(result)

def parse_service(json_data):
    '''Parses a service'''
    return json.loads(json_data)

