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

# Sayfa ayarları
st.set_page_config(
    page_title="MetriqAI Analytics",
    page_icon="📊",
    layout="wide"
)

# ───────────────────────────────
# SIDEBAR
# ───────────────────────────────
st.sidebar.title("⚙️ Ayarlar")

user_package = st.sidebar.selectbox(
    "Paket Seçin",
    ["basic", "pro", "premium"],
    index=2
)

st.sidebar.markdown("""
### 💼 Paket Özellikleri

**🟢 BASIC ($497)**  
- PDF Raporu  
- Metin Raporu  
- Temel metrikler  

**🔵 PRO ($997)**  
- Basic +  
- PowerPoint  
- Detaylı Excel  
- Şehir/Kategori analizi  

**🟣 PREMIUM ($1,997)**  
- Pro +  
- AI İçgörüler  
- Power BI Data  
- Risk Analizi  
- Sınırsız rapor  
""")

# ───────────────────────────────
# ANA SAYFA
# ───────────────────────────────
st.title("📊 MetriqAI Analytics - Ultimate Edition")

uploaded_file = st.file_uploader(
    "📂 Excel veya CSV dosyanızı yükleyin",
    type=["xlsx", "xls", "csv"]
)

if uploaded_file:
    try:
        # Veri yükleme
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Tarih sütununu dönüştür
        if "tarih" in df.columns:
            df["tarih"] = pd.to_datetime(df["tarih"], errors="coerce")

        st.success(f"✅ {len(df):,} satır veri başarıyla yüklendi!")

        # Veri önizleme
        with st.expander("👀 Veri Önizleme"):
            st.dataframe(df.head(10))

        # ───────────────────────────────
        # METRİKLER
        # ───────────────────────────────
        st.markdown("---")
        st.subheader("📈 Temel Metrikler")

        col1, col2, col3, col4 = st.columns(4)

        total_revenue = df["net_tutar"].sum() if "net_tutar" in df.columns else 0
        daily_avg = (
            df.groupby("tarih")["net_tutar"].sum().mean()
            if "tarih" in df.columns and "net_tutar" in df.columns
            else 0
        )

        with col1:
            st.metric("💰 Toplam Gelir", f"₺{total_revenue:,.2f}")
        with col2:
            st.metric("📊 Günlük Ortalama", f"₺{daily_avg:,.2f}")
        with col3:
            st.metric("🛒 Toplam İşlem", f"{len(df):,}")
        with col4:
            avg_transaction = (
                df["net_tutar"].mean() if "net_tutar" in df.columns else 0
            )
            st.metric("🎯 Ortalama İşlem", f"₺{avg_transaction:,.2f}")

        # ───────────────────────────────
        # GRAFİKLER
        # ───────────────────────────────
        st.markdown("---")
        st.subheader("📊 Görsel Analiz")

        if "tarih" in df.columns and "net_tutar" in df.columns:
            daily_sales = (
                df.groupby("tarih")["net_tutar"].sum().reset_index().sort_values("tarih")
            )
            st.line_chart(
                daily_sales.set_index("tarih")["net_tutar"],
                use_container_width=True
            )

        if "kategori" in df.columns and "net_tutar" in df.columns:
            st.markdown("### 📦 Kategori Bazlı Satışlar")
            category_sales = (
                df.groupby("kategori")["net_tutar"].sum().sort_values(ascending=False)
            )
            st.bar_chart(category_sales)

        # ───────────────────────────────
        # RAPORLAR
        # ───────────────────────────────
        st.markdown("---")
        st.subheader("📥 Raporları İndir")

        colA, colB, colC, colD = st.columns(4)

        # PDF (Basic+)
        with colA:
            if st.button("📄 PDF Raporu"):
                with st.spinner("PDF oluşturuluyor..."):
                    try:
                        stats = {
                            "total_revenue": total_revenue,
                            "transactions": len(df),
                            "daily_average": daily_avg
                        }
                        pdf_bytes = build_pdf(df, stats, user_package)
                        st.download_button(
                            "⬇️ PDF İndir",
                            data=pdf_bytes,
                            file_name="metriqAI_rapor.pdf",
                            mime="application/pdf"
                        )
                        st.success("✅ PDF hazır!")
                    except Exception as e:
                        st.error(f"❌ PDF oluşturma hatası: {e}")

        # PowerPoint (Pro+)
        with colB:
            if user_package in ["pro", "premium"]:
                if st.button("📊 PowerPoint Raporu"):
                    with st.spinner("PowerPoint hazırlanıyor..."):
                        try:
                            ppt_bytes = build_ppt(df, user_package)
                            st.download_button(
                                "⬇️ PPTX İndir",
                                data=ppt_bytes,
                                file_name="metriqAI_sunum.pptx",
                                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                            )
                            st.success("✅ PowerPoint hazır!")
                        except Exception as e:
                            st.error(f"❌ PowerPoint hatası: {e}")
            else:
                st.info("🔒 Yalnızca Pro paket ve üzeri")

        # Excel (Pro+)
        with colC:
            if user_package in ["pro", "premium"]:
                if st.button("📈 Excel Raporu"):
                    with st.spinner("Excel hazırlanıyor..."):
                        try:
                            excel_bytes = save_excel(df, detailed=True)
                            st.download_button(
                                "⬇️ Excel İndir",
                                data=excel_bytes,
                                file_name="metriqAI_detayli.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                            st.success("✅ Excel hazır!")
                        except Exception as e:
                            st.error(f"❌ Excel hatası: {e}")
            else:
                st.info("🔒 Yalnızca Pro paket ve üzeri")

        # AI (Premium)
        with colD:
            if user_package == "premium":
                if st.button("🤖 AI Raporu"):
                    with st.spinner("AI analizi hazırlanıyor..."):
                        try:
                            summary_text = ai_summary(df)
                            docx_bytes = build_docx(df, summary_text)
                            st.download_button(
                                "⬇️ AI DOCX İndir",
                                data=docx_bytes,
                                file_name="metriqAI_AI_rapor.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )
                            st.success("✅ AI rapor hazır!")
                        except Exception as e:
                            st.error(f"❌ AI rapor hatası: {e}")
            else:
                st.info("🔒 Yalnızca Premium paket")

    except Exception as e:
        st.error(f"❌ Hata oluştu: {e}")
else:
    st.info("👆 Başlamak için dosya yükleyin.")
    st.markdown("""
    ### 🎯 Özellikler
    - 📄 PDF, PPT, XLSX, DOCX raporları
    - 📊 Otomatik veri analizi
    - 🤖 AI destekli içgörüler
    - 💼 Paket bazlı fiyatlandırma
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align:center;color:gray;'>
<p>MetriqAI Analytics © 2025 | Powered by GPT-5 & Streamlit</p>
</div>
""", unsafe_allow_html=True)
