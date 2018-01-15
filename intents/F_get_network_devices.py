from connectors import apicem

def main(parameters):
    '''Gets a list of all network devices'''

    devices = apicem.get_network_device()

    device_filter = []
    for i in parameters['NetworkDevice']:
            device_filter.append(i)

    text = ''
    for i in devices:
        if i['family'] in device_filter or device_filter == []:
            text += '- ' + i['hostname'] + ' (' + i['platformId'] + ')\n'

    answer = {
        'text': text,
        'markdown': text,
        'file': None
    }

    return answer