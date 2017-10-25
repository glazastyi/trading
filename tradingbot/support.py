# -*- coding: utf-8 -*-
import httplib
import urllib
import json
import hashlib
import hmac
from collections import OrderedDict
import config
import time

def get_data(method,*args):
    time.sleep(1)

    server = config.API_URl
    keys = get_keys()
    api_key = keys[0]
    secret_key = keys[1]
    data = ''
    if len(args):
        data = OrderedDict(args[0])

    encoded_data = urllib.urlencode(data)
    sign = hmac.new(secret_key, msg = encoded_data, digestmod = hashlib.sha256).hexdigest().upper()
    headers = {"Api-key": api_key, "Sign": sign}

    conn = httplib.HTTPSConnection(server)
    conn.request("GET", method + '?' + encoded_data, '', headers)

    response = conn.getresponse()
    data = json.load(response)
    conn.close()
    return data

def post_data(method,*args):
    time.sleep(1)
    server = config.API_URl
    keys = get_keys()
    api_key = keys[0]
    secret_key = keys[1]

    data = OrderedDict(args[0])
    encoded_data = urllib.urlencode(data)
    sign = hmac.new(secret_key, msg=encoded_data, digestmod=hashlib.sha256).hexdigest().upper()
    headers = {"Api-key": api_key, "Sign": sign, "Content-type": "application/x-www-form-urlencoded"}

    conn = httplib.HTTPSConnection(server)
    conn.request("POST", method, encoded_data, headers)
    response = conn.getresponse()
    data = json.load(response)
    conn.close()
    return data

def get_rank(el):
    return (float(el["best_ask"])/float(el["best_bid"]) - 1) * float(el["volume"]) * float(el["vwap"])
   

def get_pairs(number,exception):
    pairs = [el for el in get_data("/exchange/ticker") if "/BTC" in el["symbol"] and el["best_bid"] > 10 ** (-6)]
    pairs = sorted(pairs, key = lambda el: get_rank(el), reverse = True)
    tmp = []
    for i, el in enumerate(pairs):
        if el["symbol"] in exception or float(el["best_ask"])/float(el["best_bid"]) > 1.5:
            tmp.append(i)
    for i, el in enumerate(tmp):
        pairs.pop(el - i)

    processed_data = pairs[15:15 + number]
    return processed_data

def get_nonzero_balances():
    data = get_data("/payment/balances", [])
    filtered_data = []
    for el in data:
        if el["type"] == "total" and el["value"] != 0 and el["currency"] not in config.EXCLUSION_CURRENCY:
            filtered_data.append("%s/BTC"%el["currency"])
    return filtered_data


def get_balance(value):
    return get_data("/payment/balance",[("currency",value)])["value"]

def make_order(type, pair,price,quantity):
    type_of_action = {"buy":"/exchange/buylimit", "sell":"/exchange/selllimit"}
    order = post_data(type_of_action[type],[('currencyPair', pair),('price', price),('quantity', quantity)])
    return order

def close_opened_orders():
    """Функция должна закрыть все открытые ордера"""
    result = []
    data = get_data("/exchange/client_orders",[("openClosed","OPEN")])
    if data["totalRows"] != 0:
         for el in data['data']:
            result.append(post_data(" /exchange/cancellimit",
                              [("currencyPair",el["currencyPair"]),("orderId",el["id"])]))


def sell_all_pairs():
    '''сначала нужно получить все пары если баланса не хватает то докупаем и продаем
    пока эта операция делается без записи в бд'''
    print get_nonzero_balances()

def  get_keys():
    """
    Functions return secret keys for stock exchange
    return: keys
    """
    with open("keys.txt",'r') as keys_file:
        keys = keys_file.readlines()
        keys[0] = keys[0][:-1]
    return keys