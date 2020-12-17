from spotify.get_service.spoti_service import *
from spotify.pl_builder.get_playlist import *
import pandas as pd

def spoti_playlist(playlist_uri):

    next_workout_pred = pd.read_csv('model/predictions/prediction.csv')
    next_workout_pred.set_index('acc_time', inplace=True)
    next_workout_pred.index = pd.to_datetime(next_workout_pred.index).to_period('min')

    sp_user, sp_auth = get_oauth() 
    
    get_playlist(sp_user, sp_auth, playlist_uri, next_workout_pred)