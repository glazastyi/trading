import unittest
from tradingbot.livecoin_api import get_exchange_ticker


class TestLivecoinApi(unittest.TestCase):

    def test_get_exchange_ticker(self):
        self.assertGreater(len(get_exchange_ticker()), 0)
