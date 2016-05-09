from collections import *
from config import main
list1 = []
list2 = []
list3 = []
list4 = []
categories = []
sold_average = []
bought_average = []


class UserPreference:

    def __init__(self):
        self.results = []

    def get_preferences(self, user):
        self.frequency_based(user+'.csv')
        return self.results

    def frequency_based(self, user):
        fp = open(main.path+'data/user/'+user, "r")
        lines = fp.readlines()
        
        for i in range(len(lines)):
            lines[i] = lines[i].strip()
        
        for i in range(1,len(lines)):
            list1 = lines[i].split(",")
            list2.append(list1)
            list3.append(list1[3])
           
        d = defaultdict(int)
        for i in list3:
            d[i] += 1
        result = max(iter(d.items()), key=lambda x: x[1])
        self.results.append(result[0])
        self.deviation_based()
      
    # STANDARD DEVIATION APPROACH
    def deviation_based(self):
        global categories
        for i in range(0,len(list2)):
            categories.append(list2[i][3])        
        categories = list(set(categories))
           
        i = 0
        for item in list2:
              list4.append(categories.index(item[3]))
        
        sold_average = [0]*len(categories)
        bought_average = [0]*len(categories)
        s_average = []
        b_average = []      
        s=[0]*len(categories)
        b=[0]*len(categories)
        
        for item in list2:
            cat = item[3]
            ind = categories.index(cat)
            if item[4] == 'sold':
                sold_average[ind]+= int(float(item[5]))
            else:
                bought_average[ind]+= int(float(item[5]))
                
        for x in list4:
                if list2[i][3] == categories[x]:
                    if list2[i][4] == 'sold':
                        s[x]+=1
                    if list2[i][4] == 'bought':
                        b[x]+=1
                i+=1
                
        for i in range(len(categories)):
            if s[i]!=0:
                s_average.append(sold_average[i]/s[i])
            else:
                s_average.append(0)        
                
        for i in range(len(categories)):
            if b[i]!=0:
                b_average.append(bought_average[i]/b[i])
            else:
                b_average.append(0)

        deviation = []
        for i in range(len(categories)):
            deviation.append(s_average[i]-b_average[i])

        max_category = max(deviation)
        self.results.append(categories[deviation.index(max_category)])
