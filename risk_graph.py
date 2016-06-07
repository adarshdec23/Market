from matplotlib import pyplot
from core.risk import userClassifier
from core.classifer_results import user

u = userClassifier.Matcher()
attribs = u.get_all_attributes()
con_x, mod_x, agg_x, con_y, mod_y, agg_y = [], [], [], [], [], []
for a in attribs:
    if user.labels[a[0]] == 'conservative':
        con_x.append(a[1][1])
        con_y.append(a[1][2])
    elif user.labels[a[0]] == 'moderate':
        mod_x.append(a[1][1])
        mod_y.append(a[1][2])
    elif user.labels[a[0]] == 'aggressive':
        agg_x.append(a[1][1])
        agg_y.append(a[1][2])

low = pyplot.scatter(x=con_x, y=con_y, c='green', marker='>')
moderate = pyplot.scatter(x=mod_x, y=mod_y, c='white', marker='^')
high = pyplot.scatter(x=agg_x, y=agg_y, c='yellow')
pyplot.legend([low, moderate, high], ["Low Risk", "Moderate Risk", "High Risk"])
pyplot.xlabel("Negative Returns")
pyplot.ylabel("Sharpe Ratio")
pyplot.show()
