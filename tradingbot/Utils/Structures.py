# -*- coding: utf-8 -*-
class BufferPair(object):
    def __init__(self, symbol, price, quatity):
        """
        
        :param symbol: название пары
        :param price: цена на пару
        :param quatity: объем который мы покупаем
        """
        self.symbol = symbol
        self.price = price
        self.quantity = quatity
