import sqlite3
import requests
from flask import Flask
from flask import request
from flask import Response
import os
import json
import threading
from constants import *
from time import gmtime, strftime
from datetime import datetime

URL = os.getenv('SLACK_URL')
TOKEN = os.getenv('SLACK_TOKEN')
messageStack = []
app = Flask(__name__)

def work():
    return 'work', 200

def initDB():
    connection = sqlite3.connect('cash_register.db')
    sql_service = connection.cursor()
    return connection, sql_service

def closeDB(connection, sql_service):
    sql_service.close()
    connection.commit()
    connection.close()

def sendNotificationForTeam(userId):
    payloadMessage = ResponseSlack.CLOSING_CASH_REGISTER % userId
    payload = ResponseSlack.RESPONSE_CHANNEL_ALL % payloadMessage
    head = {"Content-type": "application/json"} 
    r = requests.post(url=URL, data=payload, headers=head)

def canCloseCashRegister(userId, cash_register):
    currentTime = str(datetime.now()).split(' ')
    date = currentTime[0]
    time = '%s:%s' % (currentTime[1].split(':')[0], currentTime[1].split(':')[1])
    connection, sql_service = initDB()
    sql_service.execute(ReservationTableQueries.CAN_CLOSE_CASH_REGISTER, [cash_register, date, time, time])
    canClose = False
    result = sql_service.fetchone()
    userReserved = None
    if result:
        if result[ReservationTable.USER.value] == userId:
            canClose = True
        else:
            userReserved = result[ReservationTable.USER.value]
    closeDB(connection, sql_service)
    return canClose, userReserved
def close_register():
    user = request.form.get('user_id')
    message = request.form.get('text').split(' ')
    if message:
        action = message[SlackMessage.ACTION.value]
        if action == CashActions.CLOSE.value:
            cash_register = message[SlackMessage.CASH_REGISTER.value]
            canClose, userReserved = canCloseCashRegister(user, cash_register)
            if canClose:
                sendNotificationForTeam(user)
                response = ResponseSlack.PROCESSING_CLOSE_CASH
            else:
                if userReserved:
                    response = ResponseSlack.CASH_REGISTER_ALREADY_RESERVED % userReserved
                else:
                    response = ResponseSlack.CASH_REGISTER_NOT_RESERVED
        else:
            response = ResponseSlack.INVALID_ACTION
    else:
        response = ResponseSlack.UNKNOWN
    # print(request.form)
    # t = threading.Thread(target=motor_controller.rotate)
    # t.start()

    return response, 200

def getAvailability(cash_register, date, initial_hour, finish_hour, sql_service):
    sql_service.execute(ReservationTableQueries.EXISTING_RESERVATION, [cash_register, date, initial_hour, initial_hour, finish_hour, finish_hour])
    availability = True
    userReservation = None
    data = sql_service.fetchone()
    if data:
        availability = False
        userReservation = data[ReservationTable.USER.value]
    return availability, userReservation
    
def doReservation(message, sql_service, userId, channel):
    cash_register = message[SlackMessage.CASH_REGISTER.value]
    date = message[SlackMessage.DATE.value]
    initial_hour = message[SlackMessage.INITIAL_HOUR.value]
    finish_hour = message[SlackMessage.FINISH_HOUR.value]
    available, userReserved = getAvailability(cash_register, date, initial_hour, finish_hour, sql_service)
    if available:
        query = ReservationTableQueries.INSERT % (userId, cash_register, date, initial_hour, finish_hour)
        sql_service.execute(query)
        reserved = ResponseSlack.CASH_REGISTER_RESERVED % (userId, cash_register)
        messagePayload = ResponseSlack.GENERIC % (reserved, channel)
    else:
        availability = ResponseSlack.CASH_REGISTER_NOT_AVAILABLE % (userId, cash_register, userReserved)
        messagePayload = ResponseSlack.GENERIC % (availability, channel)
    return messagePayload
def getReservations(sql_service, cash_register, date, channel):
    sql_service.execute(ReservationTableQueries.GET_RESERVATIONS, [cash_register, date])
    data = sql_service.fetchall()
    print(data)
    return ResponseSlack.TEST % (channel)
def ResponseSlackBot(messagePayload):
    payload = messagePayload
    bearer = "Bearer %s" % TOKEN
    head = {"Content-type": "application/json", "Authorization": bearer}
    r = requests.post(url='https://slack.com/api/chat.postMessage', data=payload, headers=head)
def processRequest(text, clientId, userId, channel):
    connection, sql_service = initDB()
    message = text.split(' ')
    messagePayload = ''
    if message:
        action = message[SlackMessage.ACTION.value]
        if action == CashActions.RESERVE.value:
            messagePayload = doReservation(message, sql_service, userId, channel)
        elif action == CashActions.AVAILABILITY.value:
            cash_register = message[SlackMessage.CASH_REGISTER.value]
            date = message[SlackMessage.DATE.value]
            messagePayload = getReservations(sql_service, cash_register, date, channel)
        else:
            messagePayload = ResponseSlack.GENERIC % (ResponseSlack.INVALID_ACTION, channel)
    else:
        messagePayload = ResponseSlack.GENERIC % (ResponseSlack.UNKNOWN, channel)
    ResponseSlackBot(messagePayload)
    closeDB(connection, sql_service)
    messageStack.remove(clientId)

def chat_bot():
    process = False
    clientId = request.get_json().get('event').get('client_msg_id')
    if request.get_json().get('challenge'):
        return request.get_json().get('challenge'), 200
    try:
        messageStack.index(clientId)
        process = False
    except:
        process = True
    if process and request.get_json().get('event').get('subtype') != 'bot_message' and request.get_json().get('event').get('subtype') != 'message_deleted':
        messageStack.append(clientId)
        text = request.get_json().get('event').get('text')
        userId = request.get_json().get('event').get('user')
        channel = request.get_json().get('event').get('channel')
        t = threading.Thread(target=processRequest(text, clientId, userId, channel))
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
# conn, c = initDB()
# c.execute("DROP TABLE reservation")
# c.execute('''CREATE TABLE reservation
#              (user text, cashRegister text, date text, initialTimeReservation time, finishTimeReservation time)''')
# closeDB(conn, c)
app.run(debug=True, port=5000)
