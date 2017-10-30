# -*- coding: utf-8 -*-
import support
import database
import config
import httplib
import urllib
import time
import json
import hmac
import support
import hashlib
from collections import OrderedDict
from collections import namedtuple
import livecoin_api
tmp =  livecoin_api.get_exchange_ticker()
tmp1 =  livecoin_api.get_exchange_ticker(("currencyPair","BTC/USD"))

for el in tmp:
    print el.high
print "HJH"
for el in tmp1:
    print el.high