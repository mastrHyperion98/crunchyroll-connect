# crunchyroll-connect

Crunchyroll-connect is a python library used to connect, communicate and fetch streaming data from api.crunchyroll.com. This library enables developers to 
develop their own Crunchyroll Application alternative with more robust and flexible features. 

# Features

* Search crunchyroll API by query
* Filter Crunchyroll catalog by genres, seasons (ex fall 2020), popularity, release dates, prefixes, etc
* Get a list of all the collections related to a series. (For example, each season of SAO is a different collection) 
* Easy to use, self managed package that handles the safe storage of data locally used by application. 
* Fetch and return stream data that can be used by external/custom media players

# Implementation Requirements
* FFmpeg(ffplayer --> https://matham.github.io/ffpyplayer/player.html) recommended for HLS episodes. 
* In theory, VLC also supports HLS, but i've had no luck getting it to properly read the stream. 


# Important Reference Works

* https://github.com/CloudMax94/crunchyroll-api/wiki
* https://github.com/BeeeQueue/yuna

Both of the above repositories were extremely important to help me understand how the crunchyroll api functions. 
