from flask import Flask, request
from flask_basicauth import BasicAuth
from werkzeug.wrappers import Response
from intents import controller
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json
import os

# Configuration information for the application
app = Flask(__name__)
#app.debug = True

app.config['BASIC_AUTH_USERNAME'] = 'cisconlp'
app.config['BASIC_AUTH_PASSWORD'] = 'thisisanamazingpasswordfortheserverthatwehave52394023409u-,,-,-.-'

basic_auth = BasicAuth(app)

# Listen for events
@app.route("/", methods=["POST"])
@basic_auth.required
def listen():
    '''Main route that receives all requests from API.AI/Spark for processing'''

    received = json.loads(request.data)

    resp_item = controller.fetch_response(
        sessionId=received['sessionId'],
        parameters=received['result']['parameters'],
        contexts=received['result']['contexts'],
        resolvedQuery=received['result']['resolvedQuery'],
        intentId=received['result']['metadata']['intentId'],
        intentName=received['result']['metadata']['intentName']
    )

    resp_text = resp_item['text']
    resp_markdown = resp_item['markdown']
    file = resp_item['file']

    if file == None:
        post = {
            "toPersonId": None,
            "roomId": None,
            "text": resp_text,
            "markdown": resp_markdown,
        }
    else:
        post = {
            "toPersonId": None,
            "roomId": None,
            "text": resp_text,
            "markdown": resp_markdown,
            "files": ('My Result', file, 'image/jpg')
        }

    #Checks if the communication was with a single user or with a room
    if received['originalRequest']['data']['data']['roomType'] == 'direct':
        post['toPersonId'] = received['originalRequest']['data']['data']['personId']
        del post['roomId']
    else:
        post['roomId'] = received['originalRequest']['data']['data']['roomId']
        del post['toPersonId']

    m = MultipartEncoder(post)

    headers = {
        'content-type': m.content_type,
        'authorization': 'Bearer YWYzNDVkY2MtMDg5MC00MjRlLTk2MzYtMzFkZjllYTBjODBiYWFlYTc2OTItYmM3'
    }

    requests.post('https://api.ciscospark.com/v1/messages', headers=headers, verify=False, data=m).json()

    resp = Response(json.dumps({
        'speech': '',
        'displayText': ''
    }))
    resp.headers['Content-Type'] = 'application/json'

    return resp


if __name__ == '__main__':
    app.run(port=5000)