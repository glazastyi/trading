# -*- coding: utf-8 -*-
from tradingbot.Databases.livecoin_table import LivecoinDB
class Order(object):
    def __init__(self, x):
        self.id = x
        self.lastModificationTime = x
        self.currencyPair = str(x)
        self.price = x
        self.quantity = x
        self.state = 0

tmp = LivecoinDB()
[tmp.buy_table.insert(Order(x)) for x in range(10)]
print(tmp.buy_table.select("foo/tmp"))
print(tmp.join_buy_on_sell())