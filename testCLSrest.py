"""
testCLSrest.py

This Python script tests the CLS REST API. It invokes every API along with
the variants of each, and then validates the return object to ensure that
all expected data is present and accounted for. It also checks the data
types of all returned data, along with all expected keys, to make sure that
the API is behaving as expected.

usage: testCLSrest.py [host | .] [api | *]
where:
        host = the hostname to issue the REST API calls against. 
                if host == '.', uses http://localhost:8000.
        api = the API to test. By default, tests ALL apis ('*').
        
"""
import os
import sys

# This exception class is raised whenever we detect an error

class ValidationError(Exception):
    def __init__(self, msg):
        self.msg = "ERROR: %s" % msg
    def __str__(self):
        return self.msg
        
def msg(msg):
    """msg(msg): print a message to the console"""
    print "%s:%s" % (os.path.basename(__file__),msg)

def checkType(varName,varValue,expected):
    """checkType(varName,varValue,exptected)
        varName - String indicating the variable whose type is being validated.
        varValue - The variable value. Used to check the actual type.
        expected - The expected type. Used to validate that the actual type is expected.
        
        This function tests the type of a variable to ensure that it is what's expected.
        If it's not, then an exception is thrown.
    """
    msg("Validating data type of %s" % varName);
    if type(varValue) != type(expected):
        raise ValidationError("%s should be %s not %s" % (varName,type(expected),type(varValue)))

def keyIssue(issue,key,keySet):
    """keyIssue(issue,key,keySet)
        issue = whether key is unexpected or missing
        key = the key
        keySet = the keySet being tested
        
        This function throws an exception indicating what type of key issue was found.
        Either a key found was unexpected, or was missing.
    """
    raise ValidationError("%s key %s from %s" % (issue,key,keySet))

def validateKeys(keySet,keysPresent,keysExpected):
    """validateKeys(keySet,keysPresent,keysExpected)
        keySet - the keySet being tested
        keysPresent - the keys present on the object
        keysExpected - the keys expected
        
        This function validates that the keys of a dictionary are present and accounted
        for, and that no extraneous keys are present.
    """
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
    """validateCommonReplyData(reply, api)
        reply - the reply object returned from the JSON call.
        api - the name of the API being checked.
        
        This function validates that the reply object contains the expected keys,
        and that the data types of each key matches what's expected.
    """

    msg("Validating common reply data in [%s] API call ..." % api)
    
    # make sure that reply is a dictionary and that the expected keys are there.
    checkType("reply", reply, {})
    validateKeys("common primary keys", reply.keys(), ['dbgObj','apiVer','apiObj'])
    
    # validate that dbgObj is a dictionary and that the expected keys are present.
    dbgObj = reply['dbgObj']
    checkType("dbgObj", dbgObj, {})
    validateKeys("dbgObj keys", dbgObj.keys(), ['query_string', 'restAPIkeys','parseOK', 'traceMsgQ', 'request_uri'])
    
    # validate that apiVer is a dictionary and that the expected keys are present.
    apiVer = reply['apiVer']
    checkType("apiVer", apiVer, {})
    validateKeys("apiDataVersion keys", apiVer.keys(), ['apiDataVersion', 'apiVersion','apiName'])

    # validate that apiObj is a dictionary. Expected keys are API-specific, so they will
    # be validated in the API specific checker.
    apiObj = reply['apiObj']
    checkType("apiObj", apiObj, {})
    
