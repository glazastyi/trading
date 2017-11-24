# -*- coding: utf-8 -*-
import json
import os
import time

from tradingbot.ThirdParty.third_party import get_config_dir


class BaseAlghoritm(object):
    """Это базовый алгоритм торговли на криптовалютных биржах
    """
    def __init__(self, exchanger, decider, config_file):
        """
        Инициализация параметров алгоритма
        :param exchanger: Биржа на которой торгует данный алгоритм
        :param decider: Модуль который принимает решения
        :param config_file: конфигурационный файл
        """
        self._exchanger = exchanger

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
        self._start_pair = data["START_PAIR"]

        self._decider = decider(self._exclusion_currency, self._commission,
                                self._number_of_pairs, 100 * self._satoshi,
                                self._start_pair, self._income)

    def close_orders(self):
        """
        Функция закрытия открытых на бирже ордеров
        :return: None
        """
        self._exchanger.update_orders()
        self._exchanger.close_orders()

    def buy_pairs(self):
        """
        Функция с помощью модуля принятия решений вычисляет наиболее выгодные
        для покупки валютные пары и выставляет ордера на их покупку 
        :return: None
        """
        all_pairs = self._exchanger.get_pairs()
        balance = self._exchanger.get_btc_balance()
        current_pairs = self._exchanger.get_current_pairs()

        pairs_to_buy = self._decider.get_buy_solution(balance,
                                                      all_pairs, current_pairs)

        self._exchanger.make_buy_orders(pairs_to_buy)

    def sell_pairs(self):
        """
        Функция с помощью модуля принятия решений вычисляет валютные пары
        пригодные для продажи и выставляет ордера на их продажу 
        :return: 
        """
        current_pairs = self._exchanger.get_current_pairs()
        pairs_to_sell = self._decider.get_sell_solution(current_pairs)
        self._exchanger.make_sell_orders(pairs_to_sell)

    def run(self):
        """
        Работа алгоритма
        :return: 
        """
        while True:
            self.close_orders()
            self.sell_pairs()
            self.buy_pairs()
            time.sleep(self._period)
