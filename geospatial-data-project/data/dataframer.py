import pandas as pd
import os

from pymongo import MongoClient
client = MongoClient()
db = client.get_database('companies_project')

offices_filter3 = list(db.companies_usa_filt5_c.find({}, {'offices':1}))

offices = {'latitude': [], 'longitude': [], 'city': [], 'state': []}
schools = {'latitude': [], 'longitude': [], 'name': [], 'rating': []}
companies = {'_id': [], 'latitude': [], 'longitude': []}
airports = {'latitude': [], 'longitude': [], 'name': [], 'distance': []}

for off in offices_filter3:
    offices['latitude'].append(off['offices']['latitude'])
    offices['longitude'].append(off['offices']['longitude'])
    offices['city'].append(off['offices']['city'])
    offices['state'].append(off['offices']['state_code'])

    for school in off['offices']['schools']:
        schools['latitude'].append(off['offices']['schools'][str(school)]['geometry']['location']['lat'])
        schools['longitude'].append(off['offices']['schools'][str(school)]['geometry']['location']['lng'])
        schools['name'].append(off['offices']['schools'][str(school)]['name'])
        schools['rating'].append(off['offices']['schools'][str(school)]['rating'])

    for company in off['offices']['off_nearby']:
        if company != 'many':
            companies['_id'].append(off['offices']['off_nearby'][company]['_id'])
            companies['latitude'].append(off['offices']['off_nearby'][company]['coord']['coordinates'][1])
            companies['longitude'].append(off['offices']['off_nearby'][company]['coord']['coordinates'][0])

    for airport in off['offices']['airports']:
        if airport != 'mean_dist':
            airports['latitude'].append(off['offices']['airports'][airport]['Position']['Coordinate']['Latitude'])
            airports['longitude'].append(off['offices']['airports'][airport]['Position']['Coordinate']['Longitude'])
            airports['name'].append(off['offices']['airports'][airport]['Names']['Name']['name'])
            airports['distance'].append(off['offices']['airports'][airport]['Distance']['Value'])




offices_df = pd.DataFrame.from_dict(offices)
schools_df = pd.DataFrame.from_dict(schools)
companies_df = pd.DataFrame.from_dict(companies)
airports_df = pd.DataFrame.from_dict(airports)

offices_df.to_csv("offices_f5.csv", index=False)
schools_df.to_csv("schools_f5.csv", index=False)
companies_df.to_csv("companies_f5.csv", index=False)
airports_df.to_csv("airports_f5.csv", index=False)