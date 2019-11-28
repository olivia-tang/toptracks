# -*- coding: utf-8 -*-
"""
Created by: Olivia Tang
Date: 11/27/2019

Gathers audio metrics for top 50 tracks of Spotify user exports to data to
.xlsx file.
Created using Spotipy module. 
"""


import sys
import spotipy
import pandas as pd
import spotipy.util as util



# Get user authorization and read in user's top 50 tracks

client_id = ''
client_secret = ''
client_username = ''

scope = 'user-library-read'
if len(sys.argv) > 1:
    username = sys.argv[1]
else :
    sys.exit()

token = util.prompt_for_user_token(username, scope, client_id = client_id,
                                   client_secret = client_secret)

if token: 
    sp = spotipy.Spotify(auth=token)
else:
    print("Can't get token for", username)
cache_token = token.get_access_token()

sp = spotipy.Spotify(cache_token)

#medium term = approx. last 6 months
top_tracks = sp.current_user_top_tracks(limit=50, offset=0, 
                                        time_range = 'medium_term')

track_IDs = [] #create list to store IDs of each track in top 50 songs

for n in range (len(top_tracks['items'])) : #for each track
    track_IDs.append(top_tracks['items'][n]['id'])
    
    
#get audio features (danceability, energy, valence) for each track
def get_features(track_IDs) :
    #Create empty lists to store audio features for each track
    track_IDs['danceability'] = []
    track_IDs['energy'] = []
    track_IDs['valence'] = []

    for track in track_IDs['id'] :
        #pull audio features per track
        features = sp.audio_features(track)
        
        #append to relevant feature list
        track_IDs['danceability'].append(features[0]['danceability'])
        track_IDs['energy'].append(features[0]['energy'])
        track_IDs['valence'].append(features[0]['valence'])


#organize data into dataframe
dic_df = {}
dic_df['danceability'] = []
dic_df['energy'] = []
dic_df['valence'] = []

for feature in track_IDs:
    dic_df[feature].extend(track_IDs[feature])

#convert to dataframe
df = pd.DataFrame.from_dict(dic_df)

#convert to excel file
df.to_excel('INSERT FILE PATH HERE\top_tracks.xlsx', index=None, header=True)

        
        
        
