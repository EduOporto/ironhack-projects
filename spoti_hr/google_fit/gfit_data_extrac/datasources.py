import pandas as pd

def datasources(service):
    # Given a Google Fit API authorization service, it returns a dataframe with all the datasources 
    # registred in the API database that are related to the Xiaomi MiBand 3

    # API query for all the datasources
    datasources = service.users().dataSources().list(userId='me').execute()
    
    # Filter the results for those related to Mi Band 3
    miband = [e for e in datasources['dataSource'] 
                if 'application' in e and 
                'packageName' in e['application'] and 
                (e['application']['packageName'] == 'com.huami.watch.hmwatchmanager' or 
                e['application']['packageName'] == 'com.mc.miband1')]

    # Building the dataframe
    data_dict = {'dataStreamId': [e['dataStreamId'] for e in miband], # Dataource ID
                'dataStreamName': [e['dataStreamName'] for e in miband], # Datasource Name
                'dataType_name': [e['dataType']['name'] for e in miband], # Datasource Type
                'dataType_pack': [e['application']['packageName'] for e in miband], # Datasource Pack
                'dataType_fieldname': [e['dataType']['field'][0]['name'] for e in miband]} # Type of data

    return pd.DataFrame(data_dict)