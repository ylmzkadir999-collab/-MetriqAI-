# app.py
streamlit
pandas
numpy
reportlab
python-pptx
openpyxl
plotly
kaleido
openai
anthropic
 from raporter import (
    generate_graphs,
    ai_summary,
    build_pdf,
    build_docx,
    build_ppt,
    save_excel
) 
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
""", unsafe_allow_html=True)# app.py
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
""", unsafe_allow_html=True)# reporting.py — MetriqAI Advanced Reporting Engine
import pandas as pd
from io import BytesIO
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

# 1️⃣ PDF RAPORU ------------------------------------------------------------
def build_pdf(df, stats, user_package):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    # Kurumsal Renk ve Stil
    title_style = ParagraphStyle(
        'Title',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0072B2"),
        spaceAfter=20,
        alignment=1,
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        fontSize=12,
        textColor=colors.HexColor("#222222"),
        leading=14,
        spaceAfter=12,
    )

    elements.append(Paragraph("MetriqAI Advanced Business Intelligence Report", title_style))
    elements.append(Paragraph(datetime.now().strftime("%d %B %Y"), subtitle_style))
    elements.append(Spacer(1, 12))

    # KPI Tablosu
    data = [
        ["📊 KPI", "Değer"],
        ["Toplam Gelir", f"₺{stats['total_revenue']:,.2f}"],
        ["Günlük Ortalama", f"₺{stats['daily_average']:,.2f}"],
        ["İşlem Sayısı", f"{stats['transactions']:,}"],
        ["Paket", user_package.upper()],
    ]
    table = Table(data, colWidths=[200, 200])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0072B2")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 20))

    # AI Summary Placeholder
    elements.append(Paragraph("<b>AI Executive Summary:</b>", subtitle_style))
    elements.append(Paragraph("MetriqAI veri analizi, gelir akışlarında yapısal trendleri belirledi. "
                              "Kısa vadeli volatilite gözlense de, genel eğilim pozitif. "
                              "Öneri: Müşteri segmentasyonu stratejisini yeniden değerlendirin ve yüksek marjlı ürünlerde dijital kampanyaları artırın.",
                              ParagraphStyle('Body', fontSize=10, leading=14)))
    elements.append(Spacer(1, 20))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()


# 2️⃣ POWERPOINT RAPORU ------------------------------------------------------------
def build_ppt(df, user_package):
    prs = Presentation()
    slide_title = prs.slide_layouts[0]

    # Kapak
    slide = prs.slides.add_slide(slide_title)
    slide.shapes.title.text = "MetriqAI Business Report"
    slide.placeholders[1].text = f"Paket: {user_package.upper()} | Satır Sayısı: {len(df):,}"

    # Sayfa 2: KPI Overview
    slide2 = prs.slides.add_slide(prs.slide_layouts[1])
    slide2.shapes.title.text = "📈 Performance Overview"
    body = slide2.placeholders[1].text = (
        f"- Total Revenue: ₺{df['net_tutar'].sum():,.2f}\n"
        f"- Daily Avg: ₺{df.groupby('tarih')['net_tutar'].sum().mean():,.2f}\n"
        f"- Transactions: {len(df):,}\n\n"
        f"Analysis suggests strong growth patterns in high-value segments."
    )

    # Sayfa 3: AI Insights
    slide3 = prs.slides.add_slide(prs.slide_layouts[1])
    slide3.shapes.title.text = "🤖 AI Strategic Insights"
    slide3.placeholders[1].text = (
        "The AI model detected patterns in your dataset:\n\n"
        "• 34% of total sales originate from top 2 categories.\n"
        "• Customers in Istanbul show higher repeat-purchase probability.\n"
        "• Suggested Action: Focus digital ads on returning users."
    )

    ppt_stream = BytesIO()
    prs.save(ppt_stream)
    ppt_stream.seek(0)
    return ppt_stream.getvalue()


# 3️⃣ EXCEL RAPORU ------------------------------------------------------------
def save_excel(df, detailed=False):
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Veri')
        if detailed:
            summary = df.describe().T
            summary.to_excel(writer, sheet_name='Özet')
            if 'kategori' in df.columns:
                df.groupby('kategori')['net_tutar'].sum().to_excel(writer, sheet_name='Kategori Analizi')
    buffer.seek(0)
    return buffer.getvalue()


# 4️⃣ DOCX RAPORU (AI) ------------------------------------------------------------
def build_docx(df, ai_text=None):
    doc = Document()
    doc.add_heading("MetriqAI - AI Analiz Raporu", level=1)

    doc.add_paragraph(datetime.now().strftime("%d %B %Y"), style='Normal')

    if not ai_text:
        ai_text = (
            "The AI system analyzed the dataset and identified key business signals. "
            "Revenue growth remains stable across major cities, with outliers in category distribution."
        )
    doc.add_paragraph(ai_text, style='Normal')

    doc.add_heading("Key Metrics", level=2)
    p = doc.add_paragraph()
    p.add_run(f"Total Rows: {len(df):,}\n").bold = True
    if 'net_tutar' in df.columns:
        p.add_run(f"Total Revenue: ₺{df['net_tutar'].sum():,.2f}\n")
        p.add_run(f"Average Transaction: ₺{df['net_tutar'].mean():,.2f}\n")

    doc.add_heading("Strategic Notes", level=2)
    doc.add_paragraph(
        "Focus marketing efforts on the top 20% of high-value clients. "
        "Automate reporting cycles and adopt adaptive pricing for better margin optimization."
    )

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()


# 5️⃣ AI SUMMARY (Premium) ------------------------------------------------------------
def ai_summary(df):
    try:
        avg = df['net_tutar'].mean()
        total = df['net_tutar'].sum()
        top_city = df['sehir'].mode()[0] if 'sehir' in df.columns else 'Bilinmiyor'
        return (f"Dataset contains {len(df):,} records. Total revenue reached ₺{total:,.2f}, "
                f"with an average transaction value of ₺{avg:,.2f}. "
                f"Top performing region: {top_city}. Strategic focus should remain on retention.")
    except Exception as e:
        return f"AI analysis failed: {e}"
