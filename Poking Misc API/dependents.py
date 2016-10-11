'''
Created on Jul 30, 2014

@author: Belly Strategy
'''
import urllib
from bs4 import *
import time
import random

def processed(stn):
    try:
        strn=str(stn)
        return strn.replace("\n", " ").replace("\r"," ").replace(',', ";").encode('utf-8','ignore')
    except:
        return "-"

#read files that contain things and put each line into an array
def readfile(fileName):
    locFile= open(fileName,"r")
    locLines=locFile.readlines()
    locs=[]
    for i in locLines:
        locs.append(i)
    locFile.close()
    return locs

#putting this here: write file function
def writefile(obj,export):
    writef=open(export,"ab")
    for o in obj:
        stuff=",".join(o)
        stuff=stuff+"\n"
        print stuff
        writef.writelines(stuff)
    writef.close()


#build string to CityData
#url, publisher ID, and format is set already (inside function)
def URLbuild(type1,where,pageNum):
    t="&type="&type1
    w="&where="&where
    p="&page="&pageNum
    baseURL="http://api.citygridmedia.com/content/places/v2/search/where?publisher=10000005967&format=json&"
    fullURL=baseURL&t&w&p
    print fullURL
    return fullURL


def getMoney(yurl):
    time.sleep(1+random.randint(1,2))
    conn= urllib.urlopen(yurl)
    soup = BeautifulSoup(conn.read())
    moneySign = soup.find(itemprop='priceRange')
    print moneySign
    monay= moneySign.string
    return monay