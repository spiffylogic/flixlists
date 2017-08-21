#!/usr/local/bin/python2

import sys
#import netflix
#import imdb

def usage():
    print 'usage: flixlists <cmd>'
    print 'where cmd is one of ...'

if len(sys.argv) != 2:
    usage()
elif sys.argv[1] == 'netflix':
    print 'Show Netflix My List'
elif sys.argv[1] == 'imdb':
    print 'Show IMDb Watchlist'
elif sys.argv[1] == 'netflix-cookie':
    print 'Paste Netflix cookie here:'
else:
    usage()

