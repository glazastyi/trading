# -*- coding: utf-8 -*-
from tradingbot.Databases.livecoin_warehouse import LivecoinDB
class Order(object):
    def __init__(self, x):
        self.id = x
        self.lastModificationTime = x
        self.currencyPair = str(x)
        self.price = x
        self.quantity = x
        self.state = 0

tmp = LivecoinDB()
tmp.operations_table.insert(1,1,1)
print tmp.operations_table.select("1")
