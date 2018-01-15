import time
from tinydb import TinyDB, Query
import requests
import json

db = TinyDB('apicem.json')

#https://fra-apicem1.cisco.com/
#USER = "demo1"
#PASSWORD = "Cisco123"
#URL = "https://fra-apicem1.cisco.com/api/v1"

#https://fra-apicem3.cisco.com/
#USER = "demo1"
#PASSWORD = "Cisco123"
#URL = "https://fra-apicem3.cisco.com/api/v1"

#DEVNET-APICEM
USER = "devnetuser"
PASSWORD = "Cisco123!"
URL = "https://devnetapi.cisco.com/sandbox/apic_em/api/v1"

CURRENT_TIME = time.time()
CACHE_TIMER = 60*60*24 # 60s x 60m x 24h


def cache_available(name, variables):
    '''Returns true if the requested value is already cached, or False if the value is not cached or timed out'''
    q = Query()
    query = db.search(q['name'] == name)

    result = {}

    if query == []:
        result['status'] = False
        result['value'] = {}
        return result

    if query[0]['timeout'] < CURRENT_TIME:
        result['status'] = False
        result['value'] = query[0]['value']
        db.remove(q.name == name)
        return result

    result['status'] = True
    result['value'] = query[0]['value']
    return result


def get_ticket():
    '''
    Requests a ticket from APIC-EM based on the username and password
    The ticket will be used for all further requests
    '''
    headers = {
        "content-type": "application/json"
    }

    content = {
        "username": USER,
        "password": PASSWORD
    }

    q = Query()
    if db.search(q['name'] == 'ticket') == []:
        new_ticket = requests.post(URL + "/ticket", headers=headers, verify=False, data=json.dumps(content)).json()['response']
        db.insert({'name': 'ticket', 'value': {
            'serviceTicket': new_ticket['serviceTicket'],
            'timeout': CURRENT_TIME + new_ticket['idleTimeout'] -60
        }})
    elif db.search(q['name'] == 'ticket')[0]['value']['timeout'] < CURRENT_TIME:
        new_ticket = requests.post(URL + "/ticket", headers=headers, verify=False, data=json.dumps(content)).json()['response']
        db.update({'name': 'ticket', 'value': {
            'serviceTicket': new_ticket['serviceTicket'],
            'timeout': CURRENT_TIME + new_ticket['idleTimeout'] -60
        }},q['name'] == 'ticket')

    return db.search(q['name'] == 'ticket')[0]['value']['serviceTicket']


#----------------------------------------------------------------------------------------------------------------------
# [GET] /host
#----------------------------------------------------------------------------------------------------------------------
def get_host(limit=None,offset=None,sortBy=None,order=None,hostName=None,hostMac=None,hostType=None,connectedInterfaceName=None,hostIp=None,connectedNetworkDeviceIpAddress=None,subtype=None,filterOperation=None):
    '''Gets all available hosts - attributes can be used for filtering the list of hosts'''

    headers = {
        "X-Auth-Token": get_ticket()
    }

    search = {
        'limit': limit,
        'offset': offset,
        'sortBy': sortBy,
        'order': order,
        'hostName': hostName,
        'hostMac': hostMac,
        'hostType': hostType,
        'connectedInterfaceName': connectedInterfaceName,
        'hostIp': hostIp,
        'connectedNetworkDeviceIpAddress': connectedNetworkDeviceIpAddress,
        'subtype': subtype,
        'filterOperation': filterOperation
    }

    for i in search.keys():
        if search[i] == None:
            del search[i]

    cache = cache_available('get_host', search)
    if cache['status'] == True:
        host = cache['value']
    else:

        host = requests.get(URL + "/host", headers=headers, params=search, verify=False).json()['response']
        db.insert({
            'name': 'get_host',
            'variables': search,
            'timeout': CURRENT_TIME + CACHE_TIMER,
            'value': host
        })

    return host


#----------------------------------------------------------------------------------------------------------------------
# [GET] /interface
#----------------------------------------------------------------------------------------------------------------------
def get_interface():
    '''Gets a list of all interfaces'''

    headers = {
        "X-Auth-Token": get_ticket()
    }

    cache = cache_available('get_interface', {})
    if cache['status'] == True:
        interfaces = cache['value']
    else:
        interfaces = requests.get(URL + "/interface", headers=headers, verify=False).json()['response']
        db.insert({
            'name': 'get_interface',
            'variables': {},
            'timeout': CURRENT_TIME + CACHE_TIMER,
            'value': interfaces
        })

    return interfaces

