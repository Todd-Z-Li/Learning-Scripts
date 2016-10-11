'''
Created on Mar 7, 2012

@author: todd.li
'''

import csv
import urllib
import simplejson
import time

url = "https://graph.facebook.com/"
query="search?q="
typ="&type=post"
limit = "&limit="
until = "&until="
pageNum=""
lim="500"

readFile=open("C:\BEB\FB\input.csv", 'rb')
readStuff=csv.reader(readFile)
readFile.close
param = []
for i in readStuff:
    print i
    param.append(i[1])
        
writeF=open("C:\BEB\FB\output.csv",'a')
writeF.write("messageID, name, id, gender, locale, message, date, application, shares, likes, # liked, who liked, id who liked \n")
writeF.close() 

global term
term=str(param[0])
global totlim
totlim=int(param[1])
if totlim < 10:
    totlim=10
#datelim=param[2]
tottCount=0

def processed(strn):
    return strn.replace("\n", " ").replace("\r"," ").replace('"', "'").encode('utf-8','ignore')

def getPage(pageUrl):
    print pageUrl
    page=urllib.urlopen(pageUrl)
    time.sleep(2)
    page2=page.read()
    pageObj= simplejson.loads(page2)
    return pageObj

def makePage(pagination):
    pageurl=url+query+term+typ+limit+lim+until+pagination
    return pageurl

def getFBUserInfo(nom):
    userPage=urllib.urlopen("https://graph.facebook.com/"+nom)
    try:
        if userPage:
            pageinfo=userPage.read()
            print pageinfo
            userPageObj=simplejson.loads(pageinfo)
            userObj=[]
            userObj.append(userPageObj["gender"])
            userObj.append(userPageObj["locale"])
            return userObj[0]+'","'+userObj[1]
        else:
            return '-1","-1'
    except:
        return '-1","-1'

def getPageNum(strn):
    splitStr=strn.split("=")
    lenStr=len(splitStr)
    pageNumm=splitStr[lenStr-1]
    print pageNumm
    return pageNumm

def writePage(pageObj, totlim):
    if pageObj["paging"] and totlim>0:
        for i in pageObj["data"]:
            if totlim>0:
                print i
                writeLine=[]
                writeLine.append(str(i["id"]))
                writeLine.append(str(processed(i["from"]["name"])))
                writeLine.append(str(i["from"]["id"]))
                writeLine.append(getFBUserInfo(str(i["from"]["id"])))
                try:
                    writeLine.append(str(processed(i["message"])))
                except:
                    writeLine.append("~")
                '''
                try:
                    writeLine.append(str(processed(i["name"])))
                except:
                    writeLine.append("~")
                try:    
                    writeLine.append(str(processed(i["link"])))
                except:
                    writeLine.append("~")
                try:
                    writeLine.append(str(processed(i["caption"])))
                except:
                    writeLine.append("~")
                try:
                    writeLine.append(str(processed(i["description"])))
                except:
                    writeLine.append("~")
                '''    
                writeLine.append(str(i["created_time"]))
                
                try:
                    writeLine.append(str(processed(i["application"]["name"])))
                except:
                    writeLine.append("~")
                try:
                    writeLine.append(str(i['shares']['count']))
                except:
                    writeLine.append("0")
                try:
                    writeLine.append(str(i['likes']['count']))
                    for l in i['likes']["data"]:
                        writeLine.append(l["name"])
                        writeLine.append(str(l["id"]))
                except:
                    writeLine.append("0")
                    
                print writeLine
                print totlim
                totlim=totlim-1
                writeFile=open("C:\BEB\FB\output.csv",'ab')
                writeFile.write('","'.join(writeLine) + '"\r\n')
                writeFile.close()     
            else:
                return 0              
        return [getPageNum(processed(pageObj["paging"]["next"])),totlim]
    else:
        return [0,0]

def main(pageNum,totlim):
    if totlim>0:
        page=getPage(makePage(pageNum))
        try:
            if len(page["data"])>0:
                pageN=writePage(page,totlim)
                if pageN[0] !=0:
                    print pageN
                    main(str(pageN[0]),pageN[1])
                else:
                    print "No More Data!"
            else:
                print "No More Pages!"
        except:
            print "no more pages!"
    else:
        print "finished!"
    
main(pageNum,totlim)

            