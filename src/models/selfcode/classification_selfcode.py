import numpy as np

class KNNClassifierRaw:
    def __init__(self, k=5):
        self.k = k
        self.X_train = None
        self.y_train = None

    def fit(self, X, y):       
        self.X_train = X
        self.y_train = y

    def predict(self, X_test):        
        predictions = []
        
        for x_test in X_test:           
            distances = np.sqrt(np.sum((self.X_train - x_test) ** 2, axis=1))          
            k_indices = np.argsort(distances)[:self.k]
            k_nearest_labels = self.y_train[k_indices]                     
            labels, counts = np.unique(k_nearest_labels, return_counts=True)
            most_common = labels[np.argmax(counts)]
            predictions.append(most_common)
                
        return np.array(predictions)