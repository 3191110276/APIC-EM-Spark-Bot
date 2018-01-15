from connectors import apicem
from collections import Counter
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import os
import re

def main(parameters):
    '''Returns a list of 'free' ports - using ports that are currently not up in APIC-EM'''

    location_req = parameters['location']
    role_req = parameters['type']

    output_structure = {}

    all_locations = apicem.get_location()

    location_available = False

    if len(all_locations) > 0:
        for location in all_locations:
            if location_req == location['locationName']:
                location_available = True
    else:
        if location_req != 'Any' and location_req != 'any':
            answer = {
                'text': 'No locations have been defined! Please either define a location in the controller, or use \"Any\" for the location.',
                'markdown': 'No locations have been defined! Please either define a location in the controller, or use \"Any\" for the location.',
                'file': None
            }
            return answer

    if location_available == False:
        if location_req != 'Any' and location_req != 'any':
            answer = {
                'text': 'No locations with this name has been defined! Please either define a location in the controller, or use \"Any\" for the location.',
                'markdown': 'No locations with this name has been defined! Please either define a location in the controller, or use \"Any\" for the location.',
                'file': None
            }
            return answer

    nw_devices = apicem.get_network_device()
    for device in nw_devices:
        output_structure[device['id']] = {
            'series': device['series'],
            'lineCardCount': device['lineCardCount'],
            'interfaceCount': device['interfaceCount'],
            'family': device['family'],
            'hostname': device['hostname'],
            'roleSource': device['roleSource'],
            'platformId': device['platformId'],
            'role': device['role'],
            'location': device['location'],
            'type': device['type'],
            'lineCardId': device['lineCardId'],
            'locationName': device['locationName'],
            'available_ports': 0,
            'port_list': [],
            'port_type_count': None
        }

    #Add ports to the devices
    ports = apicem.get_interface()
    for port in ports:
        if port['status'] != 'up' and port['interfaceType'] == 'Physical':
            output_structure[port['deviceId']]['available_ports'] += 1
            output_structure[port['deviceId']]['port_list'].append(port['portName'])

    #Remove devices that do not have available ports
    for k in output_structure.keys():
        if output_structure[k]['available_ports'] == 0:
            del output_structure[k]

    #Remove devices that do not fit the role requirement
    for k in output_structure.keys():
        if output_structure[k]['role'] != role_req:
            del output_structure[k]

    #Remove devices that do not fit the location requirement
    if location_req != 'Any' and location_req != 'any':
        for k in output_structure.keys():
            if output_structure[k]['locationName'] != location_req:
                del output_structure[k]

    for device in output_structure:
        portslist = []
        for port in output_structure[device]['port_list']:
            m = re.search("\d", port)
            if m:
                portslist.append(port[:m.start()])

        output_structure[device]['port_type_count'] = Counter(portslist)

    main_dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
    font_path = os.path.join(main_dir, 'resources', 'CiscoSansTTExtraLight.ttf')
    switch_pic_path = os.path.join(main_dir, 'resources', 'switch_ports.png')
    router_pic_path = os.path.join(main_dir, 'resources', 'router_ports.png')
    small_font = ImageFont.truetype(font_path, 45)
    normal_font = ImageFont.truetype(font_path, 50)
    large_font = ImageFont.truetype(font_path, 115)

    increment = 0
    for device in output_structure:
        if output_structure[device]['role'] == 'BORDER ROUTER':
            img = Image.open(router_pic_path)
        else:
            img = Image.open(switch_pic_path)

        draw = ImageDraw.Draw(img)

        ports_overview = []
        for ptype in output_structure[device]['port_type_count']:
            ports_overview.append(ptype + ': ' + str(output_structure[device]['port_type_count'][ptype]))

        device_name = output_structure[device]['series']
        if device_name[-8:] == 'Switches':
            device_name = device_name[:-8]

        draw.multiline_text((265, 40), str(output_structure[device]['available_ports']), (0, 0, 0), font=large_font, align="left")
        draw.multiline_text((38, 200), device_name, (0, 0, 0), font=normal_font, align="left")
        for i in range(len(ports_overview)):
            draw.multiline_text((680, 25+50*i), ports_overview[i], (0, 0, 0), font=small_font, align="left")

        img.save('port_counts_part' + str(increment) + '.png')
        increment += 1

    if output_structure == {}:
        text = 'I could not find a device that fits your requirements.'
        answer = {
            'text': text,
            'markdown': text,
            'file': None
        }
    else:
        #Image stitching
        img_height = 297 * increment
        background_image = Image.new('RGB', (1289, img_height))
        for i in range(increment):
            background_image.paste(Image.open('port_counts_part' + str(i) + '.png'), (0, 297*i))
            background_image.save('port_counts.png')

        send_image = open('port_counts.png', 'rb')
        text = 'Please check manually on the device to verify that nothing is plugged into the ports'

        answer = {
            'text': text,
            'markdown': text,
            'file': send_image
        }

    return answer