import logging
from helpers.config_loader import load_config

config = load_config()
logging_path = "{}/actuator.log".format(
    config['SYSTEM']['WORKING_DIRECTORY'])

logging.basicConfig(
    filename=logging_path,
    filemode='a',
    format='%(asctime)s - PID %(process)d - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
