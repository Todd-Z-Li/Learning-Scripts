'''
Created on Jul 30, 2014

@author: Belly Strategy
'''


from dependents import *
from YelpSample import *

import oauth2
import datetime

#base stuff that we need to have
API_HOST = 'api.yelp.com'
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'San Francisco, CA'
SEARCH_LIMIT = 20
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'

# OAuth credential placeholders that must be filled in by users.
CONSUMER_KEY = ""
CONSUMER_SECRET = "-"
TOKEN = ""
TOKEN_SECRET = "--"


#get terms and locations
def pullYelp():
    locs=readfile("locations.csv")
    terms=readfile("types.csv")

    for l in locs:
        for t in terms:
            results=[]
            print len(l),len(t)
            if len(l) +len(t)>3:
                offset=0
                resp = search(processed(t),processed(l),offset)
                print resp
                bizs=resp.get('businesses')
                totals=resp.get('total') #don't worry about this, see comment on line 46
                if not bizs:
                    print 'No businesses for {0} in {1} found.'.format(t, l)
                else:
                    #should be offset<totals-Search_LIMIT; this section can be refined a little bit better because I will loose the up to 19 businesses if there is 59 businesses total...
                    while offset<300:
                        offset=offset+SEARCH_LIMIT #refine this here to make offset easier
                        resp2 = search(processed(t),processed(l),offset)
                        res=resp2.get('businesses')
                        if len(res)==0:
                            offset=99999
                        for r in res:
                            print processed(r["id"])
                            bizs.append(r)
                            print len(bizs)
                    for biz in bizs:
                        print processed(biz["id"])
                        appendobj=[processed(t),processed(l),processed(biz["id"]),processed(biz["name"]),processed(biz["is_closed"]),processed(biz["is_claimed"]),processed(biz["rating"]),processed(biz["review_count"])]
                        try:
                            appendobj.append(processed(biz["location"]["address"][0]))
                            appendobj.append(processed(biz["location"]["city"]))
                            appendobj.append(processed(biz["location"]["state_code"]))
                            appendobj.append(processed(biz["location"]["postal_code"]))
                        except:
                            appendobj.append("missing valid address")
                            appendobj.append("missing valid address")
                            appendobj.append("missing valid address")
                            appendobj.append("missing valid address")
                            pass
                        try:
                            appendobj.append(processed(biz["phone"]))
                        except:
                            appendobj.append("missing Phone")
                            pass
                        try:
                            appendobj.append(processed(datetime.datetime.fromtimestamp(int(biz["menu_date_updated"])).strftime('%Y-%m-%d %H:%M:%S')))
                        except:
                            appendobj.append("no menu updates")
                            pass
                        try:
                            appendobj.append(processed(biz["categories"][0]))
                        except:
                            appendobj.append(processed("no categories"))
                            pass
                        results.append(appendobj)
                writefile(results,"yelpout aug 17 2015.csv")

            else:
                print "MISSING query terms or locations"

#run program here!
pullYelp()











if __name__ == '__main__':
    pass