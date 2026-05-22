import os
import pandas as pd
import numpy as np 
import time
from metrics import AdjustR2, R2, RMSE, MAE

class LinearRegressionRaw:
    def __init__(self):
        self.theta = None 
        
    def fit(self, X, y):       
        # Chèn thêm một cột toàn số 1 vào ma trận X để tính hệ số chặn Bias
        X_b = np.c_[np.ones((X.shape[0], 1)), X]
               
        # Công thức chuẩn tắc OLS nguyên bản: theta = (X^T * X)^(-1) * X^T * y
        X_transpose = X_b.T
        self.theta = np.linalg.inv(X_transpose.dot(X_b)).dot(X_transpose).dot(y)

    def predict(self, X):      
        X_b = np.c_[np.ones((X.shape[0], 1)), X]
        return X_b.dot(self.theta)

if __name__ == "__main__":   
    current_dir = os.path.dirname(os.path.abspath(__file__))       
    pca_data_path = os.path.normpath(os.path.join(current_dir, "..", "..", "..", "data", "processed", "pca_data.csv"))
    clean_data_path = os.path.normpath(os.path.join(current_dir, "..", "..", "..", "data", "processed", "clean_data.csv"))
    
    if not os.path.exists(pca_data_path) or not os.path.exists(clean_data_path):
        print("⚠️ Không tìm thấy file dữ liệu tại thư mục data/processed!")
    else:
        print("========== KHỞI CHẠY LINEAR REGRESSION RAW (100% DATA) ==========")
        X = pd.read_csv(pca_data_path).values.astype(float)
        y = pd.read_csv(clean_data_path)['mat_final_price'].values.astype(float)
        
        # Xáo trộn dữ liệu đồng bộ bằng Seed 42
        np.random.seed(69)
        indices = np.arange(X.shape[0])
        np.random.shuffle(indices)
        X, y = X[indices], y[indices]
        
        # Chia tách tập Train/Test theo tỷ lệ 80/20 hình thức thủ công
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        print(f"Kích thước nạp vào - Train: {X_train.shape}, Test: {X_test.shape}")
        
        # ĐO THỜI GIAN HUẤN LUYỆN ĐẠI SỐ
        t0 = time.time()
        model = LinearRegressionRaw()
        model.fit(X_train, y_train)
        train_time = time.time() - t0
        
        # ĐO THỜI GIAN DỰ ĐOÁN
        t1 = time.time()
        y_pred = model.predict(X_test)
        pred_time = time.time() - t1
        
        # Tính toán các chỉ số đánh giá bằng file metrics.py tự chế
        N = len(y_test)
        mean_y_test = np.full(N, np.mean(y_test))
        rmse_val = RMSE(N, y_test, y_pred, 0)
        r2_val = R2(N, y_test, y_pred, mean_y_test, 0)
        mae_val = MAE(N, y_test, y_pred, 0)
        
        print("\n" + "="*50)
        print(" KẾT QUẢ ĐÁNH GIÁ LINEAR REGRESSION THÔ SƠ TỰ CHẾ")
        print("="*50)
        print(f"Thời gian huấn luyện (Train Time) : {train_time:.4f} giây")
        print(f"Thời gian dự đoán (Predict Time) : {pred_time:.4f} giây")
        print(f"Hệ số chặn (Intercept)           : {model.theta[0]:.4f}")
        print("-" * 50)
        print(f"Mean Absolute Error (MAE)        : {mae_val:.2f} (cents)")
        print(f"Root Mean Squared Error (RMSE)   : {rmse_val:.2f}")
        print(f"R-squared (R2)                   : {r2_val:.4f}")
        print("="*50)