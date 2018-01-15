def main(parameters):
    '''Returns a text response about things the bot can do'''

    my_capabilities = 'Hi, I can help you with the following tasks:\n'
    my_capabilities += '- ' + 'Checking of the network status (for example: "What is my network status?")\n'
    my_capabilities += '- ' + 'Find out errors with the network devices. (for example: "What is wrong with my network devices?")\n'
    my_capabilities += '- ' + 'Finding of host connections based on IP or MAC (for example: "Where is **10.1.15.117** connected?")\n'
    my_capabilities += '- ' + 'Helping with the expansion of the network (for example: "I want to expand my network")\n'
    my_capabilities += '- ' + 'Get a list of network devices (for example: "What are my network devices?")\n'

    answer = {
        'text': my_capabilities,
        'markdown': my_capabilities,
        'file': None
    }

    return answer



