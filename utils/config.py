import configparser
import os
def read_ini():
    base_dir = os.path.dirname(__file__)        # path to utils/
    ini_path = os.path.join(base_dir, '..', 'conf.ini')  # one level up + file
    ini_path = os.path.abspath(ini_path)        # normalize path

    config = configparser.ConfigParser()
    config.read(ini_path)

    data = {section: dict(config[section]) for section in config.sections()}
    return data


config = read_ini()
# print(config)
