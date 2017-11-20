from Sqlite3_API import Sqlite3

class LivecoinDB(object):

    def make_insert_request(self, order):
        values =(order.id, order.lastModificationTime, order.symbol,
                 order.quantity, order.price)
        request = """INSERT INTO Orders 
    				(id, start_time, symbol, purchased_quantity, purchase_price,
    				 sold_quantity, profit, end_time, result)
    				VALUES (%s, %s, "%s","%s","%s",0,0,0,0)"""%values

        self.set_values(request)

    def make_update_request(self, params, param_values, conditions,
                            cond_values):
        print  params, param_values, conditions, cond_values
        mask = """update Orders set %s where %s"""
        str_param = ""
        str_cond = ""

        for el in params:
            str_param += "{} = %s,".format(el)
        for el in conditions:
            str_cond += "{} %s,".format(el)

        request = mask % (str_param[:-1], str_cond[:-1]) % (
        param_values + cond_values)

        self.set_values(request)

    def make_select_request(self, params, conditions, cond_values):
        mask = """select %s from Orders where %s"""
        str_param = ""
        str_cond = ""

        for el in params:
            str_param += " {},".format(el)
        for el in conditions:
            str_cond += " {} %s and".format(el)

        request = mask % (str_param[:-1], str_cond[:-3]) % (cond_values)

        result = self.get_values(request)
        return result

    def update_orders(self,orders):
        modes = ["buy", "sell"]
        for mode in modes:
            for order in orders[mode]:
                self.make_insert_request(self, order)





