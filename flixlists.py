#!/usr/local/bin/python2

import sys

def usage():
    print 'usage: flixlists <cmd>'
    print 'where cmd is one of ...'

if len(sys.argv) < 2:
    usage()
elif sys.argv[1] == 'netflix' and len(sys.argv) == 2:
    print 'Netflix My List:'
    import netflix
    value = netflix.list()
    netflix.parseVideos(value)
elif sys.argv[1] == 'netflix' and len(sys.argv) > 2:
    title = sys.argv[2]
    print 'Is ' + title + ' available on Netflix?'
    import netflix
    print netflix.getAvailability(title)
elif sys.argv[1] == 'imdb':
    print 'IMDb Watchlist:'
    import imdb
else:
    usage()

