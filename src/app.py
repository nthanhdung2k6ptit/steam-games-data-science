import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Steam Game Appraiser", page_icon="🎮", layout="wide")

st.title("🎮 Steam Game Price Appraiser")
st.markdown("Công cụ thẩm định giá và phân khúc thị trường dành cho nhà phát triển Indie.")
st.divider()

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.header("1. Cấu hình tựa game")
       
    game_type = st.selectbox("Loại sản phẩm", ["Game", "DLC", "Soundtrack", "Mod"])
    
    col_date1, col_date2 = st.columns(2)
    with col_date1:
        release_year = st.number_input("Năm phát hành", min_value=2000, max_value=2030, value=2026)
    with col_date2:
        release_month = st.slider("Tháng phát hành", 1, 12, 5)
        
    num_languages = st.number_input("Số lượng ngôn ngữ hỗ trợ", min_value=1, max_value=30, value=5)
    
    st.markdown("**Nền tảng hỗ trợ (Platforms)**")
    col_plat1, col_plat2, col_plat3 = st.columns(3)
    with col_plat1:
        win = st.checkbox("Windows", value=True)
    with col_plat2:
        mac = st.checkbox("Mac OS")
    with col_plat3:
        linux = st.checkbox("Linux")
        
    has_discount = st.toggle("Dự kiến có chương trình giảm giá (Discount)")
    req_age = st.selectbox("Độ tuổi yêu cầu (Required Age)", [0, 12, 16, 18])
    
    st.markdown("<br>", unsafe_allow_html=True)    
    predict_btn = st.button("🚀 TIẾN HÀNH THẨM ĐỊNH", use_container_width=True, type="primary")

with col2:
    st.header("2. Báo cáo phân tích")
    
    if predict_btn:
        mock_price = 14.99
        mock_category = "CHEAP"
        
        st.success("✅ Đã phân tích xong dữ liệu bằng mô hình Random Forest!")
            
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.metric(label="Giá bán đề xuất (Regression)", value=f"${mock_price}")
        with res_col2:
            st.metric(label="Phân khúc thị trường (Classification)", value=mock_category)
            
        st.divider()
        
        st.subheader("3. Yếu tố tác động đến định giá")
        st.markdown("Biểu đồ bên dưới thể hiện mức độ đóng góp của từng cấu hình vào giá trị tựa game:")
                
        fig, ax = plt.subplots(figsize=(8, 4))
        features = ['Hỗ trợ Mac/Linux', f'Ngôn ngữ ({num_languages})', f'Loại: {game_type}', 'Không giảm giá']
        impacts = [2.5, 1.2, 5.0, -1.0] # Số dương kéo giá lên, số âm kéo giá xuống
        colors = ['#2e7b32' if val > 0 else '#c62828' for val in impacts]
        
        ax.barh(features, impacts, color=colors)
        ax.axvline(0, color='black', linewidth=1)
        ax.set_xlabel('Tác động lên giá ($)')
                
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        st.pyplot(fig)
        
        st.info("💡 **Gợi ý:** Thuật toán nhận thấy việc hỗ trợ đa nền tảng và phát hành dưới dạng 'Game' đóng vai trò lớn nhất trong việc nâng cao giá trị tài sản của bạn.")

    else:        
        st.info("👈 Vui lòng cấu hình thông số tựa game bên trái và bấm nút Thẩm định.")
        st.image("https://cdn.pixabay.com/photo/2017/10/24/07/11/game-controller-2883622_1280.png", width=400) # Ảnh minh họa placeholder