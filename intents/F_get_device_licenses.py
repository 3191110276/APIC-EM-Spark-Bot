from connectors import apicem
import concurrent.futures

def main(parameters):
    '''Gets the licenses for our network devices'''

    text = 'Right now, I found these licenses:\n'

    devices = apicem.get_network_device()

    pool = concurrent.futures.ThreadPoolExecutor(max_workers=40)
    futures = [pool.submit(apicem.get_licenseinfo_for_network_device, devid['id']) for devid in devices]
    results = [r.result() for r in concurrent.futures.as_completed(futures)]

    for x in range(len(results)):
        if results[x] != None:
            licenses = []
            for lic in results[x]:
                if lic['status'] in parameters['LicenseStatus'] or parameters['LicenseStatus'] == '':
                    licenses.append(lic['name'])
            if licenses != []:
                text += '- ' + devices[x]['hostname'] + ' (' + devices[x]['id'] + '): ' + ','.join(licenses) + '\n'

    if text == 'Right now, I found these licenses:\n':
        text = 'Right now, no devices have licenses.'

    answer = {
        'text': text,
        'markdown': text,
        'file': None
    }

    return answer