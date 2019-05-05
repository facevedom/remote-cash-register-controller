import time
from helpers.logger import logging
import RPi.GPIO as GPIO


class Servo:

    def __init__(self, control_pin, delay, frecuency, initial_position, middle_position):
        self.__control_pin = control_pin
        self.__delay = delay
        self.__frecuency = frecuency
        self.__initial_position = initial_position
        self.__middle_position = middle_position

    def move(self, position):
        logging.debug("Moving servo to position '%s'", position)
        self.__actuator.ChangeDutyCycle(position)

    def teardown(self):
        self.__actuator.stop()
        try:
            GPIO.cleanup()
            logging.debug("Communication with GPIOs closed")
        except Exception:
            logging.exception("Failed to teardown GPIO channels")
            raise

    def setup(self):
        try:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.__control_pin, GPIO.OUT)
            logging.debug("Communication with GPIOs established for pin %s", self.__control_pin)
        except Exception:
            logging.exception("Failed to setup GPIO")
            raise
        
        self.__actuator = GPIO.PWM(self.__control_pin, self.__frecuency)
        self.__actuator.start(self.__initial_position)

    def pivot(self):
        self.setup()
        positions = [self.__initial_position,
                     self.__middle_position,
                     self.__initial_position]

        for position in positions:
            time.sleep(self.__delay)
            self.move(position)

        self.teardown()