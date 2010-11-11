
from jindo.jindolib import parse_service

response = '''{"services":[{"id":345319,"serviceType":396,"serviceTypeName":"(gs) Grid Service","ipAddresses":["72.47.230.175"],"hostServer":null,"billingStatus":"0","billingStatusText":"OPEN","operatingSystem":null,"operatingSystemName":null,"accessDomain":"s67022.gridserver.com","primaryDomain":"cakebread.homelinux.org","addons":[{"id":565,"description":"(gs) Django Container 128M - Beta"},{"id":434,"description":"(gs) Rails Container Lite - Free"}]},{"id":345843,"serviceType":525,"serviceTypeName":"(dv) Dedicated-Virtual Base 3","ipAddresses":["70.32.78.91"],"hostServer":"vz307.mediatemple.net","billingStatus":"0","billingStatusText":"OPEN","operatingSystem":"1001","operatingSystemName":"Centos 4","accessDomain":null,"primaryDomain":"polopop.com","addons":[{"id":221,"description":"(dv) Linux Plesk Basic 30"}]},{"id":345845,"serviceType":605,"serviceTypeName":"(dv) Dedicated-Virtual Base 3.5","ipAddresses":["70.32.107.244"],"hostServer":"vz406.mediatemple.net","billingStatus":"0","billingStatusText":"OPEN","operatingSystem":"1002","operatingSystemName":"Centos 5","accessDomain":null,"primaryDomain":"cakebread.info","addons":[{"id":221,"description":"(dv) Linux Plesk Basic 30"}]},{"id":427401,"serviceType":669,"serviceTypeName":"(ve) Server 1GB","ipAddresses":["70.32.111.178"],"hostServer":"vzd007.mediatemple.net","billingStatus":"0","billingStatusText":"OPEN","operatingSystem":"16","operatingSystemName":"Ubuntu 9.10 Karmic","accessDomain":"ve.svfdbcfc.vesrv.com","primaryDomain":"ve.cakebread.info","addons":[{"id":719,"description":"(ve) Snapshot Backups"}]}]}'''

SERVER_RESP = '''{
    "service": {
        "accessDomain": "ve.svfdbcfc.vesrv.com", 
        "addons": [
            {
                "description": "(ve) Snapshot Backups", 
                "id": 719
            }
        ], 
        "billingStatus": "0", 
        "billingStatusText": "OPEN", 
        "hostServer": "vzd007.mediatemple.net", 
        "id": 427401, 
        "ipAddresses": [
            "70.32.111.178"
        ], 
        "operatingSystem": "16", 
        "operatingSystemName": "Ubuntu 9.10 Karmic", 
        "primaryDomain": "ve.cakebread.info", 
        "serviceType": 669, 
        "serviceTypeName": "(ve) Server 1GB"
    }
}'''

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

def test_get_service_detail():
    json_data = parse_service(SERVER_RESP)
    assert json_data['service']['accessDomain'] == "ve.svfdbcfc.vesrv.com"

    #API broken, should be integer:
    assert json_data['service']['billingStatus'] == "0"
    assert json_data['service']['addons'] == [ { "description": "(ve) Snapshot Backups", "id": 719 } ]
    assert json_data['service']['addons'][0]["description"]  == "(ve) Snapshot Backups"
    assert json_data['service']['addons'][0]["id"]  == 719
    assert json_data['service']['primaryDomain'] == "ve.cakebread.info"
    assert json_data['service']['billingStatusText'] == "OPEN"
    assert json_data['service']['hostServer'] == "vzd007.mediatemple.net"
    assert json_data['service']['ipAddresses'] == ["70.32.111.178"]
    #API broken, should be integer:
    assert json_data['service']['operatingSystem'] == "16"
    assert json_data['service']['operatingSystemName'] == "Ubuntu 9.10 Karmic"
    assert json_data['service']['serviceType'] == 669
    assert json_data['service']['serviceTypeName'] == "(ve) Server 1GB"
    for key in SERVICE_KEYS:
        assert json_data['service'].has_key(key)
