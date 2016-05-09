from core.database import stockdata
from sklearn.svm import SVR
from sklearn import grid_search, preprocessing
from sklearn.metrics import mean_squared_error, mean_absolute_error, median_absolute_error
import numpy as np
import matplotlib.pyplot as plt


class ShortTerm:

# Get the data
link = stockdata.StockData()
link.sfrom('2013-01-01')
link.sto('2016-01-20')
allResults = link.get_sdata('ITC')

# Split into train and testing data
testSplit = 150
result = allResults[:testSplit]
test = allResults[-testSplit:]

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
ans = svr.predict(minMaxFeatures.transform(test))
# print(minMaxPred.inverse_transform(ans))
test = [row[0] for row in test]
print(clf.best_params_["gamma"], clf.best_params_["C"], clf.best_params_["kernel"])
ansO = minMaxPred.inverse_transform(ans)
print(mean_squared_error(test, ansO), mean_absolute_error(test, ansO), median_absolute_error(test, ansO))
plt.plot(range(testSplit), test, 'blue', range(testSplit), ansO, 'red')
plt.show()
