from connectors import apicem

def main(parameters):
    '''Shows what problems are present for network devices - categorizes NW devices by problem in the output'''

    devices = apicem.get_network_device()

    errors = {}

    for i in devices:
        if i['collectionStatus'] != 'Managed':
            if i['collectionStatus'] == 'In Progress':
                if 'In Progress' not in errors:
                    errors['In Progress'] = {
                        'devices': [],
                        'count': 0
                    }
                errors['In Progress']['devices'].append('- ' + i['hostname'] + ' (' + i['platformId'] + ')')
                errors['In Progress']['count'] += 1
            else:
                if i['errorCode'] not in errors:
                    errors[i['errorCode']] = {
                        'devices': [],
                        'count': 0
                    }
                errors[i['errorCode']]['devices'].append('- ' + i['hostname'] + ' (' + i['platformId'] + ')')
                errors[i['errorCode']]['count'] += 1

    for e in errors:
        if e == 'DEV-UNREACHED':
            errors['Device unreachable: SNMP Timeouts are occurring with these devices'] = errors.pop(e)

    text = 'I found the following problems with your network devices:\n\n'
    for e in errors:
        text += str(e) + ' (' + str(errors[e]['count']) + ')\n'
        for dev in errors[e]['devices']:
            text += dev + '\n'
        text += '\n\n'

    answer = {
        'text': text,
        'markdown': text,
        'file': None
    }

    return answer