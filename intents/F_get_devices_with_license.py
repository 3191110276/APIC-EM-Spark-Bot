from connectors import apicem
import concurrent.futures

def main(parameters):
    '''Returns a list of all devices that have a certain license'''

    devices = apicem.get_network_device_with_license(parameters['licensename'])

    if 'errorCode' in devices:
        if devices['detail'] == 'License file name does not exists':
            nw_devices = apicem.get_network_device()
            license_names = []

            pool = concurrent.futures.ThreadPoolExecutor(max_workers=40)
            futures = [pool.submit(apicem.get_licenseinfo_for_network_device, devid['id']) for devid in nw_devices]
            results = [r.result() for r in concurrent.futures.as_completed(futures)]

            for devlic in results:
                if devlic != None:
                    for lic in devlic:
                        license_names.append(lic['name'])

            license_names = list(set(license_names))
            if len(license_names) > 0:
                text = 'This is not a valid name for a license on any of your devices. Please ask again with a valid license. Currently, the following licenses are available on devices in your network:\n'

                for x in license_names:
                    text += '- ' + x + '\n'
            else:
                text = 'None of your devices have any licenses registered on them .'

            return text

    text = 'There are ' + str(len(devices)) + ' devices with this license:\n'

    pool = concurrent.futures.ThreadPoolExecutor(max_workers=40)
    futures = [pool.submit(apicem.get_network_device_by_id, id) for id in devices]
    results = [r.result() for r in concurrent.futures.as_completed(futures)]

    for i in results:
        text += '- ' + i['hostname'] + ' (' + i['id'] + ')\n'

    answer = {
        'text': text,
        'markdown': text,
        'file': None
    }

    return answer