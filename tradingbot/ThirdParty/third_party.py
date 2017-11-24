# -*- coding: utf-8 -*-

import os


def get_keys():
    """
    Functions return secret keys for stock exchange
    return: keys
    """
    with open(os.path.join(get_config_dir(), "keys.txt"), "r") as keys_file:
        keys = keys_file.readlines()
        keys[0] = keys[0][:-1]

    return keys


def get_main_dir():
    """
    :return: путь до директории проекта 
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def get_config_dir():
    """
    :return: путь к конфигурации проекта 
    """
    return os.path.join(get_main_dir(), "configs")


def get_data_dir(exchanger):
    """
    :param exchanger: название биржи
    :return: путь до хранилища определенной биржи
    """
    return os.path.join(get_main_dir(), "Data/{}.db".format(exchanger))
