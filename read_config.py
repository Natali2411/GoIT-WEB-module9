import configparser
import os

config_path = os.environ.get("CONFIG_PATH")

config = configparser.ConfigParser()
config.read(config_path)


def get_conf_value(section: str, option: str):
    return config.get(section, option)
