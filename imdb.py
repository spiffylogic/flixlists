#!/usr/local/bin/python2

import json;
import requests;
import re;
from pprint import pprint;
import netflix

# Enter your IMDb user ID here:
imdb_user = 'ur12345678'

imdb_url = 'http://www.imdb.com'
# Note: the cookie isn't actually needed when using the username and public watchlist
#cookie_file = open('imdb-cookie')
#imdb_cookie = cookie_file.read()[:-1] # strip newline character
imdb_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        #'Cookie': imdb_cookie,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.8',
        'Referer': 'http://www.imdb.com/'}

# scrape the watchlist page and extract the json contents
url = imdb_url + '/user/' + imdb_user + '/watchlist'
response = requests.get(url, headers=imdb_headers)
react_regex = "IMDbReactInitialState.push\((.*?)\);"
m = re.search(react_regex, response.content)
s = m.group(1)
react_json = json.loads(s)

items = react_json['list']['items']
#print("Found "+str(len(items))+" items in master list")

titles_json = react_json['titles']
# this contains the first 100 titles of the watchlist
#print("Found "+str(len(titles_json))+" titles in titles list")

def printTitle(j, item_id, primary_json):
    title = primary_json['title']
    # Note: year not available for in-development films
    if 'year' in primary_json:
        year_str = ' ('+primary_json['year'][0]+')'
    else:
        year_str = ''
    print str(j)+": "+item_id+": "+title+year_str

    ca = False
    #ca = netflix.isAvailableInCanadaUNOGS(item_id)
    a = netflix.getAvailability(title)
    ca = a.get("available")
    if ca:
        endDate = a.get("endDate")
        print '^ AVAILABLE ON NETFLIX' + ((' UNTIL ' + endDate) if endDate != None else '')

page_size = 50

# First 2 pages available in titles json
j = 0
for i in range(2*page_size):
    j = j+1
    item_id = items[i]['const']
    printTitle(j, item_id, titles_json[item_id]['primary'])

# Subsequent pages are available from data endpoint
for page in range(2, len(items) / page_size + 1):
    print "(Page "+str(page)+")"
    ids = map(lambda x: x['const'], items[page*page_size:(page+1)*page_size])
    url = imdb_url+'/title/data?ids='+','.join(ids)
    response = requests.get(url)
    data_json = response.json()
    for item_id in data_json:
        j = j+1
        printTitle(j, item_id, data_json[item_id]['title']['primary'])
