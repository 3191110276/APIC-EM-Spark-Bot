import sys

def fetch_response(sessionId,parameters,contexts,resolvedQuery,intentId,intentName):
    '''
    Maps the incoming request to a function based on the name of the intent
    Calls the corresponding function once it has been determined
    '''

    method_to_call = getattr(sys.modules[__name__], intentName.replace(" ", "_").lower())
    return method_to_call(parameters=parameters)


import F_get_available_ports
def get_available_ports(parameters=None):
    return F_get_available_ports.main(parameters)

import F_get_bot_capabilities
def get_bot_capabilities(parameters=None):
    return F_get_bot_capabilities.main(parameters)

import F_get_connection_status
def get_connection_status(parameters=None):
    return F_get_connection_status.main(parameters)

import F_get_device_licenses
def get_device_licenses(parameters=None):
    return F_get_device_licenses.main(parameters)

import F_get_device_temperature
def get_device_temperature(parameters=None):
    return F_get_device_temperature.main(parameters)

import F_get_devices_with_license
def get_devices_with_license(parameters=None):
    return F_get_devices_with_license.main(parameters)

import F_get_network_device_for_user
def get_network_device_for_user(parameters=None):
    return F_get_network_device_for_user.main(parameters)

import F_get_network_device_problems
def get_network_device_problems(parameters=None):
    return F_get_network_device_problems.main(parameters)

import F_get_network_devices
def get_network_devices(parameters=None):
    return F_get_network_devices.main(parameters)

import F_get_network_status
def get_network_status(parameters=None):
    return F_get_network_status.main(parameters)

import F_get_users_at_location
def get_users_at_location(parameters=None):
    return F_get_users_at_location.main(parameters)

import F_get_configuration
def get_configuration(parameters=None):
    return F_get_configuration.main(parameters)