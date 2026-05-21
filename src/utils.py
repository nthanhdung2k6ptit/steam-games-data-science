import os
import joblib

def save_model(model, path):
	directory = os.path.dirname(path)
	if directory and not os.path.exists(directory):
		os.makedirs(directory, exist_ok=True)
	joblib.dump(model, path)
	print(f"Model saved to {path}")

