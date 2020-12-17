import pandas as pd
import numpy as np
import datetime
import random
import time
from tqdm import tqdm

pd.options.mode.chained_assignment = None 

def get_playlist(user, oauth, playlist_uri, prediction):

    # Get list of playlist's songs
    playlist_songs = [e['track']['uri'] for e in oauth.playlist_tracks(playlist_uri)['items']]

    # Get lenght and tempo of the songs, and join all in a dataframe
    playlist_dict = {'uri': playlist_songs, 'length': [], 'tempo': []}
    
    for song in playlist_songs:
        analysis = oauth.audio_analysis(song)
        playlist_dict['length'].append(analysis['track']['duration'])
        playlist_dict['tempo'].append(analysis['track']['tempo'])
    playlist_df = pd.DataFrame(playlist_dict)

    # Through the mean length of the playlist in rounded minutes, get an stimation of what the heart BPM
    # will be in the intervals between a song finishes and a new one starts 
    playlist_mean = round(playlist_df.length.mean() / 60)
    time_intervals = prediction[prediction.index.minute % playlist_mean == 0]

    # SONG SELECTION
    # Create a dict with each of the intervals as keys and empty lists as values, and a list with the
    # number of elements, in order to control the loop through the songs
    range_box = {}
    for i in range(time_intervals.shape[0]):
        range_box[i] = []
    lenght_range_box = list(range(len(range_box)))

    # Accumulator of the ranges. The loop starts with a range of 3 BPM more and less of the predicted BPM 
    # for that interval. After that loop is done, this range increases to 6, 9, 12 and so one, until 
    # the loop has chosen two songs for each of the intervals 
    ranger = 3

    # Once the loop has chosen two song for a given interval, those go to this empty dict and disappear 
    # from 'range_box'
    final_choices = {}

    # This while loop stops when all the intervals have two songs assigned
    while len(lenght_range_box) > 0:
        # Iterating through the time intervals
        for time, ran in zip(time_intervals.iterrows(), lenght_range_box):
            
            # Building the interval
            interval = pd.Interval(left=time[1]['predicted_mean']-ranger,
                                right=time[1]['predicted_mean']+ranger,
                                closed='both')
            
            # List of the songs that fit for the BPM interval of the time iterated
            songs_chosen = [e for e in playlist_df.iterrows() if e[1]['tempo'] in interval]

            try:
                # If there are songs available, pick a random one, assign it to 'range_box' and drop it 
                # from the song's dataframe
                song = random.choice(songs_chosen)
                range_box[ran].append(song[1]['uri'])
                playlist_df.drop(song[0], inplace=True)                
            except:
                # Pass if there are no songs available
                pass
            
            # Check wether the iterated time interval has been filled with two songs. If so, assign it to
            # the dict of 'final_choices' and drop it from the time_intervals dataframe and the control list
            if len(range_box[ran]) == 2:
                final_choices[ran] = range_box[ran]
                    
                #del range_box[ran]
                lenght_range_box.remove(ran)
                time_intervals.drop(time[0], inplace=True)
            
        # Increase the ranges of the BPMs +3
        ranger += 3
    
    # Sort the results by time intervals, placing the first song of each list first, and the second second.
    # Join both lists and the leftovers of the given playlist at the end
    choice_sorted = sorted(final_choices.items())
    choice_ready = [e[1][0] for e in choice_sorted] + [e[1][1] for e in choice_sorted] + playlist_df.uri.to_list()

    # Create the playlist on the user's profile, with the actual date as name
    year, month, day = datetime.date.today().year, datetime.date.today().month, datetime.date.today().day
    playlist_id = oauth.user_playlist_create(user, name=f'Playlist for workout {year}-{month}-{day}')['id']

    # Fill the playlist with the songs in the selected order
    oauth.user_playlist_add_tracks(user, playlist_id, choice_ready)

    print(f"""
        \nPlaylist succesfully generated in your library, 
    search for it as 'Playlist for workout {year}-{month}-{day}' 
    
    ENJOY YOUR WORKOUT!""")

