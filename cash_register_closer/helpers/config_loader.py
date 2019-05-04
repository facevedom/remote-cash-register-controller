import os
import configparser

config_file_path = "config.ini" # this path is relative to the caller!


def load_config(config_file_path=config_file_path):

    if not os.path.isfile(config_file_path):
        raise Exception(
            "Config file {} doesn't exist".format(config_file_path))

    config = configparser.ConfigParser()
    config.read(config_file_path)
    return(config)
