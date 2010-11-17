
from jindo.jindolib import parse_service


SERVER_RESP = '''{
    "service": {
        "accessDomain": "ve.svfdbcfc.vesrv.com",
        "addons": [
            {
                "description": "(ve) Snapshot Backups",
                "id": 719
            }
        ],
        "billingStatus": 0,
        "billingStatusText": "OPEN",
        "hostServer": "vzd007.mediatemple.net",
        "id": 427401,
        "ipAddresses": [
            "70.32.111.178"
        ],
        "operatingSystem": 16,
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

    assert json_data['service']['billingStatus'] == 0
    assert json_data['service']['addons'] == [ { "description": "(ve) Snapshot Backups", "id": 719 } ]
    assert json_data['service']['addons'][0]["description"]  == "(ve) Snapshot Backups"
    assert json_data['service']['addons'][0]["id"]  == 719
    assert json_data['service']['primaryDomain'] == "ve.cakebread.info"
    assert json_data['service']['billingStatusText'] == "OPEN"
    assert json_data['service']['hostServer'] == "vzd007.mediatemple.net"
    assert json_data['service']['ipAddresses'] == ["70.32.111.178"]
    assert json_data['service']['operatingSystem'] == 16
    assert json_data['service']['operatingSystemName'] == "Ubuntu 9.10 Karmic"
    assert json_data['service']['serviceType'] == 669
    assert json_data['service']['serviceTypeName'] == "(ve) Server 1GB"
    for key in SERVICE_KEYS:
        assert json_data['service'].has_key(key)
