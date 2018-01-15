from connectors import apicem
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import os

def main(parameters):
    '''
    Gets information about the status of the APIC-EM controller and about the network devices
    Returns the result as a picture in Spark
    '''

    text = ''
    apic_health = 100
    reachability_health = 100
    status = 'APIC-EM Online'

    nw_devices = apicem.get_network_device()
    ok_count = 0
    for device in nw_devices:
        if device['reachabilityStatus'] == 'Reachable':
            ok_count += 1

    if ok_count == len(nw_devices):
        device_reachability = 'All devices are reachable!'
    else:
        reachability_health = 100 * ok_count/len(nw_devices)
        device_reachability = str(ok_count) + '/' + str(len(nw_devices)) + ' devices reachable'

    main_dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
    font_path = os.path.join(main_dir, 'resources', 'CiscoSansTTExtraLight.ttf')
    picture_path = os.path.join(main_dir, 'resources', 'status_template.png')

    img = Image.open(picture_path)
    draw = ImageDraw.Draw(img)

    normal_font = ImageFont.truetype(font_path, 56)

    #DRAW APIC-EM and devices logos
    img.paste(Image.open(os.path.join(main_dir, 'resources', 'apicem_logo.png'), 'r'), (100, 100))
    img.paste(Image.open(os.path.join(main_dir, 'resources', 'devices_logo.png'), 'r'), (1070, 160))

    #DRAW APIC-EM health
    if apic_health == 100:
        img.paste(Image.open(os.path.join(main_dir, 'resources', 'green_status.png'), 'r'), (580, 60))
    elif apic_health > 70:
        img.paste(Image.open(os.path.join(main_dir, 'resources', 'yellow_status.png'), 'r'), (580, 60))
    else:
        img.paste(Image.open(os.path.join(main_dir, 'resources', 'red_status.png'), 'r'), (580, 60))

    #DRAW Device health
    if reachability_health == 100:
        img.paste(Image.open(os.path.join(main_dir, 'resources', 'green_status.png'), 'r'), (1600, 60))
    elif reachability_health > 70:
        img.paste(Image.open(os.path.join(main_dir, 'resources', 'yellow_status.png'), 'r'), (1600, 60))
    else:
        img.paste(Image.open(os.path.join(main_dir, 'resources', 'red_status.png'), 'r'), (1600, 60))

    # Alignment of text on the picture (first = left/right; second = up/down)
    draw.multiline_text((45, 420), status, (0, 0, 0), font=normal_font, align="center")
    draw.multiline_text((1045, 420), device_reachability, (0, 0, 0), font=normal_font, align="center")

    img.save('apicem_status.png')

    send_image = open('apicem_status.png', 'rb')

    answer = {
        'text': text,
        'markdown': text,
        'file': send_image
    }

    return answer