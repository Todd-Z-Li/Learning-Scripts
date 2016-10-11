'''
Created on Aug 26, 2014

@author: Belly Strategy
'''
from dependents import *

readf = open("yelps.csv","rb")

for i in readf:
    j=[]
    print i
    j.append(i)
    j.append(getMoney(i))
    writef=open("yelpdollars.csv","ab")
    writef.write(",".join(j))
    writef.write("\n")
    writef.close()

print "DONE!"