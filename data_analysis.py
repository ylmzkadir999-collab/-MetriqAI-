if uploaded_file:
    st.success("File uploaded successfully!")

    # Demo veri simülasyonu
    st.write("Analyzing data (demo mode)...")
    kpis = {"total": 325000, "avg": 15400}
    
    st.metric("💰 Total Revenue", f"{kpis['total']:,.0f} TL")
    st.metric("📊 Daily Average", f"{kpis['avg']:,.0f} TL")
else:
    st.info("Please upload a file to start.")# from data_analysis import SalesAnalyzerclass SalesAnalyzer:
    @staticmethod
    def load_data(uploaded_file):
        import pandas as pd
        df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith("xlsx") else pd.read_csv(uploaded_file)
        df['tarih'] = pd.to_datetime(df['tarih'])
        return SalesAnalyzer(df)

    def __init__(self, df):
        self.df = df

    def compute_kpis(self):
        total = self.df['net_tutar'].sum()
        avg = self.df['net_tutar'].mean()
        return {"total": total, "avg": avg}
