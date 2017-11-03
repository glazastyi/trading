class BaseAlghoritm(object):
    def __init__(self, exchanger, decider):
        self.exchanger = exchanger
        self.decider = decider

    def set_config(self):
        pass

    def close_orders(self):
        pass

    def buy_pairs(self):
        pass

    def sell_pairs(self):
        pass

    def run(self):
        pass
