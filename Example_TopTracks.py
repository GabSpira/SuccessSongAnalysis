#imports
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#NB
#to make this work, log in on Spotify for Developers, create an app, and copy the client id and client secret in these variables
client_id = ''
client_secret = ''

#GET TOP TRACKS OF AN ARTIST IN A COUNTRY

auth_manager = SpotifyClientCredentials(client_id = client_id,
                                        client_secret= client_secret)
sp = spotipy.Spotify(auth_manager= auth_manager)

#copy here the link of the artist you want to get the top tracks of
artist = 'https://open.spotify.com/artist/6PvvGcCY2XtUcSRld1Wilr?si=b278c225a98e40b2'    #Example: Silk Sonic

top_tracks = sp.artist_top_tracks(artist, country='IT')
artist_data = sp.artist(artist)

print('\nThese are the top tracks of ' + artist_data['name'] + ' in the selected country: \n')
for track in top_tracks['tracks'][:5]:
    print('track    : ' + track['name'] + '\n')
    print('audio    : ' + track['preview_url'])
    print('cover art: ' + track['album']['images'][0]['url'] + '\n')

print('\nThis is the ' + artist_data['name'] + ' poularity: ' + str(artist_data['popularity']) + '\n')