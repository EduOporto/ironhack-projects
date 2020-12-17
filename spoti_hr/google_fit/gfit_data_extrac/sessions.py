from google_fit.gfit_data_extrac.activityTypes_df import types_df
import google_fit.gfit_data_extrac.date_format as dtb
from google_fit.gfit_data_extrac.heart_rate import heart_rate
import pandas as pd
import datetime
import pytz
import os

def sessions(service, days_ago):
    # Given a Google Fit API authorization service and a number of days from which the user wants to see 
    # his/her activities (sessions), it returns a dataframe listing all of them, ordered from most recent
    # to less, giving type of activity, start and end dates and Google Fit API package name

    # Get the actual date of the request
    d = datetime.datetime.utcnow()
    d_with_timezone = d.replace(tzinfo=pytz.UTC)
    now = d_with_timezone.isoformat()

    # Get the date from which the user wants to list the activities
    date_days_ago = (d_with_timezone - datetime.timedelta(days=days_ago)).isoformat()

    # API query for the activities
    sess_req = service.users().sessions().list(userId='me', 
                                                startTime=date_days_ago, 
                                                endTime=now, 
                                                includeDeleted=False).execute()['session']

    # Building the dataframe
    sessions_df = pd.DataFrame({'activityType': [e['activityType'] for e in sess_req], 
                                'startDate': [dtb.mill_to_date(int(e['startTimeMillis'])) for e in sess_req],
                                'startDate_mill': [int(e['startTimeMillis']) for e in sess_req],
                                'endDate': [dtb.mill_to_date(int(e['endTimeMillis'])) for e in sess_req],
                                'endDate_mill': [int(e['endTimeMillis']) for e in sess_req],
                                'packName': [e['application']['packageName'] for e in sess_req]})

    # Getting activities by its name (Google API returns this data by its ID number)
    sessions_df.activityType = sessions_df.activityType.apply(lambda x: types_df(x))

    # Sorting the values by date (DESCENDING)
    sessions_df.sort_values(by=['startDate'], ascending=False, inplace=True)

    runs = sessions_df[(sessions_df.activityType == 'Running') & (sessions_df.packName == 'com.mc.miband1')]

    print("""\n
    Checking for unregistered workouts...""")
    updates = 0
    for run in runs.iterrows():
        full_date = run[1]['endDate'].date()
        date = f"{full_date.year}_{full_date.month}_{full_date.day}"
        
        if os.path.exists(f"google_fit/heart_rates_data/running_datasets/{date}.csv"):
            pass
        else:
            updates += 1
            print(f"""\n
            Updating workout on {date}""")
            start_date = run[1]['startDate_mill']
            end_date = run[1]['endDate_mill']
            source_hr = 'raw:com.google.heart_rate.bpm:com.mc.miband1:Xiaomi:Mi Band 3:b0a299a0:Notify for Mi Band - workout heart'
            
            heart_rate(service, start_date, end_date, source_hr, date)

    return """\n
    All your workouts are up to date!""", updates
