'''
Created on Jul 29, 2014

@author: Todd
'''
import urllib
import json
import urllib2
from dependents import *

#actual program doesn't start until the end; the top is prep work!


def srchplaceswhere(what,type1,where,page,rpp,sort,rformat,placement,hasoffers,histograms,i,publishercode):

    qStr = {'publisher':publishercode, 'sort':"dist", 'page':page, 'rpp':rpp}

    url = "http://api.citygridmedia.com/content/places/v2/search/where?"

    if len(what) > 0:
        qStr['what'] = what
    if len(type1) > 0:
        qStr['type'] = type1
    if len(where) > 0:
        qStr['where'] = where

    qStr['i'] = 0

    qStr['format'] = rformat

    url += urllib.urlencode(qStr)
    print url

    response = urllib2.urlopen( url ).read()

    return response

def query(what,type1,where,page,rpp,sort,rformat,placement,has_offers,histograms,i,publishercode):
    cont=0
    arrayResult=[]
    while cont==0:
        response = srchplaceswhere(what,type1,where,page,rpp,sort,rformat,placement,has_offers,histograms,i,publishercode)

        pResponse = json.loads(response)
        print pResponse
        data = dict(json.loads(json.dumps(pResponse)))
        results = dict(json.loads(json.dumps(data[u'results'])))
        for locations in results[u'locations']:

            location = dict(json.loads(json.dumps(locations)))
            place=[]


            #featured = location[u'featured']
            public_id = location[u'public_id']
            bid = location[u'id']
            name = location[u'name']

            addressblock = location[u'address']
            address = dict(json.loads(json.dumps(addressblock)))
            city = address[u'city']
            state = address[u'state']
            street = address[u'street']
            postal_code = address[u'postal_code']

            neighborhood = location[u'neighborhood']
            latitude = location[u'latitude']
            longitude = location[u'longitude']
            #distance = location[u'distance']
            #image = location[u'image']
            phone_number = location[u'phone_number']
            #fax_number = location[u'fax_number']
            rating = location[u'rating']
            reviews = location[u'user_review_count']
            #profile = location[u'profile']
            website = location[u'website']
            #has_video = location[u'has_video']
            has_offers = location[u'has_offers']
            #offers = location[u'offers']
            tagBlock=location[u'tags']
            tags = str(tagBlock)
            bizops= location[u'business_operation_status']

            sample_categories = location[u'sample_categories']
            #impression_id = location[u'impression_id']
            #expansion  = location[u'expansion']
            place=[processed(what),processed(where),processed(bid),processed(public_id),processed(name),processed(phone_number),processed(street),processed(city),processed(state),processed(postal_code),processed(bizops),processed(latitude),processed(longitude),processed(website),processed(has_offers),processed(reviews),processed(rating),processed(neighborhood),processed(sample_categories),processed(tags)]
            arrayResult.append(place)

        if results[u'last_hit'] < results[u'total_hits']:
            print "page number: ", page
            page=page+1
            cont=0
        else:
            cont=1
    writefile(arrayResult,"outfile.csv")
    return len(arrayResult)


#here is where the program actually starts
def CityGrid():
    regions=readfile("locations.csv")
    AllTypes=readfile("types.csv")
    counter=0
    for r in regions:
        for w in AllTypes:
            #set limit for api call (daily limit is 25000 for CityGrid/CitySearch)
            if counter <=23000:
                massResult=query(w,"",r,1,50,"dist","json","","","",0,"10000005967")
                #writefile(massResult,"outfile.csv")
                counter=counter+(massResult)/50
                print counter
            else:
                break

#run the program!
CityGrid()

if __name__ == '__main__':
    pass