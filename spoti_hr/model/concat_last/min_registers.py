import numpy as np
import pandas as pd

def first_of_minute(df):
    df.index = pd.to_datetime(df.index.astype(np.int64))

    just_minutes = []
    min_first_reg = {}

    for acc, bpm in df.iterrows():
        if acc.day not in min_first_reg:
            min_first_reg[acc.day] = []
        if acc.minute not in min_first_reg[acc.day]:
            min_first_reg[acc.day].append(acc.minute)
            just_minutes.append((acc, bpm['bpm']))
        else:
            pass
        
    minreg_df = pd.DataFrame(just_minutes, columns=["acc_time", "bpm"])
    minreg_df.set_index('acc_time', inplace=True)

    return minreg_df