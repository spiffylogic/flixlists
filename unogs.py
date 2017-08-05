#!/usr/local/bin/python2
import json;
import requests;
import re;
from pprint import pprint;

# reference: https://forum.unogs.com/topic/9/part-2-a-simple-script-to-pull-information

netflix_url = 'https://www.netflix.com/browse'
netflix_cookie = 'clSharedContext=ff3fd1d3-5cf4-4832-8f49-e0ef22360b2a; dsca=customer; nfvdid=BQFmAAEBEDtC%2BYNtlR8D1xU2RFnDeidgHQsaDM0dhlB3m1S%2B7H2hU9nHKoeo6cu15hyLbNBYfHzhwDnZJNO%2BglhIpRfYj767sRqCNFOtGmHaxWBmPD4f0xO9ys0EwbYBhpDxal3OaVs3cJfZyfvxOmIJTHirLF%2B%2B; cL=1500247626460%7C150024254182077247%7C150024254120153457%7C%7C864%7C32D3J42M4NAK5BOMBH5MZH5KAA; SecureNetflixId=v%3D2%26mac%3DAQEAEQABABQs-qipU0OI6jVCPg3D9SyuSN4ploTZJVI.%26dt%3D1500413864137; NetflixId=ct%3DBQAOAAEBEDPWaNrENBQE_63gX4VfUreCQMMDn-U1A2FEgPniU9nUvDyvEyAa7TuE3RKgnU9TPhSR3H3SoO9S_XNzQYDNyLywjJNkuDQ6EYepFFyf7ZxtSIrX4OKN62L0fQ9awQ33Y_k-CvJ2n4_nMykHlFOpQ5yg_PNTkpHUo8nPzEiN101TIE1ksKrVelUc1YLa5j_Y8dQUdH5HLR1QVGuFsoOtrbOeH8vzY8lfw8cDezhMSbp1-KIdIzdDdWpP-MN-QkU_VDaQl4sjyTKo2SrhaSeJHxGo9LYfb1Sr050WSlYKShcTS2Vl0kLoowTaQCtz_8tueFHIZvF4VMGRruvBcfJKQOdwrMENcPWYKcROm2vnuL2zaEp1VXDc6n-TRvn9DL6T_P3nEM3-z9uYk7Gab6018LTvmRy9dsSLiUrJUiVM3UYke0u35VYB3ps8Hw8AAjiXlaDwlyCEeKkfNnO4SIVzw_UR64fSNvUW0pEndg3QrwB_hKEycDI9UtiUFHUwzmqvtRLKNO8Yy-i6eFVtTYDxVs_XHncEKn3JMdh0yfPu-fVrcOZp0yiuhiq-VHhywyUiAAThjnxHkl4W03xUVXQIn6ry9xSQgrKReQ_DOz4Yu2MEkyOjnqEjhWFpFWhz5RXkXwJ4vdxkMcvkiYKSfgsZwLOznB2solV77DDLekX7J8faOR0yIcUrWEw3dFjbks3WaWrVaVoxzInwXAGQUOakCW862CnK186LLdurcvk14cdIKlrTcxu2MVgMxFWO4PzUq5IFNCMTRAbpLF21QxoCG7uF1A..%26bt%3Ddbl%26ch%3DAQEAEAABABRDaFNWmoX6qeg_eWQelh9RmppVvnLon4Y.%26v%3D2%26mac%3DAQEAEAABABRfcZh4XxfHQe4l9n0_KtnaxMSTu48d25k.; playerPerfMetrics=%7B%22uiValue%22%3A%7B%22throughput%22%3A13208%7D%2C%22mostRecentValue%22%3A%7B%22throughput%22%3A13208%7D%7D; lhpuuidh-browse-LJCXDB5I6JGQJCNOIE7TEGO5Z4=CA%3AEN-CA%3A3e92226b-2e3c-4f14-9553-5c6f6b809e68_ROOT; lhpuuidh-browse-LJCXDB5I6JGQJCNOIE7TEGO5Z4-T=1500413876790; profilesNewSession=0; memclid=62f432b1-afd6-4122-90ad-3b54679aed6e';
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

