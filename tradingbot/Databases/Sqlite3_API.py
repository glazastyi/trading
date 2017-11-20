import sqlite3
import json
from tradingbot.ThirdParty.third_party import get_data_dir, get_config_dir
class Sqlite3(object):
    def __init__(self, db_name):
        self.db_name = db_name
        self.config = "/".join([get_config_dir(),"DB_tables_description.json"])
        self.way = get_data_dir(self.db_name)
        self.table_name = type(self).__name__

        with open(self.config) as config:
            self.data = json.load(config)

        try:
            self.create_table()
        except BaseException:
            print "Table already Exist"

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

    def create_table(self):
        with open(self.config) as config:
            data = json.load(config)
        create_request = data[self.db_name][self.table_name]["create"]
        self.set_values(create_request)

