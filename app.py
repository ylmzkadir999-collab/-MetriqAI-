# app.py
import streamlit as st
import pandas as pd
from reporting import generate_graphs, ai_summary, build_pdf, build_docx, build_ppt, save_excel 
st.set_page_config(page_title="MetriqAI Analytics", page_icon="📊", layout="wide")

# Sidebar - Paket seçimi (Demo için)
st.sidebar.title("⚙️ Ayarlar")
user_package = st.sidebar.selectbox(
    "Paket Seçin (Demo)",
    ['basic', 'pro', 'premium'],
    index=2  # Default: premium
)
summary = {
    analyzer = SalesAnalyzer.load_data(uploaded_file)
df = analyzer.df
    'daily_average': df.groupby('tarih')['net_tutar'].sum().mean(),
    'transactions': len(df)
}
report = create_report(summary)  #
st.sidebar.markdown(f"""
### Paket Özellikleri

**🟢 BASIC** ($497)
- PDF Raporu
- Metin Raporu
- Temel metrikler

**🔵 PRO** ($997)
- Basic + 
- PowerPoint
- Detaylı Excel
- Şehir/Kategori analizi

**🟣 PREMIUM** ($1,997)
- Pro +
- AI İçgörüler
- Power BI Data
- Risk Analizi
- Sınırsız rapor
""")

# Ana sayfa
st.title("📊 MetriqAI Analytics - Ultimate Edition")

# Dosya yükleme
uploaded_file = st.file_uploader(
    "📂 Excel veya CSV dosyanızı yükleyin",
    type=['xlsx', 'xls', 'csv']
)

if uploaded_file is not None:
    # Veri yükleme
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    # Tarih düzeltme
    if 'tarih' in df.columns:
        df['tarih'] = pd.to_datetime(df['tarih'], errors='coerce')
    
    st.success(f"✅ {len(df):,} satır veri yüklendi!")
    
    # Veri önizleme
    with st.expander("👀 Veri Önizleme"):
        st.dataframe(df.head(10))
    
    # ... Diğer grafikler ve analizler ...
    
    # RAPOR BÖLÜMÜ
    st.markdown("---")
    show_download_section(df, user_package=user_package)

else:
    st.info("👆 Lütfen bir dosya yükleyin")
    
    # Demo görsel
    st.markdown("""
    ### 🎯 Özellikler
    
    - 📄 **PDF Raporları**: Profesyonel, paket bazlı PDF'ler
    - 📊 **PowerPoint**: Otomatik sunum oluşturma
    - 📈 **Excel Detaylı**: 8+ sayfa analiz
    - 🔷 **Power BI**: BI-ready veri setleri
    - 🤖 **AI Analizi**: Yapay zeka destekli öneriler
    
    ### 📦 Paket Karşılaştırma
    
    | Özellik | Basic | Pro | Premium |
    |---------|-------|-----|---------|
    | PDF Raporu | ✅ Temel | ✅ Detaylı | ✅ Full |
    | PowerPoint | ❌ | ✅ | ✅ |
    | Excel Detaylı | ❌ | ✅ | ✅ |
    | Power BI Data | ❌ | ❌ | ✅ |
    | AI İçgörüler | ❌ | ❌ | ✅ |
    """)
