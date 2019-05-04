import os
import logging
from helpers.config_loader import load_config

config = load_config()
logging_file_path = "{}/actuator.log".format(
    config['SYSTEM']['WORKING_DIRECTORY'])

if not os.path.isfile(logging_file_path):
    os.mknod(logging_file_path)

logging.basicConfig(
    filename=logging_file_path,
    filemode='a',
    format='%(asctime)s - PID %(process)d - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
