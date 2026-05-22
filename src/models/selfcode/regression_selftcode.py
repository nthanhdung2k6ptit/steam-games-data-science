import os
import pandas as pd
import numpy as np 
from metrics import AdjustR2, R2, RMSE, MAE

class LinearRegressionFromScratch:
    def __init__(self):
        self.theta = None 
        
    def fit(self, X, y):              
        X_b = np.c_[np.ones((X.shape[0], 1)), X]
               
        X_transpose = X_b.T
        self.theta = np.linalg.inv(X_transpose.dot(X_b)).dot(X_transpose).dot(y)
        print("Mô hình đã được huấn luyện thành công bằng phương trình chuẩn tắc từ dữ liệu PCA!")
        
    def predict(self, X):      
        X_b = np.c_[np.ones((X.shape[0], 1)), X]
        return X_b.dot(self.theta)

if __name__ == "__main__":   
    current_dir = os.path.dirname(os.path.abspath(__file__))       
        
    pca_data_path = os.path.normpath(os.path.join(current_dir, "..", "..", "..", "data", "processed", "pca_data.csv"))
    clean_data_path = os.path.normpath(os.path.join(current_dir, "..", "..", "..", "data", "processed", "clean_data.csv"))
    
    if not os.path.exists(pca_data_path) or not os.path.exists(clean_data_path):
        print("Thiếu file pca_data.csv hoặc clean_data.csv")
    else:       
        df_pca = pd.read_csv(pca_data_path)
        df_clean = pd.read_csv(clean_data_path)
        
        X = df_pca.values.astype(float)
        y = df_clean['mat_final_price'].values.astype(float)
        
        print(f"Nạp dữ liệu PCA thành công! Kích thước X: {X.shape}, Kích thước y: {y.shape}")
                
        np.random.seed(69)
        indices = np.arange(X.shape[0])
        np.random.shuffle(indices)
        
        X = X[indices]
        y = y[indices]
                
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
                      
        model = LinearRegressionFromScratch()
        model.fit(X_train, y_train)
               
        y_pred = model.predict(X_test)
               
        N = len(y_test)
        mean_y_test = np.full(N, np.mean(y_test))
                
        rmse_val = RMSE(N, y_test, y_pred, 0)
        r2_val = R2(N, y_test, y_pred, mean_y_test, 0)
        mae_val = MAE(N,y_test,y_pred,0)

        print("\n" + "="*40)
        print(" KẾT QUẢ ĐÁNH GIÁ MÔ HÌNH SELF-CODE QUA PCA")
        print("="*40)
        print(f"Số lượng mẫu kiểm tra (N): {N}")
        print(f"Hệ số chặn (Intercept): {model.theta[0]:.4f}")
        print(f"Trọng số 9 thành phần PCA (Thetas): \n{model.theta[1:]}")
        print("-" * 40)
        print(f"MAE: {mae_val:.2f}")
        print(f"Root Mean Squared Error (RMSE): {rmse_val:.2f}")
        print(f"R-squared (R2): {r2_val:.4f}")
        print("="*40)