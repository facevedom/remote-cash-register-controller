import time
from helpers.logger import logging
import RPi.GPIO as GPIO


class Servo:

    def __init__(self, control_pin, frecuency, initial_position, middle_position):
        self.__control_pin = control_pin
        self.__frecuency = frecuency
        self.__initial_position = initial_position
        self.__middle_position = middle_position

        try:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.__control_pin, GPIO.OUT)
        except Exception:
            logging.exception("Failed to setup GPIO")
            raise

        self.actuator = GPIO.PWM(self.__control_pin, self.__frecuency)
        self.actuator.start(self.__initial_position)

    def move(self, position):
        logging.debug("Moving servo to position '%s'", position)
        self.actuator.ChangeDutyCycle(position)

    def close_register(self):
        time.sleep(0.2)
        self.move(self.__initial_position)
        time.sleep(0.2)
        self.move(self.__middle_position)
        time.sleep(0.2)
        self.move(self.__initial_position)
        self.teardown()

    def teardown(self):
        self.actuator.stop()
        GPIO.cleanup()
