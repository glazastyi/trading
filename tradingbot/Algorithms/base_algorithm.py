# -*- coding: utf-8 -*-
import json
import os
import time

from tradingbot.ThirdParty.third_party import get_config_dir


class BaseAlghoritm(object):
    def __init__(self, exchanger, decider, config_file):
        self._exchanger = exchanger
        self._decider = decider
        self.config_file = os.path.join(get_config_dir(), config_file)

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
        self._exchanger.update_orders()
        self._exchanger.close_orders()

    def buy_pairs(self):
        all_pairs = self._exchanger.get_pairs()
        balance = self._exchanger.get_btc_balance()
        current_pairs = self._exchanger.get_current_pairs()

        pairs_to_buy = self._decider.get_solution(balance,
                                                  all_pairs, current_pairs,
                                                  self._exclusion_currency)

        self._exchanger.make_buy_orders(pairs_to_buy)

    def sell_pairs(self):
        current_pairs = self._exchanger.get_sell_pairs()
        self._exchanger.make_sell_orders(current_pairs)

    def run(self):
        while True:
            self.close_orders()
            self.sell_pairs()
            self.buy_pairs()
            time.sleep(self._period)
