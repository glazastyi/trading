# -*- coding: utf-8 -*-
import time
import support
import database
import config
import collections

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

def buy():
    print "try to buy"
    """Блок покупки"""
    # смотрю сколько в данный момент пар валют я торгую
    # Если торгую меньше чем максимальное значение торгуемых валют, то пытаюсь докупить еще валют
    # c учетом того что у каждой валюты есть минимальный ордер и мы хотим купить как можн больше
    # валют
    # Если торгую максимальное значение, то получаю пересечение своих валют и наиболее перспективных
    # и пытаюсь докупить используя все тот же алгоритм покупки
    # выставленные ордера записываю в буфер
    # cнова вызываем эту функцию чтобы понять сколько пар мы
    rows = []
    orders = []
    info = support.get_nonzero_balances()
    difference = config.NUMBER_OF_PAIRS - len(info)
    order = collections.namedtuple("order",
                                   ["id", "start_time", "symbol", "ask", "quantity", "end_time",
                                    "bid", "receipts","result"])

    print difference
    if difference >0:
        print "buyng"
        pairs = support.get_pairs(difference,
                                  support.get_nonzero_balances().keys())
        balance = float(support.get_balance("BTC"))  - config.SATOSHI
        count = difference
        print "balance = %s" % balance

        if balance / ( 2* 10 ** (-4)) < difference:
            count = int(balance / (2 * 10 ** (-4)))
        print count
        print balance/count
        for el in pairs[:count]:

            purchase_price = float(el["best_bid"]) + 10 * config.SATOSHI

            quantity = float((balance) / (count * purchase_price*(1+config.COMMISSION)))
            symbol = el["symbol"]
            print symbol,quantity*purchase_price
            order_buy = support.make_order("buy", symbol, str(purchase_price), str(quantity))
            print order_buy
            if order_buy["success"]:

                orders.append(order_buy)
    with open("orders_buffer.txt", "a") as file:
        for el in orders:
            file.write("B%s\n"%el["orderId"])

def sell():
    print "try to sell"
    """Блок продажи доступных ордеров"""
    # смотрю сколько валют доступно к продаже
    ##беру валюту, смотрю цену по которой она счас торгруется(удачнить что конкретно это за цена)
    ##смотрю какой объем этой валюты я сейчас могу продать, если есть что продать выставляю ордер
    ## и записываю id этого ордера в буфер

    #беру валютную пару,выбираю все позиции в бд, которые можно продать с выгодой,
    # получаем все доступные пары, которые мы можем продать
    pairs = support.get_data("/payment/balances", [])
    available_pairs = []
    candidates = []

    for el in pairs:
        currency = el["currency"]
        if ((currency not in config.EXCLUSION_CURRENCY) and (el["type"] == "available")
            and (float(el["value"])) > 0):
            available_pairs.append(el)
            # для каждого элемента получаем информацию о том за сколько мы сейчас можем его продать
            tmp = support.get_data("/exchange/ticker",
                                   [("currencyPair", "%s/BTC" % el["currency"])])
            print "tmp",tmp
            ##над ценой продажи нужно еще подумать
            sell_price = float(tmp["best_ask"]) - 10 * config.SATOSHI
            print currency,float(tmp["best_ask"]) , sell_price
            # получаем информацию о том сколько сейчас денег куплено и по какой цене, выбираем только те,
            # с которых мы можем получить выгоду
            available_db1 = database.select(["purchased_quantity", "sold_quantity"],
                                           ["symbol == ","purchase_price <=","result == "],
                                           ("'%s/BTC'"%currency,sell_price / config.INCOME,0))

            available_db2 = database.select(["purchased_quantity", "sold_quantity"],
                                           ["symbol == ", "%s - start_time >= " % (time.time()),"result == "],
                                           ("'%s/BTC'"%currency, config.MAX_TIME, 0))

            available_db = available_db1 + available_db2
            quantity = 0.0
            print "quant",quantity
            # подсчитываем объем того сколько мы можем продать
            for i in available_db:
                print "selling",currency, i
                print (float(i[0])),(float(i[1]))
                quantity = (float(i[0]) - (float(i[1])))
                print quantity
                if quantity * sell_price >= 0.0001:
                    candidate = support.make_order("sell", "%s/BTC" % currency, sell_price,
                                                   quantity)
                    print  candidate
                    if candidate["success"]:
                        candidates.append(candidate)

    with open("orders_buffer.txt", "a") as file:
        print candidates
        for el in candidates:
            file.write("S%s\n"%el["orderId"])

def new_algoritm(waiting_time):
    while(True):
        close_orders()
        sell()
        buy()
        print "|||||||||||||||||||||||| ROUND |||||||||||||||||||||||| "
        time.sleep(waiting_time)

new_algoritm(200)