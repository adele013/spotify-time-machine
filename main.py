import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input('Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ')
URL = f'https://www.billboard.com/charts/hot-100/{date}'
CLIENT_ID = 'Enter your Client ID'
CLIENT_SECRET = 'Enter your Client Secret'

response = requests.get(URL)
page_html = response.text
soup = BeautifulSoup(page_html, 'html.parser')

titles = soup.select(selector='li h3', class_='c-title')

song_list = [title.getText().strip() for title in titles]
song_list = song_list[0:100]

spotify = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope='playlist-modify-private',
            redirect_uri='http://example.com',
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            show_dialog=True,
            cache_path='token.txt'
        )
)
user_id = spotify.current_user()["id"]

song_uri = []
year = date.split('-')[0]
search_years= f'{int(year)-1}-{year}'
for song in song_list:
    result = spotify.search(q=f'track:{song} year:{search_years}', type='track')
    try:
        uri = result['tracks']['items'][0]['uri']
        song_uri.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped")

playlist_name = f'{date} Billboard 100'
result = spotify.user_playlist_create(user=user_id, name=playlist_name, public=False)
playlist_id = result['id']

spotify.playlist_add_items(playlist_id=playlist_id, items=song_uri)