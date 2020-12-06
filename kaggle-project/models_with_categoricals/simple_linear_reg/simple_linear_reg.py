import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def linear_model_tt(X, y, test_size):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
    
    fit_lr = LinearRegression().fit(X_train, y_train)
    
    y_train_pred = fit_lr.predict(X_train)
    y_test_pred = fit_lr.predict(X_test)
    
    return y_train, y_test, y_train_pred, y_test_pred

def lr_results(train_real, test_real, train_pred, test_pred):
    r2_train = r2_score(train_real, train_pred)
    r2_test = r2_score(test_real, test_pred)
    
    mae_train = mean_absolute_error(train_real, train_pred)
    mae_test = mean_absolute_error(test_real, test_pred)
    
    rmse_train = mean_squared_error(train_real, train_pred)**.5
    rmse_test = mean_squared_error(test_real, test_pred)**.5

    results = {'train_set': [r2_train, mae_train, rmse_train], 
               'test_set': [r2_test, mae_test, rmse_test]}
    
    results_df = pd.DataFrame(results, index=['r2', 'mae', 'rmse'])
    
    return results_df