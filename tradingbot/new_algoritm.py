# -*- coding: utf-8 -*-
import time

import config
from tradingbot.Databases import Sqlite3_API
from tradingbot.ThirdParty import third_party


def get_successful_orders(orders):
    return_orders = [[],[]]
    for order in orders:
        type_of_order = order[:1]
        order_num = order[1:-1]
        info = third_party.get_data("/exchange/order", [("orderId", order_num)])
        quantity = float(info["quantity"]) - float(info["remaining_quantity"])
        if quantity > 0.0:
            return_orders[type_of_order == "S"].append(order_num)
    return return_orders

def close_sell_orders(orders):
    """
    главный поступат - не покупаем валюту пока ее не продали
    :param orders: 
    :return: 
    """
    for order in orders:
        info = third_party.get_data("/exchange/order", [("orderId", order)])
        quantity = float(info["quantity"]) - float(info["remaining_quantity"])

        symbol = info["symbol"]
        price = float(info["price"])
        cond = float(info["price"]) / config.INCOME

        el = Sqlite3_API.select(
            ["id", "purchased_quantity", "sold_quantity", "profit"],
            ["symbol == ", "result == "],
            ("'%s'" % symbol,0))
        el = el[0]

        purchased_quantity = float(el[1])
        sold_quantity = float(el[2])
        profit = float(el[3])
        remaining_quantity = purchased_quantity - sold_quantity
        Sqlite3_API.update(["sold_quantity", "profit", "result"],
                           (sold_quantity + quantity,
                             profit + quantity * price,
                             int(remaining_quantity == quantity)),
                           ["id == "], (el[0],))

def close_buy_orders(orders):
    for order in orders:
        info = third_party.get_data("/exchange/order", [("orderId", order)])
        quantity = float(info["quantity"]) - float(info["remaining_quantity"])

        symbol = info["symbol"]
        price = float(info["price"])
        Sqlite3_API.insert(order, time.time(), symbol, quantity, price)

def close_orders():
    with open("orders_buffer.txt", "r") as file:
        orders = file.readlines()

    successful_orders = get_successful_orders(orders)

    close_buy_orders(successful_orders[0])
    close_sell_orders(successful_orders[1])
    with open("orders_buffer.txt", "w") as file:
        print " "

def buy():
    """Блок покупки"""
    balance = float(third_party.get_balance("BTC"))
    count  = third_party.get_num_of_pairs(balance)
    pairs = third_party.get_pairs(count, [])
    part_of_bank = balance/count
    for el in pairs:
        purchase_price = third_party.get_purchase_price(float(el["best_bid"]))
        quantity = part_of_bank / purchase_price
        symbol = el["symbol"]
        order_buy = third_party.make_order("buy", symbol, str(purchase_price), quantity)

        if order_buy["success"]:
            with open("orders_buffer.txt", "a") as file:
                file.write("B%s\n"%order_buy["orderId"])

def sell():

    pairs = third_party.get_data("/payment/balances", [])
    for el in pairs:
        currency = el["currency"]
        if ((currency not in config.EXCLUSION_CURRENCY) and (el["type"] == "available")
            and (float(el["value"])) > 0):
            sell_price = third_party.get_sell_price(currency)
            volume = third_party.get_sold_volume(currency, sell_price)
            order = third_party.make_order("sell", "%s/BTC" % currency, sell_price, volume)
            if order["success"]:
                with open("orders_buffer.txt", "a") as file:
                    file.write("S%s\n"%order["orderId"])


def new_algoritm(waiting_time):
    while(True):
        close_orders()
        sell()
        buy()

        time.sleep(waiting_time)

new_algoritm(200)