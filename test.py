from core.database import stockdata
from sklearn.svm import SVR
from sklearn import grid_search, preprocessing
import numpy as np

# Get the data
link = stockdata.StockData()
link.sfrom('2013-01-01')
link.sto('2016-01-20')
result = link.get_sdata('ITC')

# Extract required features and output values
features = result[:-1]  # Features will be 0 to n-1
predictions = result[1:]  # Outputs will be 1 to n
predictions = [row[0] for row in predictions]  # Predict open and close values

# Transform into numpy arrays
X = np.array(features)
y = np.array(predictions)

# Pre-processing, transform to range [-1,1]
minMaxFeatures = preprocessing.MinMaxScaler((-1, 1))
minMaxPred = preprocessing.MinMaxScaler((-1, 1))
X = minMaxFeatures.fit_transform(features)
y = minMaxPred.fit_transform(predictions)

# Find the best parameters
svr = SVR()
parameters = {'C': [1, 10, 100], 'gamma': np.logspace(-3, -1, 3), 'kernel': ['rbf', 'linear']}
clf = grid_search.GridSearchCV(svr, parameters)
clf.fit(X, y)

# Predict
svr = SVR(C=clf.best_params_["C"], gamma=clf.best_params_["gamma"], kernel=clf.best_params_["kernel"])
svr.fit(X, y)
ans = svr.predict(minMaxFeatures.transform(result[-1:]))
print(minMaxPred.inverse_transform(ans))
