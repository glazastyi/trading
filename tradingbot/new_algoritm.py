# -*- coding: utf-8 -*-
import time
import support
import database
import config
import collections

def close_orders():
    print "try to close orders"
    """Закрываю открытые ордера"""
    # считываю выставленные ордера
    orders = []
    with open("orders_buffer.txt", "r") as file:
        orders = file.readlines()
    # обновляю информацию в базе данных
    for order in orders:

        info = support.get_data("/exchange/order", [("orderId", order[1:-1])])
        quantity = float(info["quantity"]) - float(info["remaining_quantity"])

        symbol = info["symbol"]
        price = float(info["price"])
        # для купленных денег делаю запись в бд
        print order[0]
        if order[0] == "B":
            print quantity > 0.0
            if quantity > 0.0:
                database.insert(order[1:-1], time.time(), symbol, quantity, price)

        if order[0] == "S":
            # нужно выбрать все купленные пары и закрывать их постепенно
            # нужно выбрать те которые покупались с учетом выгоды
            cond = float(info["price"]) / config.INCOME

            update_list = database.select(["id", "purchased_quantity", "sold_quantity", "profit"],
                                          ["symbol == ","purchase_price <= ", "result == "], ("'%s'"%symbol,cond,0))



            print "here", update_list
            for el in update_list:
                balance = float(el[1]) - float(el[2])
                profit = float(el[3])
                print quantity, float(el[2]),profit,price
                if balance > quantity:
                    database.update(["sold_quantity", "profit"],
                                    (float(el[2]) + quantity,profit + quantity * price),
                                    ["id == "], (el[0],))
                else:
                    quantity -= balance
                    database.update(["sold_quantity", "profit", "end_time", "result"],
                                    (float(el[1]), profit + quantity * price, time.time(), 1),
                                    ["id == "], (el[0],))

        # закрываю ордер
        support.post_data("/exchange/cancellimit", [("currencyPair", symbol), ("orderId", order[1:-1])])
    print "clearing order buffer"
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