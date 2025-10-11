# app.py
import streamlit as st
import pandas as pd
from reporting import generate_graphs, ai_summary, build_pdf, build_docx, build_ppt, save_excel
from data_analysis import SalesAnalyzer

st.set_page_config(page_title="MetriqAI Analytics", page_icon="📊", layout="wide")

# ─────────────────────────────
# SIDEBAR - Paket Seçimi
# ─────────────────────────────
st.sidebar.title("⚙️ Ayarlar")
user_package = st.sidebar.selectbox(
    "Paket Seçin (Demo)",
    ['Basic', 'Pro', 'Premium'],
    index=2  # Default: Premium
)

st.sidebar.markdown("""
### Paket Özellikleri
**🟢 BASIC ($497)**  
- PDF Raporu  
- Metin Raporu  
- Temel metrikler  

**🔵 PRO ($997)**  
- PowerPoint  
- Detaylı Excel  
- Şehir/Kategori analizi  

**🔴 PREMIUM ($1,997)**  
- AI İçgörüler  
- Power BI Data  
- Risk Analizi  
- Sınırsız rapor  
""")

# ─────────────────────────────
# ANA SAYFA
# ─────────────────────────────
st.title("📊 MetriqAI Analytics - Ultimate Edition")

uploaded_file = st.file_uploader(
    "📂 Excel veya CSV dosyanızı yükleyin",
    type=['xlsx', 'xls', 'csv']
)

if uploaded_file is not None:
    try:
        # Veriyi yükle
        analyzer = SalesAnalyzer.load_data(uploaded_file)
        df = analyzer.df

        st.success(f"✅ {len(df):,} satır veri başarıyla yüklendi!")

        # Önizleme
        with st.expander("👀 Veri Önizleme"):
            st.dataframe(df.head(10))

        # KPI Hesaplama
        kpis = analyzer.compute_kpis()

        st.markdown("### 🎯 Temel Metrikler")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("💰 Toplam Gelir", f"{kpis['total']:,.0f} TL")
        with col2:
            st.metric("📊 Günlük Ortalama", f"{kpis['avg']:,.0f} TL")
        with col3:
            st.metric("📈 Haftalık Değişim", f"{kpis['wow']:.1f}%")
        with col4:
            st.metric("🔢 İşlem Sayısı", f"{kpis['count']:,}")

        # AI Özeti (Premium)
        st.markdown("---")
        if user_package.lower() == "premium":
            st.subheader("🤖 AI Stratejik Analiz")
            summary = ai_summary(analyzer.get_kpi_text())
            st.markdown(
                f"<div style='background:rgba(0,191,255,0.1);padding:15px;border-radius:10px;'>{summary}</div>",
                unsafe_allow_html=True
            )
        else:
            summary = "AI analizi yalnızca Premium pakette kullanılabilir."
            st.info(summary)

        # Grafikler
        st.markdown("---")
        st.subheader("📈 Görsel Analiz")
        graphs = generate_graphs(kpis)
        st.image(graphs["daily"], caption="📈 Günlük Gelir Trendi")
        st.image(graphs["top_product"], caption="📦 En Popüler Ürünler")
        st.image(graphs["top_region"], caption="🌍 Bölgesel Dağılım")

        # Raporlar
        st.markdown("---")
        st.subheader("📥 Rapor İndirme")

        pdf_path = build_pdf(summary, kpis, graphs, "metriqAI_report.pdf")
        excel_path = save_excel(df, "data_clean.xlsx")

        colA, colB = st.columns(2)
        with colA:
            with open(pdf_path, "rb") as f:
                st.download_button("📑 PDF Raporu İndir", f, file_name="metriqAI_report.pdf")
        with colB:
            with open(excel_path, "rb") as f:
                st.download_button("📊 Excel Verisi İndir", f, file_name="data_clean.xlsx")

    except Exception as e:
        st.error(f"⚠️ Hata: {str(e)}")

else:
    st.info("👆 Başlamak için bir dosya yükleyin.")
    st.markdown("""
    ### 🎯 Özellikler
    - 📄 PDF Raporları  
    - 📊 PowerPoint Sunumları  
    - 📈 Excel Analizi  
    - 🤖 AI İçgörüler  
    """)
