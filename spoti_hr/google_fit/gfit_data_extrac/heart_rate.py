import google_fit.gfit_data_extrac.date_format as dtb
import pandas as pd
import numpy as np

def heart_rate(service, startDate, endDate, sourceId, date_to_save):
    # Function that given a Google Fit API service, a range of dates of a given session and a sourceId
    # returns a dataframe with the heart BPM values registered for that session

    # API query with the given dates
    req = service.users().dataSources().datasets().get(userId='me', 
                                                   dataSourceId=sourceId,
                                                   datasetId=f"{dtb.mill_to_nano(startDate)}-{dtb.mill_to_nano(endDate)}").execute()

    # Get the list of the dates of the different heart BPM registered (needs to convert dates from 
    # nanoseconds epoch to date format)
    dates = [dtb.nano_to_date(int(e['startTimeNanos'])) for e in req['point']]

    # List of the BPM registered
    bpm = [e['value'][0]['fpVal'] for e in req['point']]

    df = pd.DataFrame({'acc_time': dates, 'bpm': bpm})
    df['acc_time'] = dtb.date_to_periods(df['acc_time'])
    df.set_index('acc_time', inplace=True)

    df.index = df.index.astype(np.int64)
    df.to_csv(f"google_fit/heart_rates_data/running_datasets/{date_to_save}.csv")

    return f"Heart data for your workout on {date_to_save} succesfully registered!"