from config import sharpe as sharpe
import numpy as np
from core.database import stockdata


class SharpeCompany:
    def __init__(self):
        self.returns = []
        self.results = None

    def set_company(self, symbol):
        link = stockdata.StockData()
        link.sfrom('2007-01-01')
        link.sto('2016-01-20')
        self.results = link.get_sdata(symbol)
        self.returns = []  # Reset for a new comapany

    def calculate_returns(self):
        latest = self.results[-1][3]
        close_prices = []
        for i in range(1, sharpe.years_for_company):
            close_prices.append(float(self.results[-i * 250][3]))
        self.returns = [(float(latest) - old_close)*100/old_close for old_close in close_prices]

    def get_ratio(self):
        self.calculate_returns()
        np_returns = np.array(self.returns)
        std = np_returns.std()
        mean = np_returns.mean()
        sharpe_ratio = (mean - sharpe.risk_free_rate)/std
        return sharpe_ratio
