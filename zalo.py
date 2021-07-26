<<<<<<< HEAD
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    user_id = request.args.get('user_id')
    user_message = request.args.get('user_message')
    url = "http://127.0.0.1:5005/webhooks/rest/webhook"
    data_dict = {
        "sender": user_id, "message": user_message}
    data = json.dumps(data_dict)
    headers = {'Content-type': 'application/json',
               'Accept': 'text/plain'}
    try:
        _r_bot = requests.post(url, data, headers)
        _respone_bot = json.loads(_r_bot.text)
        # print(_respone_bot)
        return (_respone_bot[0])
    except ConnectionError:
        print("Cannot connect to bot")


if __name__=="__main__":
=======
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    user_id = request.args.get('user_id')
    user_message = request.args.get('user_message')
    url = "http://127.0.0.1:5005/webhooks/rest/webhook"
    data_dict = {
        "sender": user_id, "message": user_message}
    data = json.dumps(data_dict)
    headers = {'Content-type': 'application/json',
               'Accept': 'text/plain'}
    try:
        _r_bot = requests.post(url, data, headers)
        _respone_bot = json.loads(_r_bot.text)
        # print(_respone_bot)
        return (_respone_bot[0])
    except ConnectionError:
        print("Cannot connect to bot")


if __name__=="__main__":
>>>>>>> 1b566f8a99bbd5d5cbafe6eee9141182ff558efb
    app.run(port=8088, debug=True)