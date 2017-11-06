import tradingbot.ExchangersAPI.livecoin_api as api


class LivecoinExchanger(object):
    def __init__(self):
        self.opened_orders = {"sell":[], "buy":[]}
        self.da
    def get_pairs(self):
        return api.get_exchange_ticker()

    def get_balances(self):
        return api.get_payment_balances()

    def get_opened_orders(self):
        return self.opened_orders

    def close_orders(self):
        for order in self.opened_orders:
            api.post_exchange_cancel_limit(order.symbol, order.id)

    def get_successfull_orders(self,):
        result = []
        for order in self.opened_orders:
            if order.remaining_quantity != order.quantity:
                result.append(order)

        return result

    def append_opened_order(self,type,order):
        self.opened_orders[type].append(api.get_exchange_order(order))

    def make_sell_order(self):
        pass

    def make_buy_orders(self,pairs_to_buy):
        for pair in pairs_to_buy:
            order = api.post_exchange_buy_limit(pair.symbol, pair.price,
                                          pair.quantity)
            self.append_opened_order("buy", order)


