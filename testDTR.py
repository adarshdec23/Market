from core.database import stockdata
from sklearn.tree import DecisionTreeRegressor
from sklearn import grid_search, preprocessing
from sklearn.metrics import mean_squared_error, mean_absolute_error, median_absolute_error
import numpy as np
import matplotlib.pyplot as plt

# Get the data
link = stockdata.StockData()
link.sfrom('2002-01-01')
link.sto('2016-01-20')
allResults = link.get_sdata('ITC')

# Split into train and testing data
testSplit = 250
training = allResults[:-testSplit]
test = allResults[-testSplit:]

# Extract required features and output values
X = training[:-1]  # Features will be 0 to n-1
Y = training[1:]  # Outputs will be 1 to n
# predictionsO = [row[0] for row in predictions]  # Predict open values

# Transform into numpy arrays
X = np.array(X)
Y = np.array(Y)

# Pre-processing, transform to range [-1,1]
minMax = preprocessing.MinMaxScaler((-1, 1))
minMax.fit(training)
X = minMax.transform(X)
Y = minMax.transform(Y)

# Find the best parameters
'''svr = DecisionTreeRegressor()
parameters = {'gamma': np.logspace(-3, -1, 3)}
clf = grid_search.GridSearchCV(svr, parameters)
clf.fit(X, Y)'''

# Fit to data
svr = DecisionTreeRegressor(splitter='best', random_state=1)
svr.fit(X, Y)

prediction = []
for i in range(testSplit):
    if i == 0:
        ip = minMax.transform(training[-1])
        print(training[-1])
    else:
        ip = prediction[-1]
    prediction.append(svr.predict(ip)[0])  # Predicts returns 1X6. Transform that into 1D

prediction = np.array(prediction)
# Predict

test = [row[0] for row in test]

ansO = [row[0] for row in minMax.inverse_transform(prediction)]

# Plot
plt.plot(range(testSplit), test, 'blue', range(testSplit), ansO, 'red')
plt.show()

print(mean_squared_error(test, ansO), mean_absolute_error(test, ansO), median_absolute_error(test, ansO))