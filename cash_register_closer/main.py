#from app import slack_python
from helpers.logger import logging
from helpers.config_loader import load_config, config_file_path
from actuator.actuator_manager import ActuatorManager

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

config = load_config()
logging.debug("Using configuration from '%s'", config_file_path)

actuator = ActuatorManager(config)
actuator.request_closing("CASH-REGISTER-1")
