# app.py
import streamlit as st
import pandas as pd
from reports import show_download_section  # ← YENİ
# ... diğer import'lar

st.title("📊 MetriqAI Analytics")

# Dosya yükleme
uploaded_file = st.file_uploader("📂 Excel veya CSV dosyanızı yükleyin", type=['xlsx', 'xls', 'csv'])

if uploaded_file is not None:
    # Veriyi yükle
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    # Tarih sütununu düzelt
    if 'tarih' in df.columns:
        df['tarih'] = pd.to_datetime(df['tarih'])
    
    # ... GRAFİKLER, ANALİZLER ...
    
    # RAPOR BÖLÜMÜ (en sona ekleyin)
    show_download_section(df)  # ← YENİ, TEK SATIRLA ÇÖZÜM!
    
else:
    st.info("👆 Lütfen bir dosya yükleyin")
