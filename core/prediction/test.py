from core.database import stockdata
from sklearn.svm import SVR
from sklearn import preprocessing, grid_search
from sklearn.metrics import mean_squared_error, mean_absolute_error, median_absolute_error
import numpy as np
import matplotlib.pyplot as plt
import pickle
import sys

sys.exit('This is too good to change. Don\'t run this.')
symbol = ''

# Get the data
link = stockdata.StockData()
splitDate = link.get_split_date(symbol)
link.sfrom(splitDate if splitDate else '2015-01-01')
link.sto('2016-05-09')
allResults = link.get_sdata(symbol)

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
parameters = {'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.1, 1]}
clf = grid_search.GridSearchCV(svr, parameters)
clf.fit(X, y)

# Predict
svr = SVR(C=clf.best_params_['C'], gamma=clf.best_params_['gamma'])
svr.fit(X, y)
ans = svr.predict(minMaxFeatures.transform(test))

with open('./../../upinkai/company_clf/'+symbol, 'wb') as file:
    pickle.dump(dict(svr=svr, minmax=minMaxPred), file)

test = [row[0] for row in test]
ansO = minMaxPred.inverse_transform(ans)
print(mean_squared_error(test, ansO), mean_absolute_error(test, ansO), median_absolute_error(test, ansO))
plt.plot(range(testSplit), test, 'blue', range(testSplit), ansO, 'red')
plt.show()
