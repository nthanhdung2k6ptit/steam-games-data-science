import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
import os

@st.cache_resource
def load_ml_components():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(current_dir, "models")
        
        reg_model = joblib.load(os.path.join(base_path, "regression_model.pkl"))
        clf_model = joblib.load(os.path.join(base_path, "classification.pkl"))
        scaler = joblib.load(os.path.join(base_path, "scaler.pkl"))
        pca = joblib.load(os.path.join(base_path, "pca.pkl"))
        
        return reg_model, clf_model, scaler, pca
    except Exception as e:
        st.error(f"⚠️ Lỗi đường dẫn: {e}\n Đường dẫn đang tìm kiếm là: {base_path}")
        return None, None, None, None

reg_model, clf_model, scaler, pca = load_ml_components()

st.set_page_config(page_title="Steam Game Appraiser", page_icon="🎮", layout="wide")
st.title("🎮 Steam Game Price Appraiser")
st.markdown("Công cụ thẩm định giá và phân khúc thị trường dành cho nhà phát triển Indie.")
st.divider()

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.header("1. Cấu hình tựa game")
    game_type = st.selectbox("Loại sản phẩm", ["game", "dlc", "soundtrack", "mod"])
    
    col_date1, col_date2 = st.columns(2)
    with col_date1:
        release_year = st.number_input("Năm phát hành", 2000, 2030, 2026)
    with col_date2:
        release_month = st.slider("Tháng phát hành", 1, 12, 5)
        
    num_languages = st.number_input("Số lượng ngôn ngữ hỗ trợ", 1, 30, 5)
    
    st.markdown("**Nền tảng hỗ trợ (Platforms)**")
    col_plat1, col_plat2, col_plat3 = st.columns(3)
    with col_plat1:
        win = st.checkbox("Windows", value=True)
    with col_plat2:
        mac = st.checkbox("Mac OS")
    with col_plat3:
        linux = st.checkbox("Linux")
        
    has_discount = st.toggle("Dự kiến có chương trình giảm giá")
    req_age = st.selectbox("Độ tuổi yêu cầu", [0, 12, 16, 18])
    
    predict_btn = st.button("🚀 TIẾN HÀNH THẨM ĐỊNH", use_container_width=True, type="primary")

with col2:
    st.header("2. Báo cáo phân tích")
    
    if predict_btn:
        if reg_model is None:
            st.warning("Hệ thống chưa tải được mô hình. Vui lòng kiểm tra lại.")
        else:
            try:              
                expected_cols = scaler.feature_names_in_
                               
                df_input = pd.DataFrame(0.0, index=[0], columns=expected_cols)
                                
                if 'required_age' in expected_cols: df_input['required_age'] = req_age
                if 'release_year' in expected_cols: df_input['release_year'] = release_year
                if 'release_month' in expected_cols: df_input['release_month'] = release_month
                if 'num_languages' in expected_cols: df_input['num_languages'] = num_languages
          
                if 'mat_discount_percent' in expected_cols: df_input['mat_discount_percent'] = 10 if has_discount else 0
                if 'mat_initial_price' in expected_cols: df_input['mat_initial_price'] = 0
                if 'is_free' in expected_cols: df_input['is_free'] = 0
                if 'mat_supports_windows' in expected_cols: df_input['mat_supports_windows'] = int(win)
                if 'mat_supports_mac' in expected_cols: df_input['mat_supports_mac'] = int(mac)
                if 'mat_supports_linux' in expected_cols: df_input['mat_supports_linux'] = int(linux)
                if 'platform_count' in expected_cols: df_input['platform_count'] = int(win) + int(mac) + int(linux)
                
    
                if 'appid' in expected_cols: df_input['appid'] = 0
                if 'mat_final_price' in expected_cols: df_input['mat_final_price'] = 0 
                
    
                target_type_col = f"type_{game_type.lower()}"
                for col in expected_cols:
                    if target_type_col in col.lower():
                        df_input[col] = 1.0
                
                X_scaled = scaler.transform(df_input)
                X_pca = pca.transform(X_scaled)
                
                pred_price_cents = reg_model.predict(X_pca)[0]
                pred_category = clf_model.predict(X_pca)[0]
                
                pred_price_usd = max(0, pred_price_cents / 100)
                
                st.success("✅ Đã thẩm định thành công!")
                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    st.metric(label="Giá bán đề xuất", value=f"${pred_price_usd:.2f}")
                with res_col2:
                    st.metric(label="Phân khúc thị trường", value=str(pred_category).upper())
                    
            except Exception as e:
                st.error(f"⚠️ Lỗi trong quá trình tính toán: {e}")

    else:
        st.info("👈 Vui lòng cấu hình thông số tựa game bên trái và bấm nút Thẩm định.")