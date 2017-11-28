# -*- coding: utf-8 -*-
import tradingbot.ExchangersAPI.livecoin_api as api
from tradingbot.Databases.livecoin_warehouse import LivecoinDB
from tradingbot.ThirdParty.third_party import get_data_dir2

class LivecoinExchanger(object):
    """Класс-обертка для API биржи"""

    def __init__(self):
        """
        Инициализация Хранилища
        """
        # todo: заменить opened_orders на таблицу в бд
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
        """
        :return: Текущий баланс биткоинов 
        """
        result = 0
        for element in api.get_payment_balance("BTC"):
            if element.type == "available":
                result = element.value
        print "balance = {}".format(result)
        return result

    def get_current_pairs(self):
        """
        :return: Текущий баланс по валютным парам 
        """
        return self.DB.get_current_pairs()


    def get_opened_orders(self):
        """
        :return: Словарь с текущими открытыми ордерами 
        """
        return self.opened_orders

    def close_orders(self):
        """
        Функция закрытия открытых ордеров на бирже
        :return: 
        """
        # todo: кажется эта функция будет плохо работать
        for order in self.opened_orders["sell"] + self.opened_orders["buy"]:
            api.post_exchange_cancel_limit(order.symbol, order.id)

        self.opened_orders = {"sell": [], "buy": []}
        with open(get_data_dir2() + "livecoin.txt", "w") as file:
            file.write("")


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

    def update_opened_orders(self):
        """
        Функция обновляет значения в открытых ордерах
        :return: 
        """
        # todo: не очень понятно что эта функция делает
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

    def append_opened_order(self, mode, orderId):
        """
        Добавляет новый ордер в словарь
        :param mode: тип ордела(buy,sell)
        :param order: 
        :return: 
        """
        self.opened_orders[mode].append(api.get_exchange_order(orderId))

    def make_sell_orders(self, pairs_to_sell):
        """
        Выставляет ордера на продажу
        :param pairs_to_sell: 
        :return: 
        """
        for pair in pairs_to_sell:
            order = api.post_exchange_sell_limit(pair.symbol, pair.price,
                                                 pair.quantity)
            print("make_sell_order ", order)
            self.append_opened_order("sell", order.orderId)

    def make_buy_orders(self, pairs_to_buy):
        """
        Выставляет ордера на покупку
        :param pairs_to_buy: 
        :return: 
        """
        for pair in pairs_to_buy:
            order = api.post_exchange_buy_limit(pair.symbol, pair.price,
                                                pair.quantity)
            print("make_buy_order ",order)
            self.append_opened_order("buy", order.orderId)

    def get_orders(self):
        with open(get_data_dir2()+"livecoin.txt", "r") as file:
            [self.append_opened_order(row.split()[0],int(row.split()[1]))
             for row in file.readlines()]

    def set_orders(self):
        with open(get_data_dir2()+"livecoin.txt", "w") as file:
            for key in self.opened_orders.keys():
                for order in self.opened_orders[key]:
                    print order
                    file.write("{} {}\n".format(key, order.id))

    def add_to_operations(self):
        candidats = [el for el in self.DB.get_current_pairs()
                     if el.quantity == 0]
        map(lambda x: self.DB.add_to_operations(x.symbol), candidats)
