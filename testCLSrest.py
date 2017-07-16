
import os
import sys

# This exception class is raised whenever we detect an error

class ValidationError(Exception):
    def __init__(self, msg):
        self.msg = "ERROR: %s" % msg
    def __str__(self):
        return self.msg
        
def msg(msg):
    print "%s:%s" % (os.path.basename(__file__),msg)

def wrongType(var,expected,actual):
    raise ValidationError("%s should be %s not %s" % (var,expected,actual))

def checkType(varName,varValue,expected):
    msg("Validating data type of %s" % varName);
    if type(varValue) != type(expected):
        raise ValidationError("%s should be %s not %s" % (varName,type(expected),type(varValue)))

def keyIssue(issue,key,keySet):
    raise ValidationError("%s key %s from %s" % (issue,key,keySet))

def validateKeys(keySet,keysPresent,keysExpected):
    msg("Validating %s keys of %s" % (keySet,keysExpected))

    # First make sure that any key present is expected
    for key in keysPresent:
        if key not in keysExpected:
            keyIssue("unexpected", key,keySet)
    
    # Now make sure that all the keys expected are present
    for key in keysExpected:
        if key not in keysPresent:
            keyIssue("missing", key,keySet)

def validateCommonReplyData(reply, api):

    msg("Validating common reply data in [%s] API call ..." % api)
    
    checkType("reply", reply, {})
    validateKeys("common primary keys", reply.keys(), ['dbgObj','apiVer','apiObj'])
    
    dbgObj = reply['dbgObj']
    checkType("dbgObj", dbgObj, {})
    validateKeys("dbgObj keys", dbgObj.keys(), ['query_string', 'restAPIkeys','parseOK', 'traceMsgQ', 'request_uri'])
    
    apiVer = reply['apiVer']
    checkType("apiVer", apiVer, {})
    validateKeys("apiDataVersion keys", apiVer.keys(), ['apiDataVersion', 'apiVersion','apiName'])

    apiObj = reply['apiObj']
    checkType("apiObj", apiObj, {})
    
def validateReelReplyData(apiObj, api):

    msg("Validating API specific data for [%s] API call ..." % api)
    
    validateKeys("%s apiObj keys" % api, apiObj.keys(), ['reelList','numReels'])
    
    reelList = apiObj['reelList']
    checkType("apiObj['reelList']", reelList, [])

    count = 0
    for reelx in reelList:
        checkType("reelList[%d]" % count,reelx,{});
        expectedKeys = ['url', 'sUrl','thumb','frame','title']
        validateKeys("apiList[%d]" % count, reelx.keys(), expectedKeys)
        for rkey in expectedKeys:
            checkType("apiList[%d]['%s']" % (count,rkey), reelx[rkey], u"")
        
        count = count + 1
    
    numReels = apiObj['numReels']
    checkType("apiObj['numReels']", numReels, 0)
    
    msg("Validating count of reels in reelList");
    reels = apiObj['reelList']
    if numReels != len(reels): raise ValidationError("Expected %d reels in reelList but got %d instead" % (numReels,len(reels)))

    msg("[%s] has returned a valid API object\r\n" % api)

def validateAboutUsReplyData(apiObj, api):

    msg("Validating API specific data for [%s] API call ..." % api)
    
    validateKeys("%s apiObj keys" % api, apiObj.keys(), ['aboutus'])
    
    msg("[%s] has returned a valid API object\r\n" % api)

def validateContactInfoReplyData(apiObj, api):

    msg("Validating API specific data for [%s] API call ..." % api)
    
    validateKeys("%s apiObj keys" % api, apiObj.keys(), ['location','address','email','phone','socialNetworks'])
    
    checkType("apiObj['location']", apiObj['location'], u"")

    address = apiObj['address']
    checkType("apiObj['address']", address, {})
    expectedKeys = ['name', 'street','city','state','zipcode']
    validateKeys("address keys", address.keys(), expectedKeys)
    for rkey in expectedKeys:
        checkType("apiObj[address]['%s']" % rkey, address[rkey], u"")
    
    checkType("apiObj['email']", apiObj['email'], u"")
    checkType("apiObj['phone']", apiObj['phone'], u"")

    msg("Validating data type of socialNetworks");
    socialNetworks = apiObj['socialNetworks']
    checkType("apiObj['socialNetworks']", socialNetworks, [])

    count = 0
    for snet in socialNetworks:
        checkType("apiObj['socialNetwork'[%d]" % count, snet, {})
        expectedKeys = ['network', 'id','url']
        validateKeys("socialNetworks[%d]" % count, snet.keys(), expectedKeys)
        for rkey in expectedKeys:
            checkType("apiObj['socialNetwork'][%d]['%s']" % (count,rkey), snet[rkey], u"")

        count = count + 1
            
    msg("[%s] has returned a valid API object\r\n" % api)


