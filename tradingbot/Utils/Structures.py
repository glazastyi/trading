# -*- coding: utf-8 -*-
class BufferPair(object):
    """Структура данных для хранения минимально  информации о валютной паре
    """
    def __init__(self, symbol, price, quatity):
        """
        :param symbol: название пары
        :param price: цена на пару
        :param quatity: объем пары
        """
        self.symbol = symbol
        self.price = price
        self.quantity = quatity
