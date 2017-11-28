from tradingbot.Algorithms.collecting import Collecting
from tradingbot.Exchangers.livecoin_exchanger import LivecoinExchanger
tmp = Collecting(LivecoinExchanger(), 60)
tmp.job()
