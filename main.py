import requests
from bs4 import BeautifulSoup
import datetime
import spotipy
import random
from spotipy.oauth2 import SpotifyOAuth


BASE_URL = "https://www.billboard.com/charts/hot-100"

username = 'sss'
scope = 'playlist-modify-private'

CLIENT_ID = YOUR CLIENT ID
CLIENT_SECRET = YOUR CLIENT SECRET

oauth = spotipy.SpotifyOAuth(
    scope="playlist-modify-private",
    redirect_uri="https://example.com/",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    show_dialog=True,
    cache_path="token.txt"
)

sp = spotipy.Spotify(auth_manager=oauth)
user_id = sp.current_user()['id']

# Taking Input
correct_date = False
while not correct_date:
    input_date = input("Which date do you want to travel to?\n"
                       "Type the date in this format YYYY-MM-DD:\n")
    input_date_list = input_date.split("-")
    if len(input_date_list) == 3:
        try:
            year = int(input_date_list[0])
            month = int(input_date_list[1])
            day = int(input_date_list[2])
        except ValueError:
            print("Incorrect date format entered (please use integers only)")
        else:
            try:
                date = datetime.datetime(year, month, day)
            except ValueError:
                print("Non-existent date detected")
            else:
                correct_date = True
    else:
        print("Incorrect date format entered (please use the '-' separator)")

    #checking validity
    
    current_date = datetime.datetime.now()
    date_provided = datetime.datetime.strptime(input_date, '%Y-%m-%d')
    if date_provided.date() >= current_date.date():
        correct_date = False
        print("Date provided can't be in the future")
    elif int(date_provided.strftime("%U")) == int(current_date.strftime("%U")):
        date = date_provided-datetime.timedelta(days=7)
        correct_date = True


#Searching Songs usign scraping
url = f'{BASE_URL}/{date.strftime("%Y-%m-%d")}'
soup = BeautifulSoup(requests.get(url).text, "html.parser")
songs = soup.find_all(name='h3', class_="a-no-trucate")
song_names = [song.getText().strip() for song in songs]


#making of playlist
song_uris = []
year = date.strftime("%Y-%m-%d").split("-")[0]

for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{(date_provided.strftime('%Y-%m-%d'))} Billboard 100", public=False)
random.shuffle(song_uris)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
print(f"Your playlist link: {playlist['external_urls']['spotify']}")

