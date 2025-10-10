import streamlit as st
from data_analysis import SalesAnalyzer

st.set_page_config(page_title="Metriq.AI", page_icon="⚡", layout="wide")

st.title("⚡ Metriq.AI Dashboard")
st.write("Upload your Excel or CSV file to begin analysis.")

uploaded_file = st.file_uploader("📂 Upload File", type=["xlsx", "csv"])

if uploaded_file:
    st.success("File uploaded successfully!")

    # Örnek kullanım - gerçek analiz fonksiyonu burada çağrılacak
    st.write("Analyzing data with SalesAnalyzer...")
    analyzer = SalesAnalyzer.load_data(uploaded_file)
    kpis = analyzer.compute_kpis()
    
    st.metric("💰 Total Revenue", f"{kpis['total']:,.0f} TL")
    st.metric("📊 Daily Average", f"{kpis['avg']:,.0f} TL")
else:
    st.info("Please upload a file to start.")
