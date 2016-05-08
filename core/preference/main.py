from collections import *
import numpy
fp = open('./../../data/user/user1.csv',"r")
list1 = []
list2 = []
list3 = []
list4 = []
categories = []
sold_average = []
bought_average = []
lines = fp.readlines()

for i in range(len(lines)):
    lines[i] = lines[i].strip()

for i in range(1,len(lines)):
    list1 = lines[i].split(",")
    list2.append(list1)
    list3.append(list1[3])
 
# FREQUENCY BASED APPROACH 
  
d = defaultdict(int)
for i in list3:
    d[i] += 1
result = max(iter(d.items()), key=lambda x: x[1])
print ("The most frequently traded category is %r" % result[0])
  
# STANDARD DEVIATION APPROACH
  
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
        sold_average[ind]+= int(item[5])
    else:
        bought_average[ind]+= int(item[5])
        
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
        
print (list2)
print (categories)
print (list4,sold_average,s,s_average,bought_average,b,b_average)
deviation = []
print (len(categories))
for i in range(len(categories)):
    deviation.append(s_average[i]-b_average[i])
print(deviation)
max_category = max(deviation)
print (deviation.index(max_category))
print (categories[deviation.index(max_category)])
