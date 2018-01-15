from connectors import apicem

def main(parameters):
    '''
    Gets the temperature of a specified device
    NOTE: not implemented yet
    '''


    nw_devices = apicem.get_network_device()

    all_devices = []
    for device in nw_devices:
        all_devices.append(device['id'])

    cli = apicem.post_cli_request('root', ['show version'], all_devices, 'test')
    print cli

    answer = {
        'text': 'This feature is not yet implemented.',
        'markdown': 'This feature is not yet implemented.',
        'file': None
    }

    return answer