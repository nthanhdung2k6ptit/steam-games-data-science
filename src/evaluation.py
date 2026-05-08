import numpy as np
import pandas as pd
from sklearn.metrics import (
    mean_squared_error, r2_score, mean_absolute_error,
    accuracy_score, classification_report, confusion_matrix
)

def evaluate_regression(y_true, y_pred, model_name="Model"):    
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    
    print(f"--- {model_name} Regression Metrics ---")
    print(f"RMSE: {rmse:.4f}")
    print(f"MAE:  {mae:.4f}")
    print(f"R2:   {r2:.4f}")
    
    return {"rmse": rmse, "mae": mae, "r2": r2}

def evaluate_classification(y_true, y_pred, model_name="Model"):
    acc = accuracy_score(y_true, y_pred)
    
    print(f"--- {model_name} Classification Metrics ---")
    print(f"Accuracy: {acc:.4f}")
    print("\nDetailed Classification Report:")
    print(classification_report(y_true, y_pred))
    
    return {"accuracy": acc}