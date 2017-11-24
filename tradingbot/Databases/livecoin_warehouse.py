# -*- coding: utf-8 -*-
from Sqlite3_API import Sqlite3DB, SqLite3Table
from tradingbot.Utils.Structures import BufferPair

class BufferTable(SqLite3Table):
    """
    Класс для взаимодействия c тиблицой типа буфер 
    """
    def insert(self, order):
        base_request = self.data[self.db_name][self.table_name]["insert"]
        request = base_request.format(order.id, order.lastModificationTime,
                                      order.currencyPair, order.price,
                                      order.quantity)
        self.set_values(request)

    def select(self, pair):
        """
        
        :param pair: 
        :return: 
        """
        base_request = self.data[self.table_name]["select"]
        request = base_request.format(pair)

        return self.get_values(request)

    def delete(self, pair):
        """
        
        :param pair: 
        :return: 
        """
        base_request = self.data[self.table_name]["delete"]
        request = base_request.format(pair)
        self.set_values(request)


class OperationsTable(SqLite3Table):
    """
       Класс для взаимодействия c тиблицой типа буфер 
    """
    def insert(self, *args):
        base_request = self.data[self.table_name]["insert"]
        request = base_request.format(*args)
        self.set_values(request)

    def select(self, pair):
        base_request = self.data[self.table_name]["select"]
        request = base_request.format(pair)

        return self.get_values(request)


class LivecoinDB(Sqlite3DB):
    def __init__(self):
        Sqlite3DB.__init__(self, "livecoin")
        self.buy_table = BufferTable(self.db_name, "buy_table")
        self.sell_table = BufferTable(self.db_name, "sell_table")
        self.operations_table = OperationsTable(self.db_name,
                                                "operations_table")

    def update_orders(self, orders):
        for order in orders["buy"]:
            self.buy_table.insert(order)
        for order in orders["sell"]:
            self.sell_table.insert(order)

    def join_buy_on_sell(self):
        request = "Select symbol, count(quantity)" \
                  " from BUY_TABLE GROUP BY symbol"
        return self.buy_table.get_values(request)

    def get_payment_balances(self):
        base_request = self.data["get_payment_balances"]
        return self.get_values(base_request)

    def get_buy_pairs(self):
        #todo: исправить запрос на корректный
        base_request = self.data["get_buy_pairs"]
        return map(lambda x: BufferPair(x[0],x[1],x[2]),
                   self.get_values(base_request))

    def get_current_pairs(self):
        #todo: исправить запрос на корректный
        base_request = self.data["get_current_pairs"]
        return map(lambda x: BufferPair(x[0], x[1], x[2]),
                   self.get_values(base_request))
