from core.database import stockdata
from sklearn.svm import SVR
from sklearn import grid_search, preprocessing
from sklearn.metrics import mean_squared_error, mean_absolute_error, median_absolute_error
import numpy as np
import matplotlib.pyplot as plt
import pickle


class Test:

    testSplit = 150

    def __init__(self):
        self.minMaxFeatures = None
        self.minMaxPred = None

    def get_data(self, symbol, sfrom, sto):
        link = stockdata.StockData()
        split_date = link.get_split_date(symbol)
        link.sfrom(split_date if split_date else sfrom)
        link.sto(sto)
        return link.get_sdata(symbol)

    def pre_process(self, predictions, features):
        # Transform into numpy arrays
        X = np.array(features)
        y = np.array(predictions)

        # Pre-processing, transform to range [-1,1]
        self.minMaxFeatures = preprocessing.MinMaxScaler((-1, 1))
        self.minMaxPred = preprocessing.MinMaxScaler((-1, 1))
        X = self.minMaxFeatures.fit_transform(features)
        y = self.minMaxPred.fit_transform(predictions)
        return X, y

    def grid_search(self, X, y):
        # Find the best parameters
        svr = SVR()
        parameters = {'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.1, 1]}
        clf = grid_search.GridSearchCV(svr, parameters)
        clf.fit(X, y)
        return clf

    # def save_clf(self, svr, symbol):
    #     with open('./../../upinkai/company_clf/'+symbol, 'wb') as file:
    #         pickle.dump(dict(svr=svr, minmax=self.minMaxPred), file)

    def plot_debug(self, test, ans0):
        print(mean_squared_error(test, ans0), mean_absolute_error(test, ans0), median_absolute_error(test, ans0))
        plt.plot(range(Test.testSplit), test, 'blue', range(Test.testSplit), ans0, 'red')
        plt.show()

    def get_prediction(self, symbol, sfrom='2013-01-01', sto='2016-05-09'):
        # Split into train and testing data
        allResults = self.get_data(symbol, sfrom, sto)
        # Extract required features and output values
        # Split into train and testing data
        result = allResults[:Test.testSplit]
        test = allResults[-Test.testSplit:]

        # Extract required features and output values
        features = result[:-1]  # Features will be 0 to n-1
        predictions = result[1:]  # Outputs will be 1 to n
        predictions = [row[0] for row in predictions]  # Predict open and close values

        X, y = self.preprocess(predictions, features)
        clf = self.grid_search(X, y)

        svr = SVR(C=clf.best_params_["C"], gamma=clf.best_params_["gamma"])
        svr.fit(X, y)
        # Predict
        ans = svr.predict(self.minMaxFeatures.transform(test))
        ans0 = self.minMaxPred.inverse_transform(ans)
        self.plot_debug(test, ans0)
        # self.save_clf(svr, symbol)
        return self.minMaxPred.inverse_transform(ans0)
