from google_fit.gfit_service.gfit_service import *
from google_fit.gfit_data_extrac.sessions import *

from model.prediction import *
from spotify.spotify import *

def welcome():
    print("""\n                                 WELCOME TO THE SPOTIFY-HEART APP! 
    
    With this app, you will be able to improve the order of the music you listen when doing excercise.
    
    How is so? Easy. The APP will take the data related to you heart beating collected by your MiBand
    in your last 10 workouts, and from that, it will predict how your heart rate will be in your next run. 
    
    Given that data, and the Spotify playlist you would like to listen in your next workout, the APP
    will sort the songs in order to adapt them to your pace.""")

    user_choice = int(input("""\n
    What would you like to do?
            
        1. Update your workouts
        2. Create a new playlist
        3. Exit

    Type the number of your option here: """))

    if user_choice == 1:
        g_service = create_fit_service()

        info, updates = sessions(g_service, 30)
    
        if updates > 0:
            if updates == 1:
                print(f"""\n
    I have added {updates} new workout to my database, let me now build a new prediction for your next workout!""")
            if updates > 1:
                print(f"""\n
    I have added {updates} new workouts to my database, let me now build a new prediction for your next workout!""")
            
            prediction()
        
        print(info)
        
        user_choice = int(input("""\n
    What would you like to do?
            
        1. Create a new playlist
        2. Exit
            
    Type the number of your option here: """))

        if user_choice == 1:
            playlist = str(input("""\n
    Great! Just give me the playlist URI, I will do the rest: """))

            spoti_playlist(playlist)
        if user_choice == 2:
            print("""\n
    Sure! See you next time!""")


    elif user_choice == 2:
        playlist = str(input("""\n
    Great! Just give me the playlist URI, I will do the rest: """))

        spoti_playlist(playlist)
    elif user_choice == 3:
        print("""\n
    Sure! See you next time!""")

welcome()
    




