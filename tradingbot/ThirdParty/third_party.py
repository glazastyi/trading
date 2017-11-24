# -*- coding: utf-8 -*-
import hashlib
import hmac
import httplib
import json
import os
import time
import urllib
from collections import OrderedDict

def get_keys():
    """
    Functions return secret keys for stock exchange
    return: keys
    """


    with open(os.path.join(get_config_dir(),"keys.txt"), "r") as keys_file:
        keys = keys_file.readlines()
        keys[0] = keys[0][:-1]

    return keys

def get_purchase_price(value):
    return round((value + tradingbot.config.OVER_BURSE) * (1 + tradingbot.config.COMMISSION), 8)

def get_sell_price(currency):
    tmp = get_data("/exchange/ticker",[("currencyPair", "%s/BTC" % currency)])
    return round((float(tmp["best_ask"]) - tradingbot.config.OVER_BURSE) / (1 + tradingbot.config.COMMISSION), 8)

def get_num_of_pairs(balance):
    result = tradingbot.config.NUMBER_OF_PAIRS
    if balance / (10 ** (-4)) < tradingbot.config.NUMBER_OF_PAIRS:
        count = int(balance / (10 ** (-4)))
        result = count
    return result

def get_main_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def get_config_dir():
    return os.path.join(get_main_dir(),"configs")

def get_data_dir(exchanger):
    return os.path.join(get_main_dir(),"Data/{}.db".format(exchanger))

