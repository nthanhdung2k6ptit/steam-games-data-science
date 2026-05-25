from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

def train_regression_model(X_train, y_train, model_type='rf'):   
    if model_type == 'rf':
        model = RandomForestRegressor()
    else:
        model = LinearRegression()
        
    model.fit(X_train, y_train)
    return model

