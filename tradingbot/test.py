# -*- coding: utf-8 -*-
import support
import database
import config
import time
print int(False)
def get_successful_orders(orders):
    return_orders = [[],[]]
    for order in orders:
        type_of_order = order[:1]
        order_num = order[1:-1]
        info = support.get_data("/exchange/order", [("orderId", order_num)])
        print info
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
        info = support.get_data("/exchange/order", [("orderId", order)])
        quantity = float(info["quantity"]) - float(info["remaining_quantity"])
        print info
        symbol = info["symbol"]
        price = float(info["price"])
        cond = float(info["price"]) / config.INCOME

        el = database.select(
            ["id", "purchased_quantity", "sold_quantity", "profit"],
            ["symbol == ", "result == "],
            ("'%s'" % symbol,0))
        el = el[0]
        print el
        purchased_quantity = float(el[1])
        sold_quantity = float(el[2])
        profit = float(el[3])
        remaining_quantity = purchased_quantity - sold_quantity
        database.update(["sold_quantity", "profit","result"],
                            (sold_quantity + quantity,
                             profit + quantity * price,
                             int(remaining_quantity == quantity)),
                            ["id == "], (el[0],))

def close_buy_orders(orders):
    for order in orders:
        info = support.get_data("/exchange/order", [("orderId", order)])
        quantity = float(info["quantity"]) - float(info["remaining_quantity"])

        symbol = info["symbol"]
        price = float(info["price"])
        database.insert(order, time.time(), symbol, quantity, price)

def close_orders():
    with open("orders_buffer.txt", "r") as file:
        orders = file.readlines()

    successful_orders = get_successful_orders(orders)
    print successful_orders
    close_buy_orders(successful_orders[0])
    close_sell_orders(successful_orders[1])
    with open("orders_buffer.txt", "w") as file:
        print "hi"

close_orders()