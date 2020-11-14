from eurostatapiclient import EurostatAPIClient
import pandas as pd
import os

VERSION = 'v2.1'
FORMAT = 'json'
LANGUAGE = 'en'

client = EurostatAPIClient(VERSION, FORMAT, LANGUAGE)
dir_path = os.path.dirname(os.path.realpath(__file__))

querys = {'median_age_by_nuts3': 'demo_r_pjanind3?geoLevel=nuts3&indic_de=MEDAGEPOP&precision=1&unit=YR&time=2019',
          'young_pop_rate_nuts3': 'demo_r_pjanind3?geoLevel=nuts3&indic_de=PC_Y0_14&indic_de=PC_Y25_44&precision=2&unit=PC&time=2019',
          'primry_std_nuts2': 'educ_uoe_enra11?geoLevel=nuts2&precision=2&sex=T&unit=NR&isced11=ED0&isced11=ED1&isced11=ED2&time=2018',
          'earlysec_std_nuts2': 'educ_uoe_enra15?geoLevel=nuts2&precision=2&unit=RT&isced11=ED02-8&isced11=ED1_2&time=2018',
          'kinder_std_nuts2': 'educ_uoe_enra14?geoLevel=nuts2&precision=2&unit=RT&time=2018&age=Y4'}

for name, query in querys.items():
    q_dataset = client.get_dataset(query)
    q_dataframe = q_dataset.to_dataframe()
    q_dataframe.to_csv(f"{dir_path}/{name}.csv", index=False)