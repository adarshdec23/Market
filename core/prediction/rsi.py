from config import rsi as rsi
from core.database import stockdata


class RSI:

    def __init__(self):
        self.rsis = []
        self.results = []

    def get_data(self, symbol):
        link = stockdata.StockData()
        results = link.get_last_n(symbol, rsi.time_period)
        self.results = tuple(reversed(results))

    def get_trend(self):
        upward, downward, uc, dc =0, 0, 0, 0
        for i in range(1, len(self.results)):
            if self.results[i][6] > self.results[i-1][6]:
                upward += self.results[i][6] - self.results[i-1][6]
                uc += 1
            else:
                downward += self.results[i-1][6] - self.results[i][6]
                dc += 1
        if uc == 0:
            uc = 1
        if dc == 0:
            dc = 1
        return [upward/uc, downward/dc]

    def get_rsi(self, symbol):
        self.get_data(symbol)
        trend = self.get_trend()
        if trend[1]:
            rs = trend[0] / trend[1]
        else:
            rs = trend[1]
        return 100 - (100/(1+rs))

    def get_all_rsi(self):
        link = stockdata.StockData()
        all_companies = link.get_all_companies()
        for row in all_companies:
            t = self.get_rsi(row[2])
            self.rsis.append([row[2],t])
        return self.rsis

    def get_med_analysis(self):
        self.get_all_rsi()
        for i, row in enumerate(self.rsis):
            if row[1] > rsi.upper_bound_high:
                self.rsis[i].append('Extremely negative outlook. Stock is overbought')
            elif row[1] > rsi.upper_bound_low:
                self.rsis[i].append('Negative outlook.')
            elif row[1] < rsi.lower_bound_low:
                self.rsis[i].append('Positive Outlook on one the company.')
            elif row[1] < rsi.lower_bound_high:
                self.rsis[i].append('An steep upward movement expected.')
            else:
                self.rsis[i].append('The stock will remain in the current range.')
        return self.rsis

e = RSI()
x = e.get_med_analysis()
for i in x:
    print(i)