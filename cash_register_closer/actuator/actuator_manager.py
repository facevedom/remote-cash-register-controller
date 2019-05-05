import time
import threading
from actuator.servo import Servo
from helpers.logger import logging


class ActuatorManager:

    def __init__(self, config):
        self.__config = config
        self.__servos_locked = False
        self.__request_queue = []
        self.__cash_registers = []
        self.__servos = {}

        self.list_available_cash_registers()

    def list_available_cash_registers(self):
        for property in self.__config:
            if 'SERVO_CONTROL_PIN' in self.__config[property]:
                self.__cash_registers.append(property)
        logging.info('Found these cash registers: %s', self.__cash_registers)

    def request_closing(self, register_id):
        if register_id in self.__request_queue:
            logging.debug(
                'Rejected an already existing request to close %s', register_id)
            return

        self.__request_queue.append(register_id)
        logging.debug('Scheduling closing of %s', register_id)

        while(self.__servos_locked):
            time.sleep(0.2)

        self.close_register(register_id)
        self.__request_queue.remove(register_id)

    def close_register(self, register_id):
        logging.info('---------- Closing %s ----------', register_id)
        self.__servos_locked = True

        try:
            servo_properties = self.__config[register_id]
            CONTROL_PIN = int(servo_properties['SERVO_CONTROL_PIN'])
            DELAY = float(servo_properties['SERVO_DELAY'])
            FRECUENCY = int(servo_properties['SERVO_FRECUENCY'])
            INITIAL_POSITION = int(
                servo_properties['SERVO_INITIAL_POSITION'])
            MIDDLE_POSITION = int(
                servo_properties['SERVO_MIDDLE_POSITION'])
        except Exception:
            logging.exception(
                "Error when reading properties from configuration for %s", register_id)
            raise

        current_servo = Servo(
            CONTROL_PIN,
            DELAY,
            FRECUENCY,
            INITIAL_POSITION,
            MIDDLE_POSITION,
        )

        current_servo.pivot()
        self.__servos_locked = False
        logging.info('---------- Closed  %s ----------', register_id)
