from core.database import stockdata
from sklearn.svm import SVR
from sklearn import grid_search, preprocessing
from sklearn.metrics import mean_squared_error, mean_absolute_error, median_absolute_error
import numpy as np
import matplotlib.pyplot as plt


class ShortTerm:

    def __init__(self):
        minMaxFeatures = None
        minMaxPred = None

    def get_data(self, symbol, sfrom, sto):
        link = stockdata.StockData()
        link.sfrom(sfrom)
        link.sto(sto)
        return link.get_sdata(symbol)

    def preprocess(self, predictions, features):
        # Pre-processing, transform to range [-1,1]
        self.minMaxFeatures = preprocessing.MinMaxScaler((-1, 1))
        self.minMaxPred = preprocessing.MinMaxScaler((-1, 1))
        X = self.minMaxFeatures.fit_transform(features)
        y = self.minMaxPred.fit_transform(predictions)
        return X,y

    def grid_search(self, X, y):
        # Find the best parameters
        svr = SVR()
        parameters = {'C': [1, 10, 100], 'gamma': np.logspace(-3, -1, 3)}
        clf = grid_search.GridSearchCV(svr, parameters)
        clf.fit(X, y)
        return clf

    def get_prediction(self, symbol, sfrom='2013-01-01', sto='2016-01-20'):
        # Split into train and testing data
        result = self.get_data(symbol, sfrom, sto)
        # Extract required features and output values
        features = result[:-1]  # Features will be 0 to n-1
        predictions = result[1:]  # Outputs will be 1 to n
        predictions = [row[0] for row in predictions]  # Predict open price
        test = result[-1]
        X, y = self.preprocess(predictions, features)
        clf = self.grid_search(X, y)
        svr = SVR(C=clf.best_params_["C"], gamma=clf.best_params_["gamma"])
        svr.fit(X, y)
        # Predict
        ans = svr.predict(self.minMaxFeatures.transform(test))
        return self.minMaxPred.inverse_transform(ans)[0]

x = ShortTerm()
print(x.get_prediction('HDFCBANK'))
