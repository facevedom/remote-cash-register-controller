import requests
from flask import Flask
from flask import request
import os
import motor_controller

import threading

# app-server
app = Flask(__name__)
# url-app-slack 
URL = os.getenv('SLACK_URL')

# endpoint for process request from slack
@app.route('/slack', methods=['POST'])
def login():
    text = request.form.get('text')
    username = request.form.get('user_name')
    payload = '{"text":"'+ username + ' is closing the cash register"}'
    head = {"Content-type": "application/json"} 
    r = requests.post(url=URL, data=payload, headers=head)

    t = threading.Thread(target=motor_controller.rotate)
    t.start()

    return username + ' We are processing your request, please wait...', 200
        
app.run(debug=True)