def validateReelReplyData(apiObj, api):
    """validateReelReplyData(apiObj, api)
        apiObj - the apiObj returned in the reply
        api - the API being tested.
        
        This function validates the 'reels' apiObj data structure to ensure that
        all expected elements are present and of the correct data type.
    """

    msg("Validating API specific data for [%s] API call ..." % api)
    
    # make sure apiObj has the expected keys
    validateKeys("%s apiObj keys" % api, apiObj.keys(), ['reelList','numReels'])
    
    # make sure reelList is a list (array)
    reelList = apiObj['reelList']
    checkType("apiObj['reelList']", reelList, [])

    count = 0
    for reelx in reelList:
        # make sure each element in reelList is a dictionary
        checkType("reelList[%d]" % count,reelx,{});
        # make sure that each element has the expected keys
        expectedKeys = ['url', 'sUrl','thumb','frame','title']
        validateKeys("apiList[%d]" % count, reelx.keys(), expectedKeys)
        for rkey in expectedKeys:
            # make sure each key is a unicode string
            checkType("apiList[%d]['%s']" % (count,rkey), reelx[rkey], u"")
        
        count += 1
    
    # make sure that numReels is an integer
    numReels = apiObj['numReels']
    checkType("apiObj['numReels']", numReels, 0)
    
    # make sure that numReels matches up to the count of array elements in reelList
    msg("Validating count of reels in reelList");
    reels = apiObj['reelList']
    if numReels != len(reels): raise ValidationError("Expected %d reels in reelList but got %d instead" % (numReels,len(reels)))

    msg("[%s] has returned a valid API object\r\n" % api)

def validateAboutUsReplyData(apiObj, api):
    """validateAboutUsReplyData(apiObj, api)
        apiObj - the apiObj returned in the reply
        api - the API being tested.
        
        This function validates the 'about-us' apiObj data structure to ensure that
        all expected elements are present and of the correct data type.
    """

    msg("Validating API specific data for [%s] API call ..." % api)
    
    # make sure the expected keys are present
    validateKeys("%s apiObj keys" % api, apiObj.keys(), ['aboutus'])
    
    msg("[%s] has returned a valid API object\r\n" % api)

def validateContactInfoReplyData(apiObj, api):
    """validateContactInfoReplyData(apiObj, api)
        apiObj - the apiObj returned in the reply
        api - the API being tested.
        
        This function validates the 'contact-info' apiObj data structure to ensure that
        all expected elements are present and of the correct data type.
    """

    msg("Validating API specific data for [%s] API call ..." % api)
    
    # make sure the expected keys are present
    validateKeys("%s apiObj keys" % api, apiObj.keys(), ['location','address','email','phone','socialNetworks'])
    
    # make sure that location is a unicode string
    checkType("apiObj['location']", apiObj['location'], u"")

    # make sure address is a dictionary and that the expected keys are present
    address = apiObj['address']
    checkType("apiObj['address']", address, {})
    expectedKeys = ['name', 'street','city','state','zipcode']
    validateKeys("address keys", address.keys(), expectedKeys)
    for rkey in expectedKeys:
        # make sure the key values are all unicode strings
        checkType("apiObj[address]['%s']" % rkey, address[rkey], u"")
    
    # make sure email and phone are unicode strings
    checkType("apiObj['email']", apiObj['email'], u"")
    checkType("apiObj['phone']", apiObj['phone'], u"")

    # make sure that socialNetworks is a list
    msg("Validating data type of socialNetworks");
    socialNetworks = apiObj['socialNetworks']
    checkType("apiObj['socialNetworks']", socialNetworks, [])

    count = 0
    for snet in socialNetworks:
        # make sure each element in socialNetworks is a dictionary
        checkType("apiObj['socialNetwork'[%d]" % count, snet, {})
        # validate the expected keys in each dictionary
        expectedKeys = ['network', 'id','url']
        validateKeys("socialNetworks[%d]" % count, snet.keys(), expectedKeys)
        for rkey in expectedKeys:
            # make sure each key value is a unicode string
            checkType("apiObj['socialNetwork'][%d]['%s']" % (count,rkey), snet[rkey], u"")

        count += 1
            
    msg("[%s] has returned a valid API object\r\n" % api)


