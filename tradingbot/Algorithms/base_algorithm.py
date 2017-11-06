import json
import os
import time

from tradingbot.ThirdParty.support import get_config_dir
from tradingbot.database import update_database


class BaseAlghoritm(object):
    def __init__(self, exchanger, decider, database, config_file):
        self._exchanger = exchanger
        self._decider = decider
        self._database = database
        self.config_file = os.path.join(get_config_dir(), config_file)
        self.set_config()

    def set_config(self):

        with open(self.config_file) as config:
            data = json.load(config)

        self._api_url = data["API_URl"]
        self._satoshi = data["SATOSHI"]
        self._number_of_pairs = data["NUMBER_OF_PAIRS"]
        self._income = data["INCOME"]
        self._max_waiting_time = data["MAX_WAITING_TIME"]
        self._commission = data["COMMISSION"]
        self._over_burse = data["OVER_BURSE"]
        self._exclusion_currency = data["EXCLUSION_CURRENCY"]
        self._period = data["PERIOD"]
       
    def close_orders(self):
        successful_orders = self._exchanger.get_successfull_orders()
        update_database(successful_orders)
        self._exchanger.close_orders()


    def buy_pairs(self):
        all_pairs = self._exchanger.get_pairs()
        current_pairs = self._exchanger.get_balances()
        pairs_to_buy = self._decider.get_solution(self, all_pairs, current_pairs)
        self._exchanger.make_buy_orders(pairs_to_buy)

    def sell_pairs(self):
        current_pairs = self._database.get_sell_pairs(self)
        self._exchanger.make_sell_orders(current_pairs)


    def run(self):
        while True:
            self.close_orders()
            self.sell_pairs()
            self.buy_pairs()
            time.sleep(self._period)

test = BaseAlghoritm("foo","bla","livecoin_config.json")
