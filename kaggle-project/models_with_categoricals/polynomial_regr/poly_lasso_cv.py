from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LassoCV
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def poly_lasso_cv(min_degree, max_degree, X, y, test_size):
    mae_dict = {'train': [], 'test': [], 'all': []}
    rmse_dict = {'train': [], 'test': [], 'all': []}
    rsquare_dict = {'train': [], 'test': [], 'all': []}
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)

    for degree in range(min_degree,max_degree+1):
        model = make_pipeline(PolynomialFeatures(degree, 
                                                 interaction_only=False), 
                              LassoCV(eps=0.0001,
                                      n_alphas=20,
                                      max_iter=5000, 
                                      normalize=True,cv=5))
        model.fit(X_train,y_train)

        train_pred = model.predict(X_train) 
        test_pred = model.predict(X_test)
        all_pred = model.predict(X)

        mae_dict['train'].append(mean_absolute_error(y_train, train_pred))
        mae_dict['test'].append(mean_absolute_error(y_test, test_pred))
        mae_dict['all'].append(mean_absolute_error(y, all_pred))

        rmse_dict['train'].append(mean_squared_error(y_train, train_pred)**.5)
        rmse_dict['test'].append(mean_squared_error(y_test, test_pred)**.5)
        rmse_dict['all'].append(mean_squared_error(y, all_pred)**.5)

        rsquare_dict['train'].append(r2_score(y_train, train_pred))
        rsquare_dict['test'].append(r2_score(y_test, test_pred))
        rsquare_dict['all'].append(r2_score(y, all_pred))
        
    return mae_dict, rmse_dict, rsquare_dict