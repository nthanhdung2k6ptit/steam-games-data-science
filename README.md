# Steam Games Data Science Project

Dự án phân tích dữ liệu Steam Games Dataset, tập trung vào việc xây dựng một pipeline Data Science từ dữ liệu thô đến phân tích, tiền xử lý, mô hình học máy và hệ khuyến nghị game.

Dataset ban đầu gồm nhiều file CSV chứa thông tin về các game trên Steam như tên game, giá bán, ngày phát hành, nền tảng hỗ trợ, điểm đánh giá, số lượng recommendations, mô tả ngắn, thể loại, nhà phát triển và nhà phát hành.

Trong project này, dữ liệu được import vào MySQL để mô phỏng quy trình làm việc thực tế. Sau đó, nhóm sử dụng SQL queries, views và indexes để truy vấn, liên kết và chuẩn bị dữ liệu cho các bước phân tích bằng Python.

## Main Tasks

- Import CSV data into MySQL
- Exploratory Data Analysis (EDA)
- Data Preprocessing and Feature Engineering
- PCA for dimensionality reduction
- Regression model
- Classification model
- KMeans Clustering
- Model Explainability using Feature Importance and Permutation Importance
- Ethics Analysis and Responsible AI discussion
- Content-Based Game Recommendation System using TF-IDF and Cosine Similarity

## Technologies Used

- Python
- MySQL
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- SQLAlchemy
- PyMySQL
- Jupyter Notebook

## Project Pipeline

```text
CSV Files
→ MySQL Database
→ SQL Queries / Views / Indexes
→ EDA
→ Preprocessing
→ PCA
→ Regression / Classification / Clustering
→ Model Explainability
→ Ethics Analysis
→ Recommendation System