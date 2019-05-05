from enum import Enum
class CashActions(Enum):
    CLOSE = 'close'
    RESERVE = 'reserve'
    RESERVATIONS = 'reservations'
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
	INVALID_ACTION = '''{
		"channel": "%s",
		"blocks": [
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "Invalid action"
				},
				"accessory": {
					"type": "image",
					"image_url": "https://scontent.feoh1-1.fna.fbcdn.net/v/t1.0-9/22886279_1847002292276836_3724632587332837591_n.jpg?_nc_cat=107&_nc_ht=scontent.feoh1-1.fna&oh=5db69c676bd014fdbb627c42d0a75291&oe=5D67405C",
					"alt_text": "plants"
				}
			}
		]	
	}'''
	CASH_REGISTER_NOT_AVAILABLE = '<@%s> Unfortunately the %s is not available at this time, it is reserved by <@%s>'
	CASH_REGISTER_RESERVED = '<@%s> The %s have been reserved succesfully.'
	PROCESSING_CLOSE_CASH = 'We are processing your request'
	CASH_REGISTER_ALREADY_RESERVED = 'You cannot close the cash register, it is reserved by <@%s>'
	CASH_REGISTER_NOT_RESERVED = 'You cannot close the cash register because you need reserve it'
	UNKNOWN = 'Try again'
	INVALID_ACTION_COMMAND = '''{
		"blocks": [
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "Invalid action"
				},
				"accessory": {
					"type": "image",
					"image_url": "https://scontent.feoh1-1.fna.fbcdn.net/v/t1.0-9/22886279_1847002292276836_3724632587332837591_n.jpg?_nc_cat=107&_nc_ht=scontent.feoh1-1.fna&oh=5db69c676bd014fdbb627c42d0a75291&oe=5D67405C",
					"alt_text": "plants"
				}
			}
		]	
	}'''
	RESERVATIONS_LIST = '{"channel": "%s", "blocks": %s}'