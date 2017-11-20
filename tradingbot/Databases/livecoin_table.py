from Sqlite3_API import Sqlite3
import json
class buy_table(Sqlite3):
    def insert(self, order):
        base_request = self.data[self.db_name][self.table_name]["insert"]
        request = base_request.format(order.id, order.lastModificationTime,
                                      order.currencyPair, order.price, order.quantity)
        self.set_values(request)

    def select(self, pair):
        base_request = self.data[self.db_name][self.table_name]["select"]
        request = base_request.format(pair)

        return self.get_values(request)

    def delete(self, pair):
        base_request = self.data[self.db_name][self.table_name]["delete"]
        request = base_request.format(pair)
        self.set_values(request)

class sell_table(Sqlite3):
    def insert(self, order):
        base_request = self.data[self.db_name][self.table_name]["insert"]
        request = base_request.format(order.id, order.lastModificationTime,
                                      order.currencyPair, order.price, order.quantity)
        self.set_values(request)

    def select(self, pair):
        base_request = self.data[self.db_name][self.table_name]["select"]
        request = base_request.format(pair)

        return self.get_values(request)

    def delete(self, pair):
        base_request = self.data[self.db_name][self.table_name]["delete"]
        request = base_request.format(pair)
        self.set_values(request)

class operations_table(Sqlite3):
    def insert(self):
        pass

    def select(self):
        pass


class LivecoinDB(object):
    def __init__(self):
        self.name = "livecoin"
        self.buy_table = buy_table(self.name)
        self.sell_table = sell_table(self.name)
        self.operations_table = operations_table(self.name)

    def update_orders(self,orders):
        for order in orders["buy"]:
            self.buy_table.insert(order)
        for order in orders["sell"]:
            self.sell_table.insert(order)

    def join_buy_on_sell(self):
        request = "Select symbol, count(quantity) from BUY_TABLE GROUP BY symbol"
        return self.buy_table.get_values(request)