from connectors import apicem
import re
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from pathlib2 import Path
import os


def main(parameters):
    '''Gets the network device to which a user is connected and returns it as a picture'''

    connection = {
        'hostIP': None,
        'hostMac': None,
        'conn_type': None,
        'ap_name': None,
        'ap_series': None,
        'ap_family': None,
        'ap_ssid': None,
        'switch_name': None,
        'switch_series': None,
        'switch_family': None,
        'switch_port': None
    }

    text = ''

    hostMac = parameters['hostInfo'].replace('-',':').replace(' ',':')
    if re.match("[0-9a-f]{2}([:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", hostMac.lower()):
        host_information = apicem.get_host(hostMac=hostMac)
        nw_information = apicem.get_network_device_by_id(host_information[0]['connectedNetworkDeviceId'])

        connection['hostIP'] = host_information[0]['hostIp']
        connection['hostMac'] = host_information[0]['hostMac']
        connection['conn_type'] = host_information[0]['hostType']
        connection['series'] = nw_information['series'][:-1]
        connection['family'] = nw_information['family']
        connection['mgmt_ip'] = nw_information['managementIpAddress']
        connection['mac_adr'] = nw_information['macAddress']
        connection['dev_id'] = nw_information['id']

    elif re.match("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$", parameters['hostInfo']):
        host_information = apicem.get_host(hostIp=parameters['hostInfo'])
        nw_information = apicem.get_network_device_by_id(host_information[0]['connectedNetworkDeviceId'])

        connection['hostIP'] = host_information[0]['hostIp']
        connection['hostMac'] = host_information[0]['hostMac']
        connection['conn_type'] = host_information[0]['hostType']
        connection['series'] = nw_information['series'][:-1]
        connection['family'] = nw_information['family']
        connection['mgmt_ip'] = nw_information['managementIpAddress']
        connection['mac_adr'] = nw_information['macAddress']
        connection['dev_id'] = nw_information['id']

    else:
        text = 'Sorry, I do not understand usernames. Please provide either an IP or a MAC address for the device you are looking for.'
        #TODO: allow search based on username

    main_dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
    font_path = os.path.join(main_dir, 'resources', 'CiscoSansTTExtraLight.ttf')

    if connection['conn_type'] == 'wireless':
        picture_path = os.path.join(main_dir, 'resources', 'device_to_AP_connection.png')
    else:
        picture_path = os.path.join(main_dir, 'resources', 'device_to_Switch_connection.png')

    img = Image.open(picture_path)
    draw = ImageDraw.Draw(img)

    normal_font = ImageFont.truetype(font_path, 60)

    # Alignment of text on the picture (first = left/right; second = up/down)
    host_data = connection['hostIP'] + '\n' + connection['hostMac']
    draw.multiline_text((120, 200), host_data, (0, 0, 0), font=normal_font, align="right") #Host IP + MAC

    nw_data = connection['series'] + '\n' + connection['mgmt_ip'] + '\n' + connection['mac_adr']
    draw.multiline_text((1600, 150), nw_data, (0, 0, 0), font=normal_font, align="left") # NW-Device Series + Mgmt-IP + MAC

    img.save('device_connection.png')

    send_image = open('device_connection.png', 'rb')

    answer = {
        'text': text,
        'markdown': text,
        'file': send_image
    }

    return answer