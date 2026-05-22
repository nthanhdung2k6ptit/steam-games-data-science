import os
import pandas as pd
import numpy as np 
import time
from metrics import Precision, Recall, F1Score, Accuracy

class LogisticRegressionMultinomialRaw:
    def __init__(self, learning_rate=0.1, epochs=100):
        self.lr = learning_rate
        self.epochs = epochs
        self.weights = None
        self.classes = None

    def _softmax(self, z):
        # Giới hạn cận trên số mũ bằng cách trừ max để triệt tiêu lỗi tràn số thực (Numerical Stability)
        exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))
        return exp_z / np.sum(exp_z, axis=1, keepdims=True)

    def _to_one_hot(self, y, num_classes):
        one_hot = np.zeros((len(y), num_classes))
        for i, val in enumerate(y):
            one_hot[i, val] = 1
        return one_hot

    def fit(self, X, y):
        # Khởi tạo danh sách nhãn chuỗi độc lập
        self.classes = np.unique(y)
        class_to_idx = {c: i for i, c in enumerate(self.classes)}
        y_encoded = np.array([class_to_idx[item] for item in y])
        
        m, n = X.shape
        num_classes = len(self.classes)
        
        # Tạo ma trận Bias
        X_b = np.c_[np.ones((m, 1)), X]
        self.weights = np.zeros((X_b.shape[1], num_classes))
        y_one_hot = self._to_one_hot(y_encoded, num_classes)
        
        # Vòng lặp Gradient Descent thô sơ quét cạn toàn bộ ma trận dữ liệu
        for epoch in range(self.epochs):
            scores = X_b.dot(self.weights)
            predictions = self._softmax(scores)
            
            # Đạo hàm Vector hóa toàn phần
            gradient = X_b.T.dot(predictions - y_one_hot) / m
            self.weights -= self.lr * gradient
            
            if (epoch + 1) % 20 == 0:
                print(f"  -> Đang chạy Epoch {epoch + 1}/{self.epochs}...")

    def predict(self, X):
        X_b = np.c_[np.ones((X.shape[0], 1)), X]
        scores = X_b.dot(self.weights)
        probs = self._softmax(scores)
        preds_idx = np.argmax(probs, axis=1)
        return np.array([self.classes[idx] for idx in preds_idx])


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))       
    pca_data_path = os.path.normpath(os.path.join(current_dir, "..", "..", "..", "data", "processed", "pca_data.csv"))
    clean_data_path = os.path.normpath(os.path.join(current_dir, "..", "..", "..", "data", "processed", "clean_data.csv"))
    
    if not os.path.exists(pca_data_path) or not os.path.exists(clean_data_path):
        print("⚠️ Không tìm thấy file dữ liệu tại thư mục data/processed!")
    else:
        print("========== KHỞI CHẠY LOGISTIC REGRESSION RAW (100% DATA) ==========")
        X = pd.read_csv(pca_data_path).values.astype(float)
        y = pd.read_csv(clean_data_path)['price_category'].values
        
        # Xáo trộn dữ liệu đồng bộ bằng Seed 42
        np.random.seed(42)
        indices = np.arange(X.shape[0])
        np.random.shuffle(indices)
        X, y = X[indices], y[indices]
        
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        print(f"Kích thước nạp vào - Train: {X_train.shape}, Test: {X_test.shape}")
        
        # ĐO THỜI GIAN HUẤN LUYỆN
        t0 = time.time()
        model = LogisticRegressionMultinomialRaw(learning_rate=0.1, epochs=100)
        model.fit(X_train, y_train)
        train_time = time.time() - t0
        
        # ĐO THỜI GIAN DỰ ĐOÁN
        t1 = time.time()
        y_pred = model.predict(X_test)
        pred_time = time.time() - t1
        
        acc_val = Accuracy(len(y_test), np.sum(y_test == y_pred))
        
        print("\n" + "="*50)
        print(" KẾT QUẢ ĐÁNH GIÁ LOGISTIC REGRESSION THÔ SƠ TỰ CHẾ")
        print("="*50)
        print(f"Thời gian huấn luyện (Train Time) : {train_time:.4f} giây")
        print(f"Thời gian dự đoán (Predict Time) : {pred_time:.4f} giây")
        print("-" * 50)
        print(f"Độ chính xác tổng thể (Accuracy) : {acc_val * 100:.2f}%")
        print("-" * 50)
        
        for label in np.unique(y_test):
            tp = np.sum((y_test == label) & (y_pred == label))
            fp = np.sum((y_test != label) & (y_pred == label))
            fn = np.sum((y_test == label) & (y_pred != label))
            
            # KHẮC PHỤC CHỐNG LỖI NAN: Nếu mẫu không dán nhãn nào cho lớp này, ép về mốc 0.0
            if tp + fp == 0:
                p_val = 0.0
            else:
                p_val = Precision(tp, fp)
                
            r_val = Recall(tp, fn)
            f1_val = F1Score(p_val, r_val) if (p_val + r_val) > 0 else 0.0
            
            print(f"Nhãn [{label.upper()}]: Precision: {p_val:.4f} | Recall: {r_val:.4f} | F1: {f1_val:.4f}")
        print("="*50)