#!/usr/local/bin/python2
import json;
import requests;
import re;
from pprint import pprint;

# reference: https://forum.unogs.com/topic/9/part-2-a-simple-script-to-pull-information

netflix_url = 'https://www.netflix.com/browse'
cookie_file = open('netflix_cookie')
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

# get additional login data from netflix
response = requests.get(netflix_url, headers=netflix_headers)
react_regex = "reactContext = (.*?);\\s*</script>"
m = re.search(react_regex, response.content)
react_context = m.group(1)
react_context = react_context.replace('\\x', '\\u00') # https://stackoverflow.com/a/18233231/432311
react_json = json.loads(react_context)
data = react_json['models']['serverDefs']['data']
netflix_api_url = data['SHAKTI_API_ROOT'] + '/' + data['BUILD_IDENTIFIER']

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

# uNoGS tutorial example
#base='[["newarrivals",{"from":'+genres+'},{"from":0,"to":'+rmax+'},["title","availability"]],["newarrivals",{"from":'+genres+'},{"from":0,"to":'+rmax+'},"boxarts","_342x192","jpg"]]';

# Netflix my list
#base = '[["lolomonobillboard", "mylist", {"from":0,"to":'+rmax+'},["title","availability"]],["lolomonobillboard", "mylist", {"from":0,"to":'+rmax+'},"boxarts","_342x192","jpg"]]';

# Netflix search
search = "intouchables"
#base = '["search", "'+search+'", "titles", {from: 0, to: 48}, ["summary", "title"]],["search", "'+search'", "titles", {from: 0, to: 48}, "boxarts", "_342x192", "webp"],["search", "'+search+'", "titles", ["id", "length", "name", "trackIds", "requestId"]]'
base = '[["search","'+search+'","titles",{"from":0,"to":'+rmax+'},["summary","title","availability"]],["search","'+search+'","titles",{"from":0,"to":'+rmax+'},"boxarts","_342x192","jpg"]]'
data = '{"paths":'+base+'}'

# Netflix API request
response = requests.post(netflix_api_url + '/pathEvaluator?withSize=true&materialize=true&model=harris&searchAPIV2=false', data=data, headers=netflix_headers)
rjson = response.json()
#pprint(rjson)

# Parse netflix response
print "-------------------------------------"
videos = rjson['value']['videos']
for vid in videos:
    if vid.isnumeric():
        vo = videos[vid]
        title = vo['title']
        boxart = vo['boxarts']['_342x192']['jpg']['url']
        isplayable = vo['availability']['isPlayable']
        retjson = '{"netflixid":"'+str(vid)+'","title":"'+str(title)+'","playable":'+str(isplayable)+',"boxart":"'+str(boxart)+'"}';
        print title

print ""
print "-------------------------------------"
print ""

# Get country info from uNoGS

def isAvailableInCanada(video_id):
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

