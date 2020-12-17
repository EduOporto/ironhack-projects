from model.concat_last.last_runs import *
from model.concat_last.min_registers import first_of_minute
from model.ARIMA.grid_search import *
from model.ARIMA.model import *

def prediction():
    last_ten = concat_last()

    minreg_df = first_of_minute(last_ten).to_period('min')
    rows_n = minreg_df['1970-01-01'].shape[0]
    
    order, seasonal_order = (1, 1, 1), (0, 1, 1, rows_n) #grid_search(minreg_df)

    get_prediction(minreg_df, order, seasonal_order)