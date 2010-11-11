
import sys
try:
    import json
except:
    import simplejson as json
import httplib


'''

jindolib.py
==========

Desc: Library for (mt) Media Temple's API


Author: Rob Cakebread <cakebread a t gmail d0t c0m>

License  : GNU General Public License Version 2

'''

__docformat__ = 'restructuredtext'


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


def print_service_details(json_data):
    '''Print details of a service'''
    #print json_data
    #json_data = json.loads(json_data)
    for key in SERVICE_KEYS:
        if key == 'ipAddresses':
            print key + ":"
            for ip in json_data['service']['ipAddresses']:
                print "    " + ip
        elif key == 'addons':
            print key + ":"
            for addon in json_data['service']['addons']:
                print "    " + addon['description']

        elif key == 'billingStatus' or key == 'serviceType' or key == 'operatingSystem':
            pass
        else:
            print key + ":", json_data['service'][key]

def fetch_service_details(service, api_key, debug=False):
    '''Returns '''
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

def parse_service(json_data):
    '''Parses a service'''
    return json.loads(json_data)

def parse_json(result):
    '''Simply loads a string into JSON'''
    return json.loads(result)

