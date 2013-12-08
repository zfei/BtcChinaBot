__author__ = 'zfei'

from time import sleep
import pprint

from api.btccapi import BTCChina
from settings import *


pp = pprint.PrettyPrinter()


class Bot:
    def __init__(self):
        self.trader = BTCChina(API_ACCESS, API_SECRET)
        self.portfolio = []

    def get_lowest_ask(self, market_depth):
        return market_depth['market_depth']['ask'][0]['price']

    def get_highest_bid(self, market_depth):
        return market_depth['market_depth']['bid'][0]['price']

    def should_buy(self, lowest_ask, highest_bid):
        return lowest_ask - highest_bid > DIFFERENCE_STEP

    def reset(self):
        pass

    def get_num_open_bids(self, orders):
        bid_count = 0
        for order in orders:
            if order['type'] == 'bid':
                bid_count += 1

    def get_num_open_asks(self, orders):
        ask_count = 0
        for order in orders:
            if order['type'] == 'ask':
                ask_count += 1

    def get_num_portfolio_bids(self):
        bid_count = 0
        for order in self.portfolio:
            if order['status'] == 'buy':
                bid_count += 1

    def get_num_portfolio_asks(self):
        ask_count = 0
        for order in self.portfolio:
            if order['status'] == 'sell':
                ask_count += 1

    def update_portfolio(self):
        orders = self.trader.get_orders()['order']
        num_open_bids = self.get_num_open_bids()
        num_open_asks = self.get_num_open_asks()
        num_port_bids = self.get_num_portfolio_bids()
        num_port_asks = self.get_num_portfolio_asks()

    def loop_body(self):
        market_depth = self.trader.get_market_depth({'limit': 1})
        lowest_ask = self.get_highest_bid(market_depth)
        highest_bid = self.get_lowest_ask(market_depth)

        if not self.should_buy(lowest_ask, highest_bid):
            sleep(NO_GOOD_SLEEP)
            return

        my_bid_price = highest_bid + CNY_STEP
        my_ask_price = my_bid_price + MIN_SURPLUS

        for trial in xrange(MAX_TRIAL):
            if self.trader.buy(my_bid_price, BTC_AMOUNT):
                self.portfolio.append({'bid': my_bid_price, 'ask': my_ask_price, 'status': 'buy'})
                break

    def start(self):
        self.reset()
        while True:
            self.loop_body()

if __name__ == '__main__':
    bot = Bot()
    bot.start()