#----------------------------------------------------------------------------------------------------------------------
# [GET] /location
#----------------------------------------------------------------------------------------------------------------------
def get_location():
    '''Gets a list of all locations'''

    headers = {
        "X-Auth-Token": get_ticket()
    }

    cache = cache_available('get_location', {})
    if cache['status'] == True:
        locations = cache['value']
    else:
        locations = requests.get(URL + "/location", headers=headers, verify=False).json()['response']
        db.insert({
            'name': 'get_location',
            'variables': {},
            'timeout': CURRENT_TIME + CACHE_TIMER,
            'value': locations
        })

    return locations

#----------------------------------------------------------------------------------------------------------------------
# [GET] /license-info/network-device/{deviceId}
#----------------------------------------------------------------------------------------------------------------------
def get_licenseinfo_for_network_device(device_id):
    '''Gets the licenses for a specified device'''

    headers = {
        "X-Auth-Token": get_ticket()
    }

    return requests.get(URL + "/license-info/network-device/" + device_id, headers=headers, verify=False).json()['response']


#----------------------------------------------------------------------------------------------------------------------
# [GET] /network-device/license/{licenseFileName}
#----------------------------------------------------------------------------------------------------------------------
def get_network_device_with_license(license_name):
    '''Gets all network devices that have a certain license'''

    headers = {
        "X-Auth-Token": get_ticket()
    }

    return requests.get(URL + "/network-device/license/" + license_name, headers=headers, verify=False).json()['response']


#----------------------------------------------------------------------------------------------------------------------
# [GET] /network-device
#----------------------------------------------------------------------------------------------------------------------
def get_network_device():
    '''Gets all network devices'''

    headers = {
        "X-Auth-Token": get_ticket()
    }

    cache = cache_available('get_network_device', {})
    if cache['status'] == True:
        network_devices = cache['value']
    else:
        network_devices = requests.get(URL + "/network-device", headers=headers, verify=False).json()['response']
        db.insert({
            'name': 'get_network_device',
            'variables': {},
            'timeout': CURRENT_TIME + CACHE_TIMER,
            'value': network_devices
        })

    return network_devices


#----------------------------------------------------------------------------------------------------------------------
# [GET] /network-device/{Location}
#----------------------------------------------------------------------------------------------------------------------
def get_network_device_by_location(location):
    '''Gets all network devices at a certain location'''

    headers = {
        "X-Auth-Token": get_ticket()
    }

    return requests.get(URL + "/location/" + location, headers=headers, verify=False).json()['response']


#----------------------------------------------------------------------------------------------------------------------
# [GET] /network-device/{DeviceId}
#----------------------------------------------------------------------------------------------------------------------
def get_network_device_by_id(id):
    '''Gets a specific network devices based on its ID'''

    headers = {
        "X-Auth-Token": get_ticket()
    }

    cache = cache_available('get_network_device_by_id', {'deviceid': id})
    if cache['status'] == True:
        nw_device = cache['value']
    else:
        nw_device = requests.get(URL + "/network-device/" + id, headers=headers, verify=False).json()['response']
        db.insert({
            'name': 'get_network_device_by_id',
            'variables': {'deviceid': id},
            'timeout': CURRENT_TIME + CACHE_TIMER,
            'value': nw_device
        })

    return nw_device

#----------------------------------------------------------------------------------------------------------------------
# [POST] /network-device-poller/cli/read-request
#----------------------------------------------------------------------------------------------------------------------
def post_cli_request(user, commands, deviceUuids, name, timeout=0, description=""):
    '''Sends a CLI command for a specific device'''

    headers = {
        "X-Auth-Token": get_ticket()
    }

    data = json.dumps({
        "username": user,
        "body": {
            "commands": commands,
            "deviceUuids": deviceUuids,
            "name": name,
            "timeout": timeout,
            "description": description
        }
    })

    return requests.post(URL + '/network-device-poller/cli/read-request/', data, headers=headers)

#----------------------------------------------------------------------------------------------------------------------
# [GET] /network-device/{DeviceId}/config
#----------------------------------------------------------------------------------------------------------------------
def get_config(id):
    '''Gets the configuration of a specific device based on its ID'''

    headers = {
        "X-Auth-Token": get_ticket()
    }

    return requests.get(URL + "/network-device/" + id +"/config", headers=headers, verify=False).json()['response']