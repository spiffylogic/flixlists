#!/usr/local/bin/python2

import sys
import netflix
#import imdb

def usage():
    print 'usage: flixlists <cmd>'
    print 'where cmd is one of ...'

if len(sys.argv) < 2:
    usage()
elif sys.argv[1] == 'netflix-list':
    print 'Netflix My List:'
    value = netflix.list()
    netflix.parseVideos(value)
elif sys.argv[1] == 'netflix-search' and len(sys.argv) > 2:
    title = sys.argv[2]
    print 'Is ' + title + ' available on Netflix?'
    print netflix.isAvailable(title)
elif sys.argv[1] == 'netflix-cookie':
    print 'Paste Netflix cookie here:'
    # TODO: save pasted cookie
elif sys.argv[1] == 'imdb':
    print 'Show IMDb Watchlist'
else:
    usage()

