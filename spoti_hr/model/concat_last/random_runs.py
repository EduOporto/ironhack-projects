import random
import datetime
import numpy as np
import os

def random_runs(df, n_runs, days_ago):

    if n_runs <= days_ago:
        # Get the actual date of the request
        today = datetime.datetime.today()

        # List of possible days that will be picked at random from the recent date to days_ago
        date_list = [today - datetime.timedelta(days=x) for x in range(days_ago)]

        files = os.listdir('../spoti_hr/google_fit/heart_rates_data/running_datasets')
        arch_dates = [e.split('.')[0] for e in files if e.split('.')[0] != '']
        arch_sorted = sorted([datetime.datetime.strptime(e, "%Y_%m_%d").date() for e in arch_dates])[-10:]

        for date in arch_sorted:
            if date in date_list:
                date_list.remove(date)

        
        rand_var = [0]*40+list(range(4))

        for _ in range(n_runs):

            begginig = df['bpm'].to_list()[:40]
            to_chunk = df['bpm'].to_list()[40:]

            chunked = np.array_split(to_chunk, random.choice(range(5,11)))
            random.shuffle(chunked)
            chunked = list(np.concatenate(chunked))

            vals_mod = begginig + chunked

            ops = ['+', '-']
            new_vals = []
            for e in vals_mod:
                num2 = random.choice(rand_var)
                operation = random.choice(ops)
            
                new_vals.append(eval(str(e) + operation + str(num2)))

            df['bpm'] = new_vals
            
            popped = date_list.pop(random.choice(range(len(date_list)))).date()
            
            df.to_csv(f'../spoti_hr/google_fit/heart_rates_data/running_datasets/{popped.year}_{popped.month}_{popped.day}.csv')

        return f"""
    \nDatasets generated"""

    else:
        return f"""
    \nNumber of runs cannot be greater than argument 'days_ago'"""
