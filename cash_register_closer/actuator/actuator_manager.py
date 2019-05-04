import time
import threading
from actuator.servo import Servo
from helpers.logger import logging


class ActuatorManager:

    def __init__(self, config):
        self.__config = config
        self.__servos_locked = False
        self.__request_queue = []

    def request_closing(self, register_id):
        if register_id in self.__request_queue:
            logging.debug(
                'Rejected an already existing request to close %s', register_id)
            return

        self.__request_queue.append(register_id)
        logging.debug('Scheduling closing of %s', register_id)

        while(self.__servos_locked):
            time.sleep(0.1)

        self.close_register(register_id)
        self.__request_queue.remove(register_id)

    def close_register(self, register_id):
        self.__servos_locked = True
        logging.info('---------- Closing %s ----------', register_id)

        try:
            SERVO_CONTROL_PIN = int(
                self.__config[register_id]['SERVO_CONTROL_PIN'])
            SERVO_DELAY = float(
                self.__config[register_id]['SERVO_DELAY'])
            SERVO_FRECUENCY = int(
                self.__config[register_id]['SERVO_FRECUENCY'])
            SERVO_INITIAL_POSITION = int(
                self.__config[register_id]['SERVO_INITIAL_POSITION'])
            SERVO_MIDDLE_POSITION = int(
                self.__config[register_id]['SERVO_MIDDLE_POSITION'])
        except Exception:
            logging.exception(
                "Error when reading properties from configuration")
            raise

        current_servo = Servo(
            SERVO_CONTROL_PIN,
            SERVO_DELAY,
            SERVO_FRECUENCY,
            SERVO_INITIAL_POSITION,
            SERVO_MIDDLE_POSITION,
        )

        current_servo.close_register()

        time.sleep(3)

        self.__servos_locked = False
        logging.info('---------- Closed  %s ----------', register_id)
