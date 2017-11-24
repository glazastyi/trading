# -*- coding: utf-8 -*-
from Sqlite3_API import Sqlite3DB, SqLite3Table
from tradingbot.Utils.Structures import BufferPair


class BufferTable(SqLite3Table):
    """
    Класс для взаимодействия c таблицой типа буфер 
    """

    def insert(self, order):
        """
        Производит Insert запрос 
        :param order: 
        :return: 
        """
        base_request = self.data[self.db_name][self.table_name]["insert"]
        request = base_request.format(order.id, order.lastModificationTime,
                                      order.currencyPair, order.price,
                                      order.quantity)
        self.set_values(request)

    def select(self, pair):
        """
        Производит  select запрос к бд
        :param pair: 
        :return: 
        """
        base_request = self.data[self.table_name]["select"]
        request = base_request.format(pair)

        return self.get_values(request)

    def delete(self, pair):
        """
        Функция удаляет значение из таблицы
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
        """
        Функция вставки в таблицу с проведенными операциями
        :param args: 
        :return: 
        """
        base_request = self.data[self.table_name]["insert"]
        request = base_request.format(*args)
        self.set_values(request)

    def select(self, pair):
        """
        Функция выбора из таблицы с результатами
        :param pair: 
        :return: 
        """
        base_request = self.data[self.table_name]["select"]
        request = base_request.format(pair)

        return self.get_values(request)


class LivecoinDB(Sqlite3DB):
    """Класс для взаимодействия с хранилищем livecoin
    """

    def __init__(self):
        """
        Производится инициализация следующих таблиц:
        buy_table - таблица операциями покупки
        sell_table - таблица с операциями продажи
        operations_table - после того как для как значения в таблицах
            buy_table и sell_table сходятся в таблицу operations_table 
            записывается новая позици
        """
        Sqlite3DB.__init__(self, "livecoin")
        self.buy_table = BufferTable(self.db_name, "buy_table")
        self.sell_table = BufferTable(self.db_name, "sell_table")
        self.operations_table = OperationsTable(self.db_name,
                                                "operations_table")

    def update_orders(self, orders):
        """
        Функция обновления таблиц исходя из новых ордеров
        :param orders: 
        :return: 
        """
        # todo: дописать функцию
        for order in orders["buy"]:
            self.buy_table.insert(order)
        for order in orders["sell"]:
            self.sell_table.insert(order)

    def join_buy_on_sell(self):
        # todo: дописать функцию
        request = "Select symbol, count(quantity)" \
                  " from BUY_TABLE GROUP BY symbol"
        return self.buy_table.get_values(request)

    def get_payment_balances(self):
        """
        получение информации о текущих баланса валют
        :return: 
        """
        base_request = self.data["get_payment_balances"]
        return self.get_values(base_request)

    def get_buy_pairs(self):
        """
        Получение значений о парах
        :return: 
        """
        # todo: исправить запрос на корректный
        base_request = self.data["get_buy_pairs"]
        return map(lambda x: BufferPair(x[0], x[1], x[2]),
                   self.get_values(base_request))

    def get_current_pairs(self):
        """
               Получение значений о парах
               :return: 
               """
        # todo: исправить запрос на корректный
        base_request = self.data["get_current_pairs"]
        return map(lambda x: BufferPair(x[0], x[1], x[2]),
                   self.get_values(base_request))