def validateOurWorkReplyData(apiObj, api):

    msg("Validating API specific data for [%s] API call ..." % api)
    
    validateKeys("%s apiObj keys" % api, apiObj.keys(), ['numVideos','videoList'])
    
    numVideos = apiObj['numVideos']
    checkType("apiObj['numVideos']", numVideos, 0)

    videoList = apiObj['videoList']
    checkType("apiObj['videoList']", videoList, [])
    
    msg("Validating count of numApis in videoList");
    if numVideos != len(videoList): raise ValidationError("Expected %d APIs in videoList but got %d instead" % (numApis,len(videoList)))
    
    count = 0
    for videox in videoList:
        checkType("apiObj['videoList'][%d]" % count, videox, {})
        expectedKeys = ['type', 'roles','description','url', 'sUrl','thumb','frame','title']
        validateKeys("videoList[%d]" % count, videox.keys(), expectedKeys)
        
        msg("Validating videoList[%d] dictionary" % count);
        for rkey in expectedKeys:
            if rkey != 'roles':
                checkType("apiObj['videoList'][%d]['%s']" % (count,rkey), videox[rkey], u"")
            else:
                checkType("apiObj['videoList'][%d]['%s']" % (count,rkey), videox[rkey], {})
                expectedRoles = ['director','dp','camera','editor']
                validateKeys("videoList[%d][%s]" % (count,rkey), videox[rkey].keys(), expectedRoles)
                for rolex in expectedRoles:
                    checkType("apiObj['videoList'][%d]['%s']['%s']" % (count,rkey,rolex), videox[rkey][rolex], u"")
                            
        count = count + 1

    msg("[%s] has returned a valid API object\r\n" % api)

def validateVersionsReplyData(apiObj, api):

    msg("Validating API specific data for [%s] API call ..." % api)
    t_dict = type({})
    t_list = type([])
    t_int = type(0)
    
    if type(apiObj) != t_dict: wrongType("apiObj object",t_dict,type(apiObj))
    
    validateKeys("%s apiObj keys" % api, apiObj.keys(), ['numApis','apiList'])
    
    msg("Validating data type of numApis");
    numApis = apiObj['numApis']
    if type(numApis) != t_int: wrongType("numApis",t_int,type(numApis))
    
    msg("Validating count of numApis in apiList");
    apiList = apiObj['apiList']
    if numApis != len(apiList): raise ValidationError("Expected %d APIs in apiList but got %d instead" % (numApis,len(apiList)))

    if type(apiList) != t_list: wrongType("apiList object",t_list,type(apiList))
    
    count = 0
    for apix in apiList:
        msg("Validating data type of apiList[%d]" % count);
        if type(apix) != t_dict: wrongType("apiList[%d] object" % count,t_dict,type(apix))
        expectedKeys = ['apiName', 'apiVersion','apiDataVersion']
        validateKeys("apiList[%d]" % count, apix.keys(), expectedKeys)
        
        for rkey in expectedKeys:
            checkType("apiList[%d]['%s']" % (count,rkey), apix[rkey], u"")
        count = count + 1
            
    msg("[%s] has returned a valid API object\r\n" % api)

import requests

def testReelAPI(host):
    apiSet = ["reels/","reels/0"]

    for api in apiSet:
        r = requests.get("%s/%s" % (host,api))
        reply = r.json()

        try:
            validateCommonReplyData(reply,api)
            validateReelReplyData(reply['apiObj'], api)
        except ValidationError as e:
            print e
            sys.exit(1)

        apiObj = reply['apiObj']
        print "numReels: ", apiObj['numReels']

        for reel in apiObj['reelList']:
            print reel['title'], "available at", reel['url']

        print "\r\n------------------------\r\n"    

