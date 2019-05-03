import time
from logger import logging
import RPi.GPIO as GPIO


class Servo:

    def __init__(self, control_pin, frecuency, initial_position, middle_position):
        self.control_pin = control_pin
        self.frecuency = frecuency
        self.initial_position = initial_position
        self.middle_position = middle_position

        try:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.control_pin, GPIO.OUT)
        except Exception:
            logging.exception("Failed to setup GPIO")
            raise

        self.actuator = GPIO.PWM(self.control_pin, self.frecuency)
        self.actuator.start(self.initial_position)

    def move(self, position):
        logging.debug("Moving servo to position '%s'", position)
        self.actuator.ChangeDutyCycle(position)

    def close_register(self):
        time.sleep(0.2)
        self.move(self.initial_position)
        time.sleep(0.2)
        self.move(self.middle_position)
        time.sleep(0.2)
        self.move(self.initial_position)
        self.teardown()

    def teardown(self):
        self.actuator.stop()
        GPIO.cleanup()
