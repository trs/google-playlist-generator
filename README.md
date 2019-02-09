## Google Play Music Playlist Generator

### What?
This is a script to generate a series of Google Play Music playlists containing every song in a library.

### Why?
This script exists to work around some annoying limitations in the Google Play Music service. It is rather specific to my preferred use case, but it may be handy for like-minded individuals:

1. I have a large collection of local music amassed over several years of ripping CD's on my primary PC. I use Google Play Cusic as a cloud backup, uploading my tracks via Google Music Manager. Lately I've given up on buying physical copies and have switched to purchasing through Google Play.

2. I prefer having a local copy of all my music on my phone. I have limited data plan and don't always have good cell reception for streaming.

3. I use Google home devices to listen to music at home. Usually I drive this process via my phone (it's easier than voice commands), but not always.

Unfortunately, there is no seamless way to meet all my needs. To put tracks on my phone, I could manually copy files from my PC to my phone, or rely on Google Play Music's caching mechanism. Neither option works great.

Google Play Music does not allow one to cast local music files from the phone ([link][1]), so the only way to use the music on a Google device is to act as a dumb-speaker via bluetooth. This requires my phone to be available and within bluetooth range and wastes battery. Also, it is difficult to have a single consistent view of my combined (manually ripped + Google purchases) music collection.

Google Play Music's local caching would give me one consistent local copy off the music and allow casting without bluetooth. The challenge there, which this script aims to fix, is that there is no way to bulk download all songs to a device.

Google does not provide a simple button to download all tracks. When you have thousands of tracks, it is too cumbersome to download each track, album, etc. individually. The best way to do so is to create a playlist of songs and download them one playlist at a time. There is a 1000 limit on the number of tracks, and creating those playlists is annoying ([link][2]).

This script uses gmusicapi to generate a series of playlists containing all songs in a music library. With those playlists defined, it is just a matter of tapping "Download Playlist" N times to cache an entire music collection. 

[1]: https://productforums.google.com/forum/#!msg/play/MCr2OckaOt0/aw5uMq8mDQAJ
[2]: https://productforums.google.com/forum/#!msg/play/tCEea8gAKvQ/Leje9ie0BQAJ


### How?
First, install the dependencies (gmusicapi). I tested with version 12. `pip install -r requirements.txt`

Next, you must establish an oauth2 session and acquire a device id. Refer to [gmusicapi documentation](https://unofficial-google-music-api.readthedocs.io/en/latest/reference/mobileclient.html#setup-and-login) for details.

Create a settings.ini file and place the device_id for your oauth session in there. Refer to settings.example.ini for details.

Run the script: `python3 google_playlist_generator.py`

Check your Google Play Music app. You should see the playlists generated in your music library within a few seconds. The playlists may appear empty for a few minutes, but will fill in. Once finished, you can manually download them all to your device by tapping the 3 vertica dots next to the playlist and choosing "Download".

**Caution:** neither this script nor the underlying gmusicapi is a supported Google API. Use at your own risk.

