import os
import time
from actuator.servo import Servo
from helpers.logger import logging
from helpers.config_loader import load_config, config_file_path

config = load_config()


def unlock(lock_file):
    if os.path.isfile(lock_file):
        try:
            os.remove(lock_file)
            logging.debug("Removed '%s' lock file", lock_file)
        except Exception:
            logging.exception("Error when removing lock file")
            raise
    else:
        logging.warning('Race condition happened')


def lock(lock_file):
    if os.path.isfile(lock_file):
        logging.warning('A cash register is already being closed')
        # TODO implement actual remediation processes in this situation
        time.sleep(3)
        unlock(lock_file)
    else:
        try:
            os.mknod(lock_file)
            logging.debug("Created '%s' lock file", lock_file)
        except Exception:
            logging.exception("Error when creating lock file")
            raise


def close_register(register_id):
    logging.info('---- Closing %s ----', register_id)

    try:
        SERVO_CONTROL_PIN = int(
            config[register_id]['SERVO_CONTROL_PIN'])
        SERVO_DELAY = int(
            config[register_id]['SERVO_DELAY'])
        SERVO_FRECUENCY = int(
            config[register_id]['SERVO_FRECUENCY'])
        SERVO_INITIAL_POSITION = int(
            config[register_id]['SERVO_INITIAL_POSITION'])
        SERVO_MIDDLE_POSITION = int(
            config[register_id]['SERVO_MIDDLE_POSITION'])
        logging.debug("Configuration read from '%s'", config_file_path)
    except Exception:
        logging.exception(
            "Error when reading properties from '%s'", config_file_path)
        raise

    lock_file = "../lock"
    lock(lock_file)

    current_servo = Servo(
        SERVO_CONTROL_PIN,
        SERVO_DELAY,
        SERVO_FRECUENCY,
        SERVO_INITIAL_POSITION,
        SERVO_MIDDLE_POSITION,
    )

    current_servo.close_register()

    unlock(lock_file)
    logging.info('---- Closed %s ----', register_id)
