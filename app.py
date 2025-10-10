import warnings
import sys
import streamlit as st
import pandas as pd
import os
import glob
import zipfile
from io import BytesIO

# --- Hata bastırıcı ve çakal koruması ---
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

def silence_streamlit_exceptions(exc_type, exc_value, traceback):
    if exc_type.__name__ in ["RuntimeError", "ValueError", "Exception"]:
        print(f"[MetriqAI Silent Mode] Caught harmless error: {exc_value}")
        return True
    return False

sys.excepthook = silence_streamlit_exceptions

# --- Modüller ---
from data_analysis import SalesAnalyzer
from reporting import (
    generate_graphs, ai_summary, build_pdf,
    build_docx, build_ppt, save_excel
)
from config import APP_NAME, PACKAGES, OPENAI_API_KEY
from ui_components import (
    load_custom_css, render_hero, render_package_selector,
    render_team_section, simulate_processing, render_footer
)
from maps import (
    create_turkey_heatmap, create_world_map,
    create_interactive_bar_chart, create_time_series_chart
)

# --- Sayfa Ayarları ---
st.set_page_config(
    page_title=f"{APP_NAME} Dashboard",
    layout="wide",
    page_icon="⚡",
    initial_sidebar_state="expanded"
)

# --- UI ---
load_custom_css()
selected_package = render_package_selector()
package_features = PACKAGES[selected_package]['features']
render_team_section()

st.sidebar.markdown("---")
st.sidebar.markdown("### 📞 Contact")
st.sidebar.markdown("📧 insights@metriq.ai")
st.sidebar.markdown("🌐 metriq.ai")

render_hero()

# --- Veri Yükleme ---
st.markdown("### 📂 Upload Your Data")
uploaded_file = st.file_uploader(
    "Drop your Excel or CSV file here",
    type=["xlsx", "xls", "csv"],
    help="Upload sales data for instant AI-powered analysis"
)

# --- Veri Analizi ---
if uploaded_file:
    try:
        analyzer = SalesAnalyzer.load_data(uploaded_file)
        simulate_processing(selected_package)
        kpis = analyzer.compute_kpis()
        st.markdown("---")

        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("💰 Total Revenue", f"{kpis['total']:,.0f} TL")
        with col2: st.metric("📊 Daily Average", f"{kpis['avg']:,.0f} TL")
        with col3: st.metric("📈 Week-over-Week", f"{kpis['wow']:.1f}%" if not pd.isna(kpis['wow']) else "N/A")
        with col4: st.metric("🔢 Total Transactions", f"{len(analyzer.df):,}")

        st.markdown("---")

        # --- AI Summary ---
        if package_features['ai_summary']:
            if OPENAI_API_KEY:
                with st.spinner("AI is analyzing your data..."):
                    summary = ai_summary(analyzer.get_kpi_text())
                st.success("✅ AI Analysis Complete!")
                st.markdown(f"<div style='background:rgba(0,191,255,0.1);padding:15px;border-radius:10px;'>{summary}</div>", unsafe_allow_html=True)
            else:
                st.warning("⚠️ No OpenAI API key found in .env file.")
        else:
            summary = "AI analysis not available in Basic plan."

        # --- Charts ---
        st.markdown("### 📊 Data Visualization")
        if package_features['interactive_charts']:
            st.plotly_chart(create_time_series_chart(analyzer.df), use_container_width=True)
        else:
            graphs = generate_graphs(kpis)
            st.image(graphs["daily"], caption="📈 Daily Revenue Trend")

        # --- Reports ---
        st.markdown("### 📥 Download Reports")
        graphs = generate_graphs(kpis)
        pdf_path = build_pdf(summary, kpis, graphs, "metriqAI_report.pdf")
        excel_path = save_excel(analyzer.df, "data_clean.xlsx")

        col_a, col_b = st.columns(2)
        with col_a:
            with open(pdf_path, "rb") as f:
                st.download_button("📑 Download PDF", f, file_name="metriqAI_report.pdf")
        with col_b:
            with open(excel_path, "rb") as f:
                st.download_button("📊 Download Excel", f, file_name="data_clean.xlsx")

    except Exception as e:
        st.error(f"⚠️ Processing Error: {str(e)}")
else:
    st.info("👆 Upload your data file to start analysis.")

# --- Footer ---
render_footer()