def validateOurWorkReplyData(apiObj, api):
    """validateOurWorkReplyData(apiObj, api)
        apiObj - the apiObj returned in the reply
        api - the API being tested.
        
        This function validates the 'our-work' apiObj data structure to ensure that
        all expected elements are present and of the correct data type.
    """

    msg("Validating API specific data for [%s] API call ..." % api)
    
    # make sure the expected keys are present
    validateKeys("%s apiObj keys" % api, apiObj.keys(), ['numVideos','videoList'])
    
    # make sure that numVideos is an int
    numVideos = apiObj['numVideos']
    checkType("apiObj['numVideos']", numVideos, 0)

    # make sure that videoList is a list
    videoList = apiObj['videoList']
    checkType("apiObj['videoList']", videoList, [])
    
    # make sure that numVideos == the number of elements in the videoList array
    msg("Validating count of numApis in videoList");
    if numVideos != len(videoList): raise ValidationError("Expected %d APIs in videoList but got %d instead" % (numApis,len(videoList)))
    
    count = 0
    for videox in videoList:
        # make sure each video in the list is a dictionary
        checkType("apiObj['videoList'][%d]" % count, videox, {})
        # make sure the expected keys are present in each dictionary
        expectedKeys = ['type', 'roles','description','url', 'sUrl','thumb','frame','title']
        validateKeys("videoList[%d]" % count, videox.keys(), expectedKeys)
        
        msg("Validating videoList[%d] dictionary" % count);
        for rkey in expectedKeys:
            # make sure the data type of each key is correct
            if rkey != 'roles':
                # everything except roles should be a unicode string
                checkType("apiObj['videoList'][%d]['%s']" % (count,rkey), videox[rkey], u"")
            else:
                # roles should be a dictionary
                checkType("apiObj['videoList'][%d]['%s']" % (count,rkey), videox[rkey], {})
                # verify the expected keys are present
                expectedRoles = ['director','dp','camera','editor']
                validateKeys("videoList[%d][%s]" % (count,rkey), videox[rkey].keys(), expectedRoles)
                for rolex in expectedRoles:
                    # make sure each key is a unicode string
                    checkType("apiObj['videoList'][%d]['%s']['%s']" % (count,rkey,rolex), videox[rkey][rolex], u"")
                            
        count += 1

    msg("[%s] has returned a valid API object\r\n" % api)

def validateVersionsReplyData(apiObj, api):
    """validateVersionsReplyData(apiObj, api)
        apiObj - the apiObj returned in the reply
        api - the API being tested.
        
        This function validates the 'versions' apiObj data structure to ensure that
        all expected elements are present and of the correct data type.
    """

    msg("Validating API specific data for [%s] API call ..." % api)

    # make sure the expected keys are present
    validateKeys("%s apiObj keys" % api, apiObj.keys(), ['numApis','apiList'])

    # make sure numApis is an int    
    numApis = apiObj['numApis']
    checkType("apiObj['numApis']", numApis, 0)
    
    # make sure apiList is a list
    apiList = apiObj['apiList']
    checkType("apiObj['apiList']", apiList, [])

    # make sure numApis == number of elements in apiList
    msg("Validating count of numApis in apiList");
    if numApis != len(apiList): raise ValidationError("Expected %d APIs in apiList but got %d instead" % (numApis,len(apiList)))

    count = 0
    for apix in apiList:
        # make sure apiList[%d] is a dictionary
        checkType("apiList[%d]" % count, apix, {})
        # make sure the expected keys are present
        expectedKeys = ['apiName', 'apiVersion','apiDataVersion']
        validateKeys("apiList[%d]" % count, apix.keys(), expectedKeys)
        
        for rkey in expectedKeys:
            # make sure the type of each element in the dictionary is a unicode string
            checkType("apiList[%d]['%s']" % (count,rkey), apix[rkey], u"")
        count += 1
            
    msg("[%s] has returned a valid API object\r\n" % api)

import requests

def testReelAPI(host):
    """testReelAPI(host)
    
        host - the host to execute the REST API call against.
        
        This function runs the two variants of the reels API. One that returns
        all reels, and another that returns the latest reel.
    """
    apiSet = ["reels/","reels/0"]

    for api in apiSet:
        # issue the GET /reels API, and then grab the JSON data.
        r = requests.get("%s/%s" % (host,api))
        reply = r.json()

        try:
            # validate the common reply data
            validateCommonReplyData(reply,api)
            # validate the reels-specific reply data
            validateReelReplyData(reply['apiObj'], api)
        except ValidationError as e:
            print e
            sys.exit(1)

        # pretty print the reels-specific data
        apiObj = reply['apiObj']
        print "numReels: ", apiObj['numReels']

        for reel in apiObj['reelList']:
            print reel['title'], "available at", reel['url']

        print "\r\n------------------------\r\n"    

def testAboutUsAPI(host):
    """testAboutUsAPI(host)
    
        host - the host to execute the REST API call against.
        
        This function tests the about-us API.
    """
    apiSet = ["about-us/"]

    for api in apiSet:
        # issue the GET /about-us API, and then grab the JSON data.
        r = requests.get("%s/%s" % (host,api))
        reply = r.json()

        try:
            # validate the common reply data
            validateCommonReplyData(reply,api)
            # validate the about-us specific reply data
            validateAboutUsReplyData(reply['apiObj'], api)
        except ValidationError as e:
            print e
            sys.exit(1)

        # pretty print the about-us specific data
        print "%.80s... [more]" % reply['apiObj']['aboutus']

        print "\r\n------------------------\r\n"    

def testContactInfoAPI(host):
    apiSet = ["contact-info/"]

    for api in apiSet:
        r = requests.get("%s/%s" % (host,api))
        reply = r.json()

        try:
            # validate the common reply data
            validateCommonReplyData(reply,api)
            # validate the contact-info specific reply data
            validateContactInfoReplyData(reply['apiObj'], api)
        except ValidationError as e:
            print e
            sys.exit(1)

        # pretty print the contact-info specific data
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
            # validate the common reply data
            validateCommonReplyData(reply,api)
            # validate the our-work specific reply data
            validateOurWorkReplyData(reply['apiObj'], api)
        except ValidationError as e:
            print e
            sys.exit(1)

        # pretty print the our-work specific data
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
            # validate the common reply data
            validateCommonReplyData(reply,api)
            # validate the versions-specific reply data
            validateVersionsReplyData(reply['apiObj'], api)
        except ValidationError as e:
            print e
            sys.exit(1)

        # pretty print the versions-specific data
        apiObj = reply['apiObj']
        
        print "numApis: ",apiObj['numApis']
        
        count = 0
        for apix in apiObj['apiList']:
            print "apiList[%d] {apiName:%s, apiVersion:%s, apiDataVersion:%s}" % (count,apix['apiName'],apix['apiVersion'],apix['apiDataVersion'])
            count = count + 1
        
        print "\r\n------------------------\r\n"    

if __name__ == "__main__":

    # if a host override is present, pick it up
    host = sys.argv[1] if len(sys.argv) > 1 else "."
    # if an api override is present, pick it up
    api = sys.argv[2] if len(sys.argv) > 2 else "*"
    
    # if host == '.', force it to the default localhost
    if host == '.': host = "http://localhost:8000"

    # Set up a dictionary with the API names and test functions
    tests = {"reels":        testReelAPI, 
             "about-us":     testAboutUsAPI, 
             "contact-info": testContactInfoAPI,
             "our-work":     testOurWorkAPI,
             "versions":     testVersionsAPI
    }
             
    if api == "*":
        # if we are running all tests
        print "Running ALL CLS REST API tests on host %s" % host
        # for each API, invoke the test function
        for apiTest in tests.keys():
            tests[apiTest](host)
            
    elif api in tests.keys():
        # if we are running a specific test
        print "Running %s CLS REST API tests on host %s" % (api,host)
        # run that single test
        tests[api](host)
    else:
        print "usage: lh [host] [test]"
        sys.exit(1)
  
    print "SUCCESS! All tests have passed.\r\n"
