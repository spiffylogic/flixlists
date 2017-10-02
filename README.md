# flixlists

This is Python command line utility quickly hacked together to view your Netflix and IMDb movie lists.
The main use case is to answer the question "which of my IMDb watchlisted movies are available on Netflix?"
End dates will be shown for titles that are expiring soon on Netflix.

To identify your Netflix and IMDb identities:
1. Copy your Netflix cookie and paste it into the file `netflix-cookie` for the program to use.
2. Enter your IMDb user ID at the top of `imdb.py` (taken from the IMDb URL, e.g. "ur12345678"), assuming you have a public watchlist.

To view your IMDb "Watchlist" and identify ones that are on Netflix: `flixlists.py imdb`

To view your Netflix "My List": `flixlists.py netflix`

To see if a particular title is currently on netflix: `flixlists.py netflix "Movie Title"`
