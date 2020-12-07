from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LassoCV
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

## Function for the Polynomial Regression with LassoCV pipeline
## It gets the min and max degrees for the Polynomial Regression, 
## an X and a y and the size of the test data

def poly_lasso_cv(min_degree, max_degree, X, y, test_size):
    
    # Dicts for saving the results
    mae_dict = {'train': [], 'test': [], 'all': []}
    rmse_dict = {'train': [], 'test': [], 'all': []}
    rsquare_dict = {'train': [], 'test': [], 'all': []}
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)

    for degree in range(min_degree,max_degree+1):
        # Pipeline with two functions: the PolynomialFeatures and the LassoCV
        model = make_pipeline(PolynomialFeatures(degree, 
                                                interaction_only=False), 
                            LassoCV(eps=0.001,
                                    n_alphas=100,
                                    max_iter=5000, 
                                    normalize=True,
                                    cv=10,
                                    tol=0.0001,
                                    verbose=0))
        model.fit(X_train,y_train)

        # Predictions
        train_pred = model.predict(X_train) 
        test_pred = model.predict(X_test)
        all_pred = model.predict(X)

        # Results appended to the dictionaries
        mae_dict['train'].append(mean_absolute_error(y_train, train_pred))
        mae_dict['test'].append(mean_absolute_error(y_test, test_pred))
        mae_dict['all'].append(mean_absolute_error(y, all_pred))

        rmse_dict['train'].append(mean_squared_error(y_train, train_pred)**.5)
        rmse_dict['test'].append(mean_squared_error(y_test, test_pred)**.5)
        rmse_dict['all'].append(mean_squared_error(y, all_pred)**.5)

        rsquare_dict['train'].append(r2_score(y_train, train_pred))
        rsquare_dict['test'].append(r2_score(y_test, test_pred))
        rsquare_dict['all'].append(r2_score(y, all_pred))

        # Print which degree has been completed, in order to give the user the status of the process
        print(f"Degree {degree} calculated")

    # Return the dictionaries with the results              
    return mae_dict, rmse_dict, rsquare_dict

## Function for the predictions of the test dataset (Diamonds without prices)
## It gets the X and y from the dataset with prices, the degree of the Polynomial Regression the user 
## wants to give it and the dataframe without the prices (test dataframe) 

def poly_lasso_cv_pred(X_t, y_t, degree, X_p):

    model = make_pipeline(PolynomialFeatures(degree, 
                                            interaction_only=False), 
                        LassoCV(eps=0.0001,
                                n_alphas=20,
                                max_iter=5000, 
                                normalize=True,cv=5))
    
    model.fit(X_t,y_t)

    prediction = model.predict(X_p)

    return prediction