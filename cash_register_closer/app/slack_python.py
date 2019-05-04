import sqlite3
import requests
from flask import Flask
from flask import request
from flask import Response
import os
import json
import threading

conn = sqlite3.connect('./app/cash_register.db')
c = conn.cursor()
# c.execute('''CREATE TABLE reservation
#              (user text, date text, initialHour int, initialMinute int, finishHour int, finishMinute int)''')

# # # Insert a row of data
# c.execute("INSERT INTO reservation VALUES ('jgmejias' ,'2006-01-05',2,4)")
# t = (2,2)
# c.execute('SELECT * FROM reservation WHERE initialHour < ? and finishHour > ?', t)
# reservation = c.fetchone()
# print(reservation)
# if reservation:
#     print(reservation[0])
#     print(reservation[2])
#     print(reservation[3])
# # Save (commit) the changes
# conn.commit()

# # We can also close the connection if we are done with it.
# # Just be sure any changes have been committed or they will be lost.
# conn.close()


URL = os.getenv('SLACK_URL')
app = Flask(__name__)

# endpoint for process request from slack

def work():
    return 'work', 200

def close_register():
    text = request.form.get('text')
    print(request.form)
    username = request.form.get('user_id')
    payload = '{"text":" <@'+ username + '> is closing the cash register"}'

    head = {"Content-type": "application/json"} 
    r = requests.post(url=URL, data=payload, headers=head)
    # t = threading.Thread(target=motor_controller.rotate)
    # t.start()

    return 'we are processing your request', 200

def processRequest(text):
    print(text.split(' '))
    # c.execute('SELECT * FROM reservation WHERE initialHour < ? and finishHour > ?', t)
    payload = '{"text": "Hello <@'+request.get_json().get('event').get('user')+'> Knock, knock.","channel": "'+request.get_json().get('event').get('channel')+'"}'
    head = {"Content-type": "application/json", "Authorization": "Bearer xoxb-585478244963-618914840321-GjKFSN1vAF3oqxIApPsTF7dq"} 
    r = requests.post(url='https://slack.com/api/chat.postMessage', data=payload, headers=head)

def chat_bot():
    print(request.get_json())
    if request.get_json().get('challenge'):
        return request.get_json().get('challenge'), 200
    if request.get_json().get('event').get('subtype') != 'bot_message' and request.get_json().get('event').get('subtype') != 'message_deleted':
        text = str(request.get_json().get('event').get('text'))
        t = threading.Thread(target=processRequest(text))
        t.start()
    return 'ok', 200

def date():
    print(json.loads(request.form.get('payload'))['actions'][0]['selected_date'])
    # text = request.form.get('challenge')
    return 'recibido', 200

def addRoutes():
    app.add_url_rule('/slack', 'slack', close_register, methods=['POST'])
    app.add_url_rule('/chat', 'chat', chat_bot, methods=['POST'])
    app.add_url_rule('/date', 'date', date, methods=['POST'])
    app.add_url_rule('/work', 'work', work, methods=['GET'])

def initializeApp():
    addRoutes()
initializeApp()
app.run(debug=True, port=5000)