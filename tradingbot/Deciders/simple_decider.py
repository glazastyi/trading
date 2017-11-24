# -*- coding: utf-8 -*-
from tradingbot.Utils.Structures import BufferPair


class SimpleDecider(object):
    def __init__(self, exclusion_currency, min_bid, start_pair):
        self.exclusion_currency = exclusion_currency
        self.min_bid = min_bid
        self.start_pair = start_pair

    def get_solution(self, number_of_pairs, balance, all_pairs, current_pairs):
        #todo: use nonlocal

        correct_pairs = self.get_correct_pairs(self)

        return map(lambda x: BufferPair(x.symbol, x.price,
                                         self.get_quantity(x)), correct_pairs)

    def get_quantity(self):
        pass

    def get_correct_pairs(self):
        nonlocal
        pairs = [el for el in self.all_pairs if
             "/BTC" in el.symbol and el.best_bid > self.min_bid]
        pairs = sorted(pairs, key=lambda el: self.get_rank(el), reverse=True)

        current_symbols = [el.symbol for el in self.current_pairs
                           if el.quantity < 100 * self.min_bid]

        correct_pairs = [el for el in pairs
                         if el.symbol not in current_symbols and
                            el.symbol not in self.exclusion_currency and
                            float(el.best_ask) / float(el.best_bid) > 1.5]

        end_pair = self.start_pair + self.number_of_pairs

        return correct_pairs[self.start_pair : end_pair]

    @staticmethod
    def get_rank(el):
        #todo: проверить формулу
        """
        возвращает ранк пары
        :param el: 
        :return: 
        """
        return (float(el.best_ask) / float(el.best_bid) - 1) * \
               float( el.volume) * float(el.vwap)