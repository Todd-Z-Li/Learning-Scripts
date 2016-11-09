'''
Created on Aug 26, 2014

@author: Belly Strategy
'''
import urllib
from bs4 import *
from dependents import *

counter=1
url="https://www.uschamber.com/chamber/directory?title=&province=All&page="

def getEm(yurl):
    conn= urllib.urlopen(yurl)
    soup = BeautifulSoup(conn.read())
    emails = soup.find_all(class_='email')
    names= soup.find_all('h4')
    print emails
    return [emails,names]


while counter <77:
    writef=open("chambs2.csv","ab")
    furl=url+str(counter)
    res=getEm(furl)
    i=0
    while i < len(res[0]):
        print res[0][i]
        try:
            writef.write(processed(res[1][i].string))
        except:
            writef.write("N/A")
        writef.write(",")
        writef.write(res[0][i].span.a.string)
        writef.write("\n")
        i=i+1
    counter=counter+1