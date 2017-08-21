#!/usr/local/bin/python2

import json;
import requests;
import re;
from pprint import pprint;
import netflix

imdb_user = 'ur34919593'
imdb_url = 'http://www.imdb.com'
imdb_cookie = 'session-id=141-6721691-6480963; session-id-time=2131402614; csm-hit=12QTSJH2CC9TBZ03B3Q9+s-12QTSJH2CC9TBZ03B3Q9|1500682653469; ubid-main=134-6646058-6334328; session-token="DRX8sTUHoINYPwb43TLAxjTa1e55DK/jzsBrkO5UATjncl5avnp1FBVzGGN5kKz8TcX49HO06l2D/sArdyeUim0OEeqHsfS60lf9jNUvFYoLkGyTklSOPU68V43+XRjem2N33g1mRrNWUds+yDs01UJ8FMb+CLH6pl39p8Fhn0LDpmKgWRajA31O4wIT6s834r+OR8KeSsGk1TPlOlb9RQ=="; x-main="QUEzW8aTY2KdeRsilmfRMdX6BB1saBO8zhBk2pdDZ80PI8YLT?bJ7c9?7z572kJL"; id=BCYkWB4UQb8OQDsUT85jBiPlOfmbMyYukzR0VZE4409wHqnJC0dMCv5dgpvORdxtcYUSf1LJrpmh%0D%0AkdCMrRSOLyhF6Zlg7cKY3mwFv-sb6Hw9ggYrGwZZ7KR-bHz1oTl2taEwPBrXUZAc7e22rxc3Pwoq%0D%0A2Y8t_PASpplW2LXWe2A7sKQ_XuvdwX2SMwywVoXScuFnEBZQxs84GzUDb73ebQ0AlA%0D%0A; uu=BCYnF8Bs5t8ULb0GbRBndB_OMUE2aCS7JsU3NNT6fi_g2byvXVJtoNAO1nieXNiHpAQZi8P1cQUw09Dfs0HoF2rNRQrHqUmnWzQiHLOUYBSOY6RAMteqx3c8-gh48TuPDMcW4_Vh25MrAUtzXinMb1AASXjfjjLbP2-SoYEyOTq-0NEQaDjIuqvDUiKNnWqmEaaCBt0e4LUI_BpURTowk1ZzD9S9DHw1p2znI8TMiXkhXoapoUvFF2SaOSwIw_JzVwN2tTkpBmCy9YVxCUMaYGDiYuZe-UdSnTnBBg4e_kscIfaDJFoj4Es7-kb9iRFki4uUHyjbO5rpWVcAzw6O96dkHw; as=%7B%22h%22%3A%7B%22t%22%3A%5B0%2C0%5D%2C%22tr%22%3A%5B0%2C0%5D%2C%22ib%22%3A%5B0%2C0%5D%7D%2C%22n%22%3A%7B%22t%22%3A%5B0%2C0%5D%2C%22tr%22%3A%5B0%2C0%5D%2C%22in%22%3A%5B0%2C0%5D%2C%22ib%22%3A%5B0%2C0%5D%7D%7D; cache=BCYkVXunuH2E_kwc7ksT4lucgechiDMZTsCmw2-lDPw9ekyzR-fFW0jBIk5omSZ3i4EeiYndd1TP%0D%0A5nDjfe1oCg1e17i86tEBeDAznKigq6oEFjc%0D%0A'
imdb_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Cookie': imdb_cookie,
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

pprint(react_json)
print()

items = react_json['list']['items']

print("Found "+str(len(items))+" items in master list")

titles_json = react_json['titles']
# this contains the first 100 titles of the watchlist

print("Found "+str(len(titles_json))+" titles in titles list")
print("IMDb Watchlist")
print("")

page_size = 50

# First 2 pages available in titles json
j = 0
for i in range(2*page_size):
    j = j+1
    item_id = items[i]['const']
    primary_json = titles_json[item_id]['primary']
    title = primary_json['title']
    # Year not available for in-development films
    if 'year' in primary_json:
        year_str = ' ('+primary_json['year'][0]+')'
    else:
        year_str = ''

    ca = False
    if j >= 10 and j < 60:
        ca = netflix.isAvailableInCanada(item_id)
    print str(j)+": "+item_id+": "+title+year_str+(' (NETFLIX)' if ca else '')

# Subsequent pages are available from data endpoint
for page in range(2, len(items) / page_size + 1):
    print "Page "+str(page)
    ids = map(lambda x: x['const'], items[page*page_size:(page+1)*page_size])
    url = imdb_url+'/title/data?ids='+','.join(ids)
    response = requests.get(url)
    data_json = response.json()
    for item_id in data_json:
        j = j+1
        primary_json = data_json[item_id]['title']['primary']
        title = primary_json['title']
        # Year not available for in-development films
        if 'year' in primary_json:
            year_str = ' ('+primary_json['year'][0]+')'
        else:
            year_str = ''
        print str(j)+": "+item_id+": "+title+year_str

