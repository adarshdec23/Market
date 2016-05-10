from collections import *
from config import main
import heapq


class UserPreference:

    def __init__(self):
        self.results = []
        self.list1 = []
        self.list2 = []
        self.list3 = []
        self.list4 = []
        self.categories = []
        self.sold_average = []
        self.bought_average = []

    def get_preferences(self, user):
        # Reset all variable
        self.results = []
        self.list1 = []
        self.list2 = []
        self.list3 = []
        self.list4 = []
        self.categories = []
        self.sold_average = []
        self.bought_average = []
        self.frequency_based(user+'.csv')
        return self.results

    def frequency_based(self, user):
        fp = open(main.path+'data/user/'+user, "r")
        lines = fp.readlines()
        
        for i in range(len(lines)):
            lines[i] = lines[i].strip()
        
        for i in range(1,len(lines)):
            self.list1 = lines[i].split(",")
            self.list2.append(self.list1)
            self.list3.append(self.list1[3])
           
        d = defaultdict(int)
        for i in self.list3:
            d[i] += 1
        result = max(iter(d.items()), key=lambda x: x[1])
        self.results.append(result[0])
        self.deviation_based(result[0])
      
    # STANDARD DEVIATION APPROACH
    def deviation_based(self,freq_cat):
        for i in range(0,len(self.list2)):
            self.categories.append(self.list2[i][3])        
        self.categories = list(set(self.categories))
           
        i = 0
        for item in self.list2:
              self.list4.append(self.categories.index(item[3]))
        
        self.sold_average = [0]*len(self.categories)
        self.bought_average = [0]*len(self.categories)
        s_average = []
        b_average = []      
        s=[0]*len(self.categories)
        b=[0]*len(self.categories)
        
        for item in self.list2:
            cat = item[3]
            ind = self.categories.index(cat)
            if item[4] == 'sold':
                self.sold_average[ind]+= int(float(item[5]))
            else:
                self.bought_average[ind]+= int(float(item[5]))
                
        for x in self.list4:
                if self.list2[i][3] == self.categories[x]:
                    if self.list2[i][4] == 'sold':
                        s[x]+=1
                    if self.list2[i][4] == 'bought':
                        b[x]+=1
                i+=1
                
        for i in range(len(self.categories)):
            if s[i]!=0:
                s_average.append(self.sold_average[i]/s[i])
            else:
                s_average.append(0)        
                
        for i in range(len(self.categories)):
            if b[i]!=0:
                b_average.append(self.bought_average[i]/b[i])
            else:
                b_average.append(0)

        deviation = []
        for i in range(len(self.categories)):
            deviation.append(s_average[i]-b_average[i])

        max_category = max(deviation)
        max2_category = heapq.nlargest(2, deviation)
        if max_category == freq_cat:
            self.results.append(self.categories[deviation.index(max_category)])
        else:
            self.results.append(self.categories[deviation.index(max2_category[1])])
