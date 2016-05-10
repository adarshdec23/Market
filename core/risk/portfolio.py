from config import sharpe as sharpe
import csv
import numpy as np
import os
import statistics
from config import main


class Portfolio:
    def __init__(self):
        self.csv = None
        self.file = None
        self.filename = None
        self.positive_returns = []
        self.negative_returns = []

    def set_user(self, filename):
        self.filename = filename
        self.file = open(main.path+'data/user/'+self.filename)
        self.csv = csv.DictReader(self.file)
        self.positive_returns = []
        self.negative_returns = []

    def get_buy_price(self, symbol, volume):
        copy_csv = csv.DictReader(open(main.path+'data/user/'+self.filename))
        for row in copy_csv:
            if row['trade_type'] == 'bought' and row['symbol'] == symbol:
                return row['stock_value']
        return False

    def get_returns(self):
        returns = []
        for row in self.csv:
            if row['trade_type'] == 'sold':
                buy_price = self.get_buy_price(row['symbol'], row['volume'])
                if buy_price:
                    stock_return = (float(row['stock_value']) - float(buy_price)) * 100/float(buy_price)
                    if stock_return < 0:
                        self.negative_returns.append(stock_return)
                    else:
                        self.positive_returns.append(stock_return)
                    returns.append(stock_return)
        return returns

    def get_companies(self):
        companies = []
        copy_csv = csv.DictReader(open(main.path+'data/user/'+self.filename))
        for row in copy_csv:
            if row['symbol'] not in companies:
                companies.append(row['symbol'])
        return companies

    def get_ratio(self):
        np_returns = np.array(self.get_returns())
        std = np_returns.std()
        mean = np_returns.mean()
        sharpe_ratio = (mean - sharpe.risk_free_rate)/std
        if len(self.positive_returns):
            mean_positive = statistics.mean(self.positive_returns)
        else:
            mean_positive = 0
        if len(self.negative_returns):
            mean_negative = statistics.mean(self.negative_returns)
        else:
            mean_negative = 0
        return dict(
            sharpe=sharpe_ratio,
            mean=mean,
            std=std,
            count=len(np_returns),
            positive_returns=mean_positive,
            negative_returns=mean_negative,
            companies=self.get_companies()
        )

    def get_all_portfolio_ratios(self):
        all_ratios = []
        for user in os.listdir(main.path+'data/user'):
            if user == '__init__.py':
                continue
            self.set_user(user)
            all_ratios.append([user[:-4], self.get_ratio()])  # Remove '.csv' part
        return all_ratios
