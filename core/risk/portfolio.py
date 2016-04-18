from config import sharpe as sharpe
import csv
import numpy as np


class SharpePortfolio:
    def __init__(self):
        self.returns = []
        self.csv = None
        self.file = None
        self.filename = None

    def set_user(self, filename):
        self.filename = filename
        self.file = open('./../../data/user/'+self.filename)
        self.csv = csv.DictReader(self.file)
        self.returns = []  #Reset for next user.

    def get_buy_price(self, symbol, volume):
        copy_csv = csv.DictReader(open('./../../data/user/'+self.filename))
        for row in copy_csv:
            if row['trade_type'] == 'bought' and row['symbol'] == symbol and row['volume'] >= volume:
                return row['stock_value']
        return False

    def calculate_returns(self):
        for row in self.csv:
            if row['trade_type'] == 'sold':
                buy_price = self.get_buy_price(row['symbol'], row['volume'])
                if buy_price != False:
                    stock_return = (float(row['stock_value']) - float(buy_price)) * 100/float(buy_price)
                    self.returns.append(stock_return)

    def get_ratio(self):
        self.calculate_returns()
        np_returns = np.array(self.returns)
        std = np_returns.std()
        mean = np_returns.mean()
        sharpe_ratio = (mean - sharpe.risk_free_rate)/std
        return sharpe_ratio
