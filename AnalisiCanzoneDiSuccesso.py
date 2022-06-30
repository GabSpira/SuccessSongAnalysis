#imports
from spotipy.oauth2 import SpotifyOAuth
import dataframe_image as dfi
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time 
import numpy as np
from matplotlib import pyplot as plt
import plotly.express as px
import os


#----------------------------------------------------------------------------------------------#


#GET FEATURES FOR A PLAYLIST


#----------------------------------------------------------------------------------------------#


#auth

#to make this work, log in on Spotify for Developers, create an app, and copy the client id and client secret in these variables
id = ''
secret = ''

auth_manager = SpotifyClientCredentials(client_id = id,
                                        client_secret= secret)
sp = spotipy.Spotify(auth_manager= auth_manager)


#-----------------------------------------------------------------------------------------#


#functions

#function to get ids of track in one single page of message (up to 100)
def getIDsinPage(tracks, id):
    for i,item in enumerate(tracks['items']):
        track = item['track']
        id.append(track['id'])


#function to get ids of tracks in a playlist
def getTracksIDs(user, playlist_id):
    track_ids = [ ]
    playlist = sp.user_playlist(user, playlist_id)
    tracks = playlist['tracks']
    getIDsinPage(tracks, track_ids)
    
    #if playlist has more than 100 songs
    while tracks['next']:
        tracks = sp.next(tracks)
        getIDsinPage(tracks, track_ids)

    return track_ids
       

#function to get features of a track given its id
def getTrackFeatures(id):
    track_info = sp.track(id)
    features_info = sp.audio_features(id)

    #track info
    name = track_info['name']
    artist = track_info['album']['artists'][0]['name']
    release_date = track_info['album']['release_date']
    length = track_info['duration_ms']
    popularity = track_info['popularity']

    #track features
    acousticness = features_info[0]['acousticness']
    danceability = features_info[0]['danceability']
    energy = features_info[0]['energy']
    instrumentalness = features_info[0]['instrumentalness']
    liveness = features_info[0]['liveness']
    loudness = features_info[0]['loudness']
    speechiness = features_info[0]['speechiness']
    tempo = features_info[0]['tempo']
    time_signature = features_info[0]['time_signature']
    mode = features_info[0]['mode']
    valence = features_info[0]['valence']

    track_data = [name, artist, release_date, length,
                popularity, acousticness, danceability, energy, 
                instrumentalness, liveness, loudness, speechiness,
                tempo, time_signature, mode, valence]

    return track_data


#---------------------------------------------------------------------#


#main

#set your playlist here 
playlist_link = ''

#get ids of tracks in a playlist
track_ids = getTracksIDs('spotify', playlist_link)
print('Nella playlist ci sono ' + str(len(track_ids)) + ' canzoni')

#obtain features for each song in playlist from id
track_list = []
for i in range(len(track_ids)):
    time.sleep(.3)
    track_data = getTrackFeatures(track_ids[i])
    track_list.append(track_data)

#dataframe
playlist = pd.DataFrame(track_list, columns = ['Name', 'Artist', 'Release-Date', 
                                            'Length', 'Popularity', 'Acousticness', 'Danceability', 
                                            'Energy', 'Instrumentalness', 'Liveness', 'Loudness', 
                                            'Speechiness', 'Tempo', 'Time-Signature', 'Mode', 'Valence'])
#dataframe style
playlist_styled = playlist.head(200).style.set_properties(**{'background-color': '#fee68f',
                                                            'color': '#830340',
                                                            'border-color': 'blue',
                                                            'align': 'center'})\
                                            .format({"Loudness": "{:20,.0f} dB"})
playlist_styled = playlist_styled.set_caption("Features of the selected song")

#export dataframe
os.makedirs('./Images', exist_ok=False)
dfi.export(playlist_styled, './Images/Playlist_DataFrame.png')


#------------------------------------------------------------------------------------#


#scatter graphs

# scatter graph of Popularity using Tempo against Danceability
fig2 = px.scatter(playlist, x=playlist['Tempo'], y=playlist['Danceability'],
                color = playlist['Popularity'], size=playlist['Popularity'], 
                title = 'Scatter Plot of Song Popularity using Tempo against Danceability')
fig2.write_image('./Images/Scatter_Tempo_Dance.png')

# scatter graph of Popularity using Loudness against Valence
fig2 = px.scatter(playlist, x=playlist['Valence'], y=playlist['Loudness'],
                color = playlist['Popularity'], size=playlist['Popularity'], 
                title = 'Scatter Plot of Song Popularity using Valence against Loudness')
fig2.write_image('./Images/Scatter_Loudness_Valence.png')

# normalize length in minutes:seconds
playlist['Length'] = (playlist['Length'])/1000/60

# scatter graph of Popularity using Length against Release Date
fig2 = px.scatter(playlist, x=playlist['Length'], y=playlist['Release-Date'],
                color = playlist['Popularity'], size=playlist['Popularity'], 
                title = 'Scatter Plot of Song Popularity using Length against Release Date')
fig2.write_image('./Images/Scatter_Length_Release.png')

# scatter graph of Popularity using Acousticness against Liveness
fig2 = px.scatter(playlist, x=playlist['Acousticness'], y=playlist['Liveness'],
                color = playlist['Popularity'], size=playlist['Popularity'], 
                title = 'Scatter Plot of Song Popularity using Acousticness against Liveness')
fig2.write_image('./Images/Scatter_Acousticness_Liveness.png')


#----------------------------------------------------------------------------------#


#polar graph

#normalize loudness
playlist['Loudness'] = (playlist['Loudness'] +60 )/60

#normalize tempo
playlist['Tempo'] = playlist['Tempo']/200

#set features to be displayed
columns_for_polar = playlist.columns.intersection(['Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 
                                                'Liveness', 'Loudness', 'Speechiness', 'Tempo', 'Valence'])
features_data = playlist[columns_for_polar]
features_mean = features_data.mean().tolist()

#subset of the most popular songs
highest_sub = playlist.loc[lambda playlist: playlist['Popularity'] >= 90].sort_values(by=['Popularity'])
highest_sub.head()

features_data_highest = highest_sub[columns_for_polar]
features_mean_highest = features_data_highest.mean().tolist()

labels = list(features_data)[:]

#graph settings and export
angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
fig = plt.figure(figsize = (18,18))

ax = fig.add_subplot(221, polar=True)
ax.plot(angles, features_mean, 'o-', linewidth=2, label = "All the songs", color= 'blue')
ax.fill(angles, features_mean, alpha=0.25, facecolor='blue')
ax.set_thetagrids(angles * 180/np.pi, labels , fontsize = 13)

ax.set_rlabel_position(250)
plt.yticks([0.1 , 0.2 , 0.3 , 0.4, 0.5,  0.6, 0.7, 0.8, 0.9,1.0], ["0.1",'0.2', "0.3", "0.4", "0.5", "0.6", '0.7', '0.8', '0.9', '1.0'], size=12)
plt.ylim(0,1.0)

ax.plot(angles, features_mean_highest, 'o-', linewidth=2, label = "Most popular", color= 'orange')
ax.fill(angles, features_mean_highest, alpha=0.25, facecolor='orange')
ax.set_title('Mean Values')
ax.grid(True)

plt.legend(loc='best', bbox_to_anchor=(0.1, 0.1))

plt.savefig('./Images/Polar_MeanValues.png')