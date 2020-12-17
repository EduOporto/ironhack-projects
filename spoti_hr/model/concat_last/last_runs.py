import os
import datetime
import pandas as pd
import numpy as np
from model.concat_last.random_runs import *

def concat_last():
    files = os.listdir('../spoti_hr/google_fit/heart_rates_data/running_datasets')
    arch_dates = [e.split('.')[0] for e in files if e.split('.')[0] != '']
    arch_sorted = sorted([datetime.datetime.strptime(e, "%Y_%m_%d").date() for e in arch_dates])[-10:]

    if len(arch_sorted) >= 10:

        last_ten = [e.strftime("%Y_%m_%-d") for e in arch_sorted]
        frames = pd.DataFrame({'acc_time': [], 'bpm': []})

        for csv, day in zip(last_ten, list(range(0,10))):
            df = pd.read_csv(f'../spoti_hr/google_fit/heart_rates_data/running_datasets/{csv}.csv')
            
            df.acc_time = pd.to_timedelta(df.acc_time) + datetime.timedelta(days=day)

            frames = pd.concat([frames, df], ignore_index=True)
        
        frames.set_index('acc_time', inplace=True)

        return pd.DataFrame(frames.bpm)

    elif len(arch_sorted) < 10:
        print("""\n
    There are not enough workouts registered.
    I am creating new random ones based on your last workout!""")

        last_date = str(arch_sorted[-1]).replace('-', '_')
        
        to_random = pd.read_csv(f'../spoti_hr/google_fit/heart_rates_data/running_datasets/{last_date}.csv')
        number = 10 - len(arch_sorted)

        random_runs(to_random, number, 20)

        return concat_last()


