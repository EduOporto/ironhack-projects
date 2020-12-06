import pandas as pd 
from poly_lasso_cv import poly_lasso_cv
from sklearn.preprocessing import MinMaxScaler

diamonds = pd.read_csv('models_with_categoricals/data/train_cate.csv')

X = diamonds.iloc[:,1:-1]
y = diamonds.price

mae_dict, rmse_dict, rsquare_dict = poly_lasso_cv(1, 5, X, y, .2)


print('Worked')


