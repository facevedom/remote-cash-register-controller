from actuator.actuator_manager import ActuatorManager
from helpers.logger import logging
from helpers.config_loader import load_config, config_file_path

config = load_config()
logging.debug("Using configuration from '%s'", config_file_path)

actuator = ActuatorManager(config)