def testAboutUsAPI(host):
    apiSet = ["about-us/"]

    for api in apiSet:
        r = requests.get("%s/%s" % (host,api))
        reply = r.json()

        try:
            validateCommonReplyData(reply,api)
            validateAboutUsReplyData(reply['apiObj'], api)
        except ValidationError as e:
            print e
            sys.exit(1)

        print "%.80s... [more]" % reply['apiObj']['aboutus']

        print "\r\n------------------------\r\n"    

def testContactInfoAPI(host):
    apiSet = ["contact-info/"]

    for api in apiSet:
        r = requests.get("%s/%s" % (host,api))
        reply = r.json()

        try:
            validateCommonReplyData(reply,api)
            validateContactInfoReplyData(reply['apiObj'], api)
        except ValidationError as e:
            print e
            sys.exit(1)

        apiObj = reply['apiObj']
        print "Location: ", apiObj['location']
        print "   Email: ", apiObj['email']
        print "   Phone: ", apiObj['phone']
        address = apiObj['address']
        print " Address: %s,%s,%s,%s %s" % (address['name'],address['street'],address['city'],address['state'],address['zipcode'])
        
        count = 0
        for snet in apiObj['socialNetworks']:
            print "socialNetwork[%d] {name:%s, id:%s, url:%s}" % (count,snet['network'],snet['id'],snet['url'])
            count = count + 1
            
        print "\r\n------------------------\r\n"    

def testOurWorkAPI(host):
    apiSet = ["our-work/","our-work/3/"]

    for api in apiSet:
        r = requests.get("%s/%s" % (host,api))
        reply = r.json()

        try:
            validateCommonReplyData(reply,api)
            validateOurWorkReplyData(reply['apiObj'], api)
        except ValidationError as e:
            print e
            sys.exit(1)

        apiObj = reply['apiObj']
        print "numVideos: ", apiObj['numVideos']

        count = 0
        for video in apiObj['videoList']:
            print "videoList[%d] detailed video information:" % count
            print "        type: %s" % video['type']
            roles = video['roles']
            for role in roles.keys():
                if roles[role]: print "%12.12s: %s" % (role,roles[role])
                
            print " description: %.80s ... [more]" % video['description']
            print "       title: %s" % video['title']
            print "         url: %s" % video['url']
            print "        sUrl: %s" % video['sUrl']
            print "       thumb: %s" % video['thumb']
            print "       frame: %s" % video['frame']
            
            count += 1
        
        print "\r\n------------------------\r\n"    

def testVersionsAPI(host):
    apiSet = ["versions/","versions/reels/"]

    for api in apiSet:
        r = requests.get("%s/%s" % (host,api))
        reply = r.json()

        try:
            validateCommonReplyData(reply,api)
            validateVersionsReplyData(reply['apiObj'], api)
        except ValidationError as e:
            print e
            sys.exit(1)

        apiObj = reply['apiObj']
        
        print "numApis: ",apiObj['numApis']
        
        count = 0
        for apix in apiObj['apiList']:
            print "apiList[%d] {apiName:%s, apiVersion:%s, apiDataVersion:%s}" % (count,apix['apiName'],apix['apiVersion'],apix['apiDataVersion'])
            count = count + 1
        
        print "\r\n------------------------\r\n"    

if __name__ == "__main__":

    host = sys.argv[1] if len(sys.argv) > 1 else "."
    api = sys.argv[2] if len(sys.argv) > 2 else "*"
    
    if host == '.': host = "http://localhost:8000"

    
    tests = {"reels":        testReelAPI, 
             "about-us":     testAboutUsAPI, 
             "contact-info": testContactInfoAPI,
             "our-work":     testOurWorkAPI,
             "versions":     testVersionsAPI
    }
             
    if api == "*":
        print "Running ALL CLS REST API tests on host %s" % host
        for apiTest in tests.keys():
            tests[apiTest](host)
            
    elif api in tests.keys():
        print "Running %s CLS REST API tests on host %s" % (api,host)
        tests[api](host)
    else:
        print "usage: lh [host] [test]"
        sys.exit(1)
  
    print "SUCCESS! All tests have passed.\r\n"
