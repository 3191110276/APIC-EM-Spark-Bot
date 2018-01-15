from connectors import apicem

def main(parameters):
    '''
    Gets the configuration of a specific device
    NOTE: not implemented yet
    '''

    devices = apicem.get_network_device()
    apicem.get_config("8dbd8068-1091-4cde-8cf5-d1b58dc5c9c7")

    output_text = apicem.get_config("8dbd8068-1091-4cde-8cf5-d1b58dc5c9c7")
    split_output = output_text.split('\n')

    while split_output[0] == '' or split_output[0] == 'Building configuration...':
        split_output.pop(0)

    text = '```'
    for item in split_output:
        text += item + '\n'
    text += '```'

    answer = {
        'text': text,
        'markdown': text,
        'file': None
    }

    return answer