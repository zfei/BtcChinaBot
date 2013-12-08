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
        self.profit = 0

    def get_lowest_market_ask(self, market_depth):
        return market_depth['market_depth']['ask'][0]['price']

    def get_highest_market_bid(self, market_depth):
        return market_depth['market_depth']['bid'][0]['price']

    def should_buy(self, lowest_ask, highest_bid):
        return lowest_ask - highest_bid > DIFFERENCE_STEP

    def reset(self):
        pass

    def get_market_depth(self):
        market_depth = None

        for trial in xrange(MAX_TRIAL):
            market_depth = self.trader.get_market_depth({'limit': 1})
            if market_depth:
                break

        return market_depth

    def get_num_open_bids(self, orders):
        bid_count = 0
        for order in orders:
            if order['type'] == 'bid':
                bid_count += 1
        return bid_count

    def get_num_open_asks(self, orders):
        ask_count = 0
        for order in orders:
            if order['type'] == 'ask':
                ask_count += 1
        return ask_count

    def get_num_portfolio_bids(self):
        bid_count = 0
        for order in self.portfolio:
            if order['status'] == 'buy':
                bid_count += 1
        return bid_count

    def get_num_portfolio_asks(self):
        ask_count = 0
        for order in self.portfolio:
            if order['status'] == 'sell':
                ask_count += 1
        return ask_count

    def get_highest_bid(self):
        highest_bid = None
        highest_bid_price = -1
        for order in self.portfolio:
            if order['status'] == 'buy' and order['bid'] > highest_bid_price:
                highest_bid_price = order['bid']
                highest_bid = order
        return highest_bid

    def get_lowest_ask(self):
        lowest_ask = None
        lowest_ask_price = float('inf')
        for order in self.portfolio:
            if order['status'] == 'sell' and order['ask'] < lowest_ask_price:
                lowest_ask_price = order['ask']
                lowest_ask = order
        return lowest_ask

    def highest_bid_filled(self):
        highest_bid = self.get_highest_bid()

        if not highest_bid:
            return

        if DEBUG_MODE:
            print '---'
            print 'Attempting to sell at', highest_bid['ask']

        for trial in xrange(MAX_TRIAL):
            if self.trader.sell(highest_bid['ask'], BTC_AMOUNT):
                highest_bid['status'] = 'sell'

                if DEBUG_MODE:
                    print 'Bid at', highest_bid['bid'], 'filled'
                    print 'will sell at', highest_bid['ask']

                break

    def lowest_ask_filled(self):
        lowest_ask = self.get_lowest_ask()

        if not lowest_ask:
            return

        self.profit += (lowest_ask['ask'] - lowest_ask['bid']) * BTC_AMOUNT
        self.portfolio.remove(lowest_ask)

        if DEBUG_MODE:
            print '---'
            print 'Ask at', lowest_ask['ask'],'filled, bought at', lowest_ask['bid']
            print 'current profit:', self.profit

    def update_portfolio(self):
        orders = None

        if DEBUG_MODE:
            print '---'
            print 'Attempting to get orders'

        for trial in xrange(MAX_TRIAL):
            orders = self.trader.get_orders()['order']
            if not orders is None:
                break

        if orders is None:
            return

        num_open_bids = self.get_num_open_bids(orders)
        num_open_asks = self.get_num_open_asks(orders)
        num_port_bids = self.get_num_portfolio_bids()
        num_port_asks = self.get_num_portfolio_asks()

        for num_asks_filled in xrange(num_port_asks - num_open_asks):
            self.lowest_ask_filled()

        for num_bids_filled in xrange(num_port_bids - num_open_bids):
            self.highest_bid_filled()

        # remove unrealistic bids
        # NO GOOD NO GOOD
        if REMOVE_UNREALISTIC:
            market_depth = self.get_market_depth()
            if market_depth is None:
                return

            my_highest_bid = self.get_highest_bid()
            if not my_highest_bid:
                return

            market_highest_bid_price = self.get_highest_market_bid(market_depth)
            if market_highest_bid_price - my_highest_bid['bid'] > REMOVE_THRESHOLD:
                self.portfolio.remove(my_highest_bid)
                # TODO: actually cancel the order

    def loop_body(self):
        self.update_portfolio()

        if len(self.portfolio) >= MAX_OPEN_ORDERS:
            if DEBUG_MODE:
                print '---'
                print 'Too many open orders, sleep for', TOO_MANY_OPEN_SLEEP, 'seconds.'

            sleep(TOO_MANY_OPEN_SLEEP)
            return
        else:
            if DEBUG_MODE:
                print '---'
                print 'I have', self.get_num_portfolio_bids(), 'open bids,', self.get_num_portfolio_asks(), 'asks.'

        market_depth = self.get_market_depth()
        if not market_depth:
            return

        highest_bid = self.get_highest_market_bid(market_depth)
        lowest_ask = self.get_lowest_market_ask(market_depth)

        if not self.should_buy(lowest_ask, highest_bid):
            if DEBUG_MODE:
                print '---'
                print 'Market spread:', str(lowest_ask - highest_bid)
                print 'Nothing interesting, sleep for', NO_GOOD_SLEEP, 'seconds.'

            sleep(NO_GOOD_SLEEP)
            return

        my_bid_price = '{0:.2f}'.format(highest_bid + CNY_STEP)
        my_ask_price = '{0:.2f}'.format(my_bid_price + MIN_SURPLUS)

        if DEBUG_MODE:
            print '---'
            print 'Attempting to bid at', my_bid_price

        for trial in xrange(MAX_TRIAL):
            if self.trader.buy(my_bid_price, BTC_AMOUNT):
                if DEBUG_MODE:
                    print 'I ordered', BTC_AMOUNT, 'bitcoins at', my_bid_price
                    print 'will sell at', my_ask_price

                self.portfolio.append({'bid': my_bid_price, 'ask': my_ask_price, 'status': 'buy'})
                break

    def start(self):
        self.reset()
        while True:
            self.loop_body()

if __name__ == '__main__':
    bot = Bot()
    bot.start()