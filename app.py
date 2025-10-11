# app.py
import streamlit as st
import pandas as pd
from reporting import (
    generate_graphs, 
    ai_summary, 
    build_pdf, 
    build_docx, 
    build_ppt, 
    save_excel
)

st.set_page_config(
    page_title="MetriqAI Analytics", 
    page_icon="📊", 
    layout="wide"
)

# Sidebar - Paket seçimi
st.sidebar.title("⚙️ Ayarlar")
user_package = st.sidebar.selectbox(
    "Paket Seçin (Demo)",
    ['basic', 'pro', 'premium'],
    index=2  # Default: premium
)

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
    try:
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
        
        # Temel metrikler
        st.markdown("---")
        st.subheader("📈 Temel Metrikler")
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Hesaplamalar (kolon adlarını veriye göre ayarlayın)
        if 'net_tutar' in df.columns:
            total_revenue = df['net_tutar'].sum()
            daily_avg = df.groupby('tarih')['net_tutar'].sum().mean() if 'tarih' in df.columns else 0
            
            with col1:
                st.metric("💰 Toplam Gelir", f"₺{total_revenue:,.2f}")
            
            with col2:
                st.metric("📊 Günlük Ortalama", f"₺{daily_avg:,.2f}")
        
        with col3:
            st.metric("🛒 Toplam İşlem", f"{len(df):,}")
        
        with col4:
            if 'net_tutar' in df.columns:
                avg_transaction = df['net_tutar'].mean()
                st.metric("🎯 Ortalama İşlem", f"₺{avg_transaction:,.2f}")
        
        # Grafikler
        st.markdown("---")
        st.subheader("📊 Görselleştirmeler")
        
        # Zaman serisi analizi
        if 'tarih' in df.columns and 'net_tutar' in df.columns:
            daily_sales = df.groupby('tarih')['net_tutar'].sum().reset_index()
            
            st.line_chart(
                daily_sales.set_index('tarih')['net_tutar'],
                use_container_width=True
            )
        
        # Kategori analizi (eğer varsa)
        if 'kategori' in df.columns and 'net_tutar' in df.columns:
            st.markdown("### 📂 Kategori Bazlı Analiz")
            category_sales = df.groupby('kategori')['net_tutar'].sum().sort_values(ascending=False)
            st.bar_chart(category_sales)
        
        # RAPOR İNDİRME BÖLÜMÜ
        st.markdown("---")
        st.subheader("📥 Raporları İndir")
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Basic - PDF
        with col1:
            if st.button("📄 PDF İndir", use_container_width=True):
                with st.spinner("PDF oluşturuluyor..."):
                    try:
                        # Temel istatistikler
                        stats = {
                            'total_revenue': df['net_tutar'].sum() if 'net_tutar' in df.columns else 0,
                            'transactions': len(df),
                            'daily_average': df.groupby('tarih')['net_tutar'].sum().mean() if 'tarih' in df.columns and 'net_tutar' in df.columns else 0
                        }
                        
                        pdf_bytes = build_pdf(df, stats, user_package)
                        st.download_button(
                            label="⬇️ PDF İndir",
                            data=pdf_bytes,
                            file_name="rapor.pdf",
                            mime="application/pdf"
                        )
                        st.success("✅ PDF hazır!")
                    except Exception as e:
                        st.error(f"❌ PDF oluşturma hatası: {str(e)}")
        
        # Pro - PowerPoint
        with col2:
            if user_package in ['pro', 'premium']:
                if st.button("📊 PowerPoint İndir", use_container_width=True):
                    with st.spinner("PowerPoint oluşturuluyor..."):
                        try:
                            ppt_bytes = build_ppt(df, user_package)
                            st.download_button(
                                label="⬇️ PPTX İndir",
                                data=ppt_bytes,
                                file_name="rapor.pptx",
                                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                            )
                            st.success("✅ PowerPoint hazır!")
                        except Exception as e:
                            st.error(f"❌ PowerPoint oluşturma hatası: {str(e)}")
            else:
                st.info("🔒 Pro paket gerekli")
        
        # Pro - Excel Detaylı
        with col3:
            if user_package in ['pro', 'premium']:
                if st.button("📈 Excel Detaylı İndir", use_container_width=True):
                    with st.spinner("Excel oluşturuluyor..."):
                        try:
                            excel_bytes = save_excel(df, detailed=True)
                            st.download_button(
                                label="⬇️ XLSX İndir",
                                data=excel_bytes,
                                file_name="rapor_detayli.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                            st.success("✅ Excel hazır!")
                        except Exception as e:
                            st.error(f"❌ Excel oluşturma hatası: {str(e)}")
            else:
                st.info("🔒 Pro paket gerekli")
        
        # Premium - AI Raporu
        with col4:
            if user_package == 'premium':
                if st.button("🤖 AI Raporu İndir", use_container_width=True):
                    with st.spinner("AI analiz yapılıyor..."):
                        try:
                            # AI özeti oluştur
                            summary_text = ai_summary(df)
                            docx_bytes = build_docx(df, summary_text)
                            st.download_button(
                                label="⬇️ DOCX İndir",
                                data=docx_bytes,
                                file_name="ai_rapor.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )
                            st.success("✅ AI rapor hazır!")
                        except Exception as e:
                            st.error(f"❌ AI rapor oluşturma hatası: {str(e)}")
            else:
                st.info("🔒 Premium paket gerekli")
        
    except Exception as e:
        st.error(f"❌ Dosya yüklenirken hata oluştu: {str(e)}")
        st.info("Lütfen dosya formatınızın doğru olduğundan emin olun.")

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
    
    ### 🚀 Nasıl Kullanılır?
    
    1. Excel veya CSV dosyanızı yükleyin
    2. Paket seçiminizi yapın (soldaki menüden)
    3. Analizleri inceleyin
    4. İhtiyacınız olan raporu indirin
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>MetriqAI Analytics © 2024 | Veri Odaklı Karar Desteği</p>
</div>
""", unsafe_allow_html=True)
