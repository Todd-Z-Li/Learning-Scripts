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
SEARCH_LIMIT = 2
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'

# OAuth credential placeholders that must be filled in by users.
CONSUMER_KEY = ""
CONSUMER_SECRET = "-"
TOKEN = "-"
TOKEN_SECRET = "-"


#get terms and locations
def pullYelp():
    bizes=readfile("ids.csv")
    for b in bizes:
        results=[]
        print b
        if len(b)>3:
            offset=0
            pString = b[:-1]
            print pString+"*"
            try:
                resp = get_business(pString)
                print resp
                categories=str(resp.get('categories'))
                rating=resp.get('rating')
                revs=resp.get('review_count')
                appendobj=[processed(b),processed(rating),processed(revs),categories]
            except:
                appendobj=[processed(b),"LOCATION NOT FOUND"]
            results.append(appendobj)
            writefile(results,"yelpBizs.csv")
        else:
            print "MISSING query terms"

#run program here!
pullYelp()











if __name__ == '__main__':
    pass