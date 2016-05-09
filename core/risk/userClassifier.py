from core.risk import company, portfolio
import statistics
from sklearn import svm, grid_search
import numpy as np
from core.classifer_results import user
import pickle
from os import path


class Matcher:

    def __init__(self):
        c = company.SharpeCompany()
        if path.exists('./../../upinkai/company.pkl'):
            with open('./../../upinkai/company.pkl', 'rb') as file:
                self.company_risks = pickle.load(file)
        else:
            self.company_risks = c.get_all_company_ratios()
            with open('./../../upinkai/company.pkl', 'wb') as file:
                pickle.dump(self.company_risks, file)

    def get_sharpe_of_company(self, symbol):
        for x in self.company_risks:
            if x[2] == symbol:
                return x[5]['sharpe']

    def get_avg_sharpe(self, companies):
        sharpes = []
        for c in companies:
            c_sharpe = self.get_sharpe_of_company(c)
            sharpes.append(c_sharpe)
        return statistics.mean(sharpes)

    def get_all_attributes(self):
        attributes = []
        p = portfolio.Portfolio()
        all_portfolio = p.get_all_portfolio_ratios()
        for count, i in enumerate(all_portfolio):
            attributes.append( [ i[0], [ i[1]['positive_returns'], i[1]['negative_returns'], self.get_avg_sharpe(i[1]['companies'])] ] )
        return attributes

    def grid_search(self, X, y):
        svc = svm.SVC()
        parameters = {'gamma': np.logspace(-3, -1, 3)}
        clf = grid_search.GridSearchCV(svc, parameters)
        clf.fit(X, y)
        return clf

    def ml(self, user_list):
        attributes = self.get_all_attributes()
        train_features = []
        train_class = []
        test_features = []
        for x in attributes:
            if x[0] not in user_list:
                train_features.append(x[1])
                train_class.append(user.labels[x[0]])
            else:
                test_features.append(x[1])
        train_class = np.array(train_class)
        train_features = np.array(train_features)
        test_features = np.array(test_features)
        grid = self.grid_search(train_features, train_class)
        clf = svm.SVC(C=10, gamma=grid.best_params_['gamma'])
        clf.fit(train_features, train_class)
        return clf.predict(test_features)

    def get_user_class(self, user_name):
        if user_name in user.labels:
            return user.labels[user_name]
        return self.ml([user_name])
