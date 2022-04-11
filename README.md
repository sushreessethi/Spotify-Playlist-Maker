# Spotify-Playlist-Maker
Spotify Playlist Maker is a Python program that builds a new Spotify playlist for the date given by the user. This script was written for personal use, so the playlist creation is authorized by an access token retreived for my Spotify account.

How it works

1.The most recently acquired Spotify access token and the script's Spotify refresh token my "app's" client ID and secret are stored in a local text file called tokens (I've excluded this database from the repository because these tokens provide read and write access to my Spotify account).
2.When the script starts, it first checks the authority of its current access token.
3.Now that it has a valid access token, it proceeds to scrape the current top 100 songs from The Hot 100, located at this URL: https://www.billboard.com/charts/hot-100
4.It parses through the page with the Beautiful Soup 4 library, building a list of "song_uris."
5.Creates a new private playlist with the name "YYYY-MM-DD Billboard 100" and add songs listed in song_uris. Songs which are not available in Spotify, we have used exception handling to skip over those songs.
6.It then uses the playlist id and song ids to make a POST request to a Spotify endpoint that adds each song to the playlist and returns playlist link.
