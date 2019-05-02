import time
import logging
import RPi.GPIO as GPIO

def move_servo(servo, position):
    time.sleep(0.2)
    servo.ChangeDutyCycle(position)

logging.basicConfig(
    filename='/var/log/remote-cash-controller.log',
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

SERVO_FRECUENCY = 50
SERVO_CONTROL_PIN = 32
SERVO_INITIAL_POSITION = 7
SERVO_MIDDLE_POSITION = 12
logging.info('---- Running at %sHz on pin %s ----', SERVO_FRECUENCY, SERVO_CONTROL_PIN)

GPIO.setmode(GPIO.BOARD)
logging.debug('Using board numbering for GPIOs')

GPIO.setup(SERVO_CONTROL_PIN, GPIO.OUT)

servo = GPIO.PWM(SERVO_CONTROL_PIN, SERVO_FRECUENCY)

try:
    logging.info('Moving')
    logging.debug('Moving servo to initial position')
    servo.start(SERVO_INITIAL_POSITION)                     # This doesn't move the servo to a particular position
    move_servo(servo, SERVO_INITIAL_POSITION)
    logging.debug('Moving servo to middle position')
    move_servo(servo, SERVO_MIDDLE_POSITION)
    logging.debug('Returning servo to initial position')
    move_servo(servo, SERVO_INITIAL_POSITION)    
    servo.stop()
    logging.info('Movement ended')
except Exception as e:
  logging.exception("Something bad happened")

logging.debug('Releasing GPIO channels')
GPIO.cleanup()