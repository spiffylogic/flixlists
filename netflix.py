#!/usr/local/bin/python2
import json;
import requests;
import re;
from pprint import pprint;
import sys;

# reference: https://forum.unogs.com/topic/9/part-2-a-simple-script-to-pull-information

netflix_url = 'https://www.netflix.com/browse'
cookie_file = open('netflix-cookie')
netflix_cookie = cookie_file.read()[:-1] # strip newline character
netflix_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
        'Cookie': netflix_cookie,
        'Accept': 'application/json, text/javascript, */*',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Referer': 'https://www.netflix.com'}

unogs_url = 'https://unogs-unogs-v1.p.mashape.com/api.cgi'
unogs_api_key = 'PMVIAK4mm1mshMVt7UUJH2uG57kSp1nuxnMjsnZWe4xqRF0Be8'
unogs_headers = {'X-Mashape-Key': unogs_api_key, 'Accept': 'application/json'}

try:
    # get additional login data from netflix
    response = requests.get(netflix_url, headers=netflix_headers)
    react_regex = "reactContext = (.*?);\\s*</script>"
    m = re.search(react_regex, response.content)
    react_context = m.group(1)
    react_context = react_context.replace('\\x', '\\u00') # https://stackoverflow.com/a/18233231/432311
    react_json = json.loads(react_context)
    data = react_json['models']['serverDefs']['data']
    netflix_api_url = data['SHAKTI_API_ROOT'] + '/' + data['BUILD_IDENTIFIER'] + '/pathEvaluator?withSize=true&materialize=true&model=harris&searchAPIV2=false'

    # netflix profile selection (WIP)
    falkorcache_regex = "(?<=falkorCache = )(.*?)(?=;</script>)"
    m = re.search(falkorcache_regex, response.content)
    falkor = m.group(1)
    falkor = falkor.replace('\\x', '\\u00') # https://stackoverflow.com/a/18233231/432311
    falkor_json = json.loads(falkor)
    profile_data = falkor_json['profiles']
    lolomo = falkor_json['lolomo'][1] # maybe this is used for loading recommendations

    genres = '0,"to":1'
    rmax = '48'

except:
    print "Netflix initialization failed. Refresh your cookie or check your internet connection"

# uNoGS tutorial example
#base='[["newarrivals",{"from":'+genres+'},{"from":0,"to":'+rmax+'},["title","availability"]],["newarrivals",{"from":'+genres+'},{"from":0,"to":'+rmax+'},"boxarts","_342x192","jpg"]]';

def postRequest(base):
    data ='{"paths":'+base.encode('ascii', 'ignore')+'}' # ignore special unicode characters in titles for now (e.g. WALL-E)
    response = requests.post(netflix_api_url, data=data, headers=netflix_headers)
    rjson = response.json()
    return rjson['value']

# Netflix my list
def list():
    base = '[["lolomonobillboard", "mylist", {"from":0,"to":'+rmax+'},["title","availability"]],["lolomonobillboard", "mylist", {"from":0,"to":'+rmax+'},"boxarts","_342x192","jpg"]]';
    return postRequest(base)

# Netflix API search request
def search(q):
    base = '[["search","'+q+'","titles",{"from":0,"to":'+rmax+'},["summary","title","availability", "availabilityEndDateNear"]],["search","'+q+'","titles",{"from":0,"to":'+rmax+'},"boxarts","_342x192","jpg"]]'
    return postRequest(base)

# Returns true if the first result in a search for the title is an exact match
def getAvailability(video_title):
    value = search(video_title)
    #parseVideos(value)
    # Roughly, this is how the response is structured with respect to what we're looking for:
    #   value/search/<q>/titles/0 -> ['videos',<ID>]
    #   value/videos/<ID> -> {title: <q>}
    availability = {}

    try:
        s = value.get('search')
        v = value.get('videos')
        a = s[video_title]['titles']['0'] # first result
        title = v[a[1]]['title']
        available = title.lower() == video_title.lower() # confirm if we have a match
        endDate = v[a[1]]['availabilityEndDateNear'] # this will be either a date string (if expiring soon) or a mysterious (useless) object otherwise

        availability = {}
        availability["available"] = available
        if isinstance(endDate, basestring):
            availability["endDate"] = endDate
    except:
        print "Something went wrong with " + video_title
        availability["available"] = False

    return availability

# Parse netflix videos response
def parseVideos(value):
    videos = value.get('videos')
    if videos:
        for vid in videos:
            if vid.isnumeric():
                vo = videos[vid]
                title = vo['title']
                print title
                boxart = vo['boxarts']['_342x192']['jpg']['url']
                isplayable = vo['availability']['isPlayable']
                retjson = '{"netflixid":"'+str(vid)+'","title":"'+title.encode('utf-8')+'","playable":'+str(isplayable)+',"boxart":"'+str(boxart)+'"}';
    else:
        print 'No videos'

# Get country info from uNoGSi (don't do this anymore)
def isAvailableInCanadaUNOGS(video_id):
    print video_id
    response = requests.get(unogs_url+'?t=loadvideo&q='+video_id, headers=unogs_headers)
    try:
        rjson = json.loads(response.content.replace('&quot;','"'))
        country_json = rjson['RESULT']['country']
        for j in country_json:
            if j[1].lower() == 'ca':
                return True
        return False
    except ValueError:
        pass
    return False
