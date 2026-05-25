from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

def train_classification_model(X_train, y_train, model_type = 'rfc'):
    if model_type == 'rfc':
        model = RandomForestClassifier()
    else:
        model = KNeighborsClassifier()
    model.fit(X_train, y_train)
    return model
