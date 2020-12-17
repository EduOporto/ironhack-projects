import gfit_data_extrac.date_format as dtb
import pandas as pd

def distance(service, startDate, endDate, sourceId):
    # Function that given a Google Fit API service, a range of dates of a given session and a sourceId
    # returns a dataframe with the distance values (in meters) registered for that session

    # API query with the given dates
    req = service.users().dataSources().datasets().get(userId='me', 
                                                   dataSourceId=sourceId,
                                                   datasetId=f"{dtb.mill_to_nano(startDate)}-{dtb.mill_to_nano(endDate)}").execute()

    # Get the list of the dates of the different heart BPM registered (needs to convert dates from 
    # nanoseconds epoch to date format)
    start_point = [dtb.nano_to_date(int(e['startTimeNanos'])) for e in req['point']]
    end_point = [dtb.nano_to_date(int(e['endTimeNanos'])) for e in req['point']]
    distance = [int(e['value'][0]['fpVal']) for e in req['point']]

    return pd.DataFrame({'startTime':start_point, 'endTime':end_point, 'distance_m':distance})