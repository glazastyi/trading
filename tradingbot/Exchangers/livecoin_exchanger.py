# -*- coding: utf-8 -*-
import tradingbot.ExchangersAPI.livecoin_api as api
from tradingbot.Databases.livecoin_warehouse import LivecoinDB


class LivecoinExchanger(object):
    def __init__(self):
        self.opened_orders = {"sell": [], "buy": []}
        self.DB = LivecoinDB()

    @staticmethod
    def get_pairs():
        """
        Функция возвращает доступные для покупки пары
        :return:
        """
        return api.get_exchange_ticker()

    @staticmethod
    def get_btc_balance():
        return api.get_payment_balance("BTC")

    def get_current_pairs(self):
        return self.DB.get_current_pairs()

    def get_opened_orders(self):
        return self.opened_orders

    def close_orders(self):
        for order in self.opened_orders["sell"] + self.opened_orders["buy"]:
            api.post_exchange_cancel_limit(order.symbol, order.id)

    def get_successfull_orders(self):
        """
        Функция обновляет информацию об открытых ордерах
        и выбирает из них успешные
        :return: 
        """
        self.update_opened_orders()
        result = {"sell": [], "buy": []}
        for mode in self.opened_orders.keys():
            for order in self.opened_orders[mode]:
                if order.remaining_quantity != order.quantity:
                    result[mode].append(order)

        return result

    def get_sell_pairs(self):
        return self.DB.get_sell_pairs()

    def update_opened_orders(self):
        for key in self.opened_orders.keys():
            self.opened_orders[key] = map(lambda x:
                                          api.get_exchange_order(x.id),
                                          self.opened_orders[key])

    def update_orders(self):
        """
        Функция обновляет информацию об успешных ордерах в буферных таблицах бд
        :return: 
        """
        self.DB.update_orders(self.get_successfull_orders())

    def append_opened_order(self, mode, order):
        self.opened_orders[mode].append(api.get_exchange_order(order))

    def make_sell_order(self, pairs_to_sell):
        for pair in pairs_to_sell:
            order = api.post_exchange_sell_limit(pair.symbol, pair.price,
                                                 pair.quantity)
            self.append_opened_order("sell", order)

    def make_buy_orders(self, pairs_to_buy):
        for pair in pairs_to_buy:
            order = api.post_exchange_buy_limit(pair.symbol, pair.price,
                                                pair.quantity)
            self.append_opened_order("buy", order)
