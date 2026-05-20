import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

def train_classification_model(X_train, y_train, model_type = 'rfc'):
    if model_type == 'rfc':
        model = RandomForestClassifier(n_estimators=100, random_state=67, class_weight='balanced')
    else:
        model = LogisticRegression(max_iter=1000, class_weight='balanced')
    model.fit(X_train, y_train)
    return model
