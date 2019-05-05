from enum import Enum
class CashActions(Enum):
    CLOSE = 'close'
    RESERVE = 'reserve'
    AVAILABILITY = 'availability'
class SlackMessage(Enum):
    ACTION = 0
    CASH_REGISTER = 1
    DATE = 3
    INITIAL_HOUR = 5
    FINISH_HOUR = 7
class ReservationTable(Enum):
    USER = 0
    CASH_REGISTER = 1
    DATE = 2
    INITIAL_HOUR = 3
    FINISH_HOUR = 4
class ReservationTableQueries:
    INSERT = "INSERT INTO reservation VALUES ('%s' ,'%s', '%s', '%s', '%s')"
    EXISTING_RESERVATION = 'SELECT * FROM reservation WHERE cashRegister = ? and date = ? and ? >= initialTimeReservation and ? <= initialTimeReservation or ? >= finishTimeReservation and ? <= finishTimeReservation'
    GET_RESERVATIONS = 'SELECT * FROM reservation WHERE cashRegister = ? and date = ? ORDER BY initialTimeReservation'
    CAN_CLOSE_CASH_REGISTER = 'SELECT * FROM reservation WHERE cashRegister = ? and date = ? and ? >= initialTimeReservation and ? <= finishTimeReservation'
class ResponseSlack:
    GENERIC = '{"text": "%s","channel": "%s"}'
    RESPONSE_CHANNEL_ALL = '{"text":"%s"}'
    CLOSING_CASH_REGISTER = '<@%s> is closing the cash register'
    UNKNOWN = 'Yo no lo entiendos'
    INVALID_ACTION = 'Invalid action'
    CASH_REGISTER_NOT_AVAILABLE = '<@%s> Unfortunately the %s is not available at this time, it is reserved by <@%s>'
    CASH_REGISTER_RESERVED = '<@%s> The %s have been reserved succesfully.'
    PROCESSING_CLOSE_CASH = 'We are processing your request'
    CASH_REGISTER_ALREADY_RESERVED = 'You cannot close the cash register, it is reserved by <@%s>'
    CASH_REGISTER_NOT_RESERVED = 'You cannot close the cash register because you need reserve it'
    TEST = '''{
  "channel": "%s",
  "blocks": [
	{
		"type": "section",
		"text": {
			"text": "A message *with some bold text* and _some italicized text_.",
			"type": "mrkdwn"
		},
		"fields": [
			{
				"type": "mrkdwn",
				"text": "*Usuario*"
			},
			{
				"type": "mrkdwn",
				"text": "*Fecha*"
			},
			{
				"type": "mrkdwn",
				"text": "*Hora inicio*"
			},
			{
				"type": "mrkdwn",
				"text": "*Hora fin*"
			},
			{
				"type": "plain_text",
				"text": "Juan"
			},
			{
				"type": "plain_text",
				"text": "2019-05-05"
			},
			{
				"type": "plain_text",
				"text": "5:30"
			},
			{
				"type": "plain_text",
				"text": "6:30"
			}
		]
	}
]
}'''