import numpy as np

class LinearRegressionRaw:
    def __init__(self):
        self.theta = None 
        
    def fit(self, X, y):                     
        X_b = np.c_[np.ones((X.shape[0], 1)), X]                              
        X_transpose = X_b.T
        self.theta = np.linalg.inv(X_transpose.dot(X_b)).dot(X_transpose).dot(y)

    def predict(self, X):      
        X_b = np.c_[np.ones((X.shape[0], 1)), X]
        return X_b.dot(self.theta)
