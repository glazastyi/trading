import sqlite3
import json
from tradingbot.ThirdParty.support import get_data_dir
class Sqlite3(object):

    def __init__(self,description):
        self.way = get_data_dir()
        #todo: создание таблицы
        #self.create_table(self,description)

    def set_values(self, request):
        con = sqlite3.connect(self.way)
        cur = con.cursor()
        cur.execute(request)
        con.commit()
        con.close()

    def get_values(self, request):
        con = sqlite3.connect(self.way)
        cur = con.cursor()
        cur.execute(request)
        result = cur.fetchall()
        con.commit()
        con.close()

        return result

    def create_table(self, description):
        with open(description) as config:
            data = json.load(config)
        create_request = data[description]

        self.set_values(create_request)

