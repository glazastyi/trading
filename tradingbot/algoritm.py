import collections
import time

import config
from tradingbot import database
from tradingbot.ThirdParty import support


def action():
    sell()
    buy()


def buy():
    print "Try to buy"
    order = collections.namedtuple("order",
                                   ["id", "start_time", "symbol", "ask", "quantity", "end_time", "bid", "receipts",
                                    "result"])
    current = [order._make(el) for el in database.select()]
    exception = [el.symbol for el in current]
    difference = config.NUMBER_OF_PAIRS - len(current)
    print "dif = %d"%difference
    if difference:
        pairs = support.get_pairs(difference, exception)
        balance = float(support.get_balance("BTC")) * (1 - config.COMMISSION)
        count = difference
        print "balance = %s"%balance
        print balance / (10 ** (-4))
        if  balance / (10 ** (-4)) < difference:
            count = int(balance / (10 ** (-4)))
        print "count = %s"%count
        for el in pairs[:count]:
            time.sleep(1)
            print el["symbol"]
            ask = float(el["best_ask"])
            quantity = str((balance) / (count * ask))
            print (float(quantity) * float(ask))
            symbol = el["symbol"]
            order_buy = support.make_order("buy", symbol, str(ask), quantity)
            if order_buy["success"]:
                database.insert(int(order_buy["orderId"]), time.time(), symbol, str(ask), str(quantity))
            print order_buy


def sell():
    print "Try to sell"
    order = collections.namedtuple("order",
                                   ["id", "start_time", "symbol", "ask", "quantity", "end_time", "bid", "receipts",
                                    "result"])
    current = [order._make(el) for el in database.select()]
    for el in current:
        time.sleep(1)
        tmp = support.get_data("/exchange/ticker", [("currencyPair", el.symbol)])
        sell_price = float(tmp["best_bid"])

        bought_price = float(el.ask)
        print el.symbol, float(sell_price) / float(bought_price)
        if (sell_price > bought_price * config.INCOME) or (int(time.time()) - int(el.start_time) > config.MAX_TIME):
            time.sleep(1)
            print "sell success"
            quantity_sell = str(support.get_balance(el.symbol[:-4]))
            order_sell = support.make_order("sell", el.symbol, str(sell_price), quantity_sell)
            if order_sell["success"]:
                receipts = (sell_price - bought_price) * float(quantity_sell)
                database.update(int(el.id), time.time(), sell_price, str(receipts))
                print order_sell


while(True):
    action()
    print "ROUND"
    time.sleep(120)