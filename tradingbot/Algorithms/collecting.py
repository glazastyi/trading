# -*- coding: utf-8 -*-

from tradingbot.ThirdParty.third_party import get_data_dir2
import pandas as pd
import time
class Collecting(object):
    """Модуль для коллекционирования данных
    """
    def __init__(self, exchanger, period):
        """
        
        :param exchanger: биржа с которой собираем данные(пока одна)
        :param period: период с которым собираем
        """
        self.exchanger = exchanger
        self.period = period

    def collecting(self):
        df = pd.DataFrame(self.exchanger.get_pairs())
        df["time"] = time.ctime()
        print df.columns
        df.to_csv(get_data_dir2()+"collecting.csv", mode = "a", index = False)

    def get_data(self):
        return pd.read_csv(get_data_dir2()+"collecting.csv")

    def job(self):
        i = 0
        while True:
            print("Iteration #{}".format(i))
            self.collecting()
            i+=1
            time.sleep(self.period)