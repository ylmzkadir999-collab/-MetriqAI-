MetriqAI — Single-file Streamlit App (v2.0 Clean)

-- coding: utf-8 --

""" One-file deploy for Streamlit Cloud. Paste this file as app.py in your repo root.

Features:

3 packages (Basic / Pro / Premium)

KPI engine (SalesAnalyzer)

AI summary (OpenAI optional; graceful fallback)

Static graphs (matplotlib) + Interactive charts & maps (plotly)

Exports: PDF, DOCX, PPTX, Excel, ZIP

Premium UI (custom CSS) + fake processing animation


Requirements (requirements.txt): streamlit>=1.28.0 pandas>=2.0.0 numpy>=1.24.0 matplotlib>=3.7.0 plotly>=5.17.0 python-dotenv>=1.0.0 openpyxl>=3.1.0 fpdf>=1.7.2 python-docx>=0.8.11 python-pptx>=0.6.21 Pillow>=10.0.0 openai>=1.0.0

Env (.env): OPENAI_API_KEY=sk-... """

─────────────────────────────────────────────────────────────

Imports

─────────────────────────────────────────────────────────────

import os, io, glob, zipfile, time, math from datetime import datetime from io import BytesIO

import numpy as np import pandas as pd import streamlit as st

import matplotlib matplotlib.use("Agg") import matplotlib.pyplot as plt

import plotly.express as px import plotly.graph_objects as go

from fpdf import FPDF from docx import Document from pptx import Presentation from pptx.util import Inches, Pt

try: from dotenv import load_dotenv load_dotenv() except Exception: pass

OpenAI (optional)

try: from openai import OpenAI except Exception: OpenAI = None

─────────────────────────────────────────────────────────────

Config & Branding

─────────────────────────────────────────────────────────────

APP_NAME = "metriq.AI" BRAND_TAGLINE = "Insights at the Speed of Thought" VERSION = "2.0" OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

PACKAGES = { "🟢 Basic": { "price": "$497", "delivery": "24h", "features": { "pdf_report": True, "excel_export": True, "ai_summary": False, "interactive_charts": False, "turkey_map": False, "world_map": False, "powerpoint": False, "email_delivery": False, "video_walkthrough": False, "priority_support": False, }, "color": "#27AE60", "icon": "🟢", }, "🔵 Pro": { "price": "$997", "delivery": "12h", "features": { "pdf_report": True, "excel_export": True, "ai_summary": True, "interactive_charts": True, "turkey_map": True, "world_map": False, "powerpoint": True, "email_delivery": True, "video_walkthrough": False, "priority_support": True, }, "color": "#3498DB", "icon": "🔵", }, "🔴 Premium": { "price": "$1,997", "delivery": "6h", "features": { "pdf_report": True, "excel_export": True, "ai_summary": True, "interactive_charts": True, "turkey_map": True, "world_map": True, "powerpoint": True, "email_delivery": True, "video_walkthrough": True, "priority_support": True, }, "color": "#E74C3C", "icon": "🔴", }, }

TEAM_MEMBERS = [ {"name": "Dr. Sarah Chen", "role": "Lead Data Scientist", "avatar": "👩‍🔬", "bio": "PhD ML, Stanford"}, {"name": "Marcus Rodriguez", "role": "Senior BI Consultant", "avatar": "👨‍💼", "bio": "MBA Harvard"}, {"name": "Emily Thompson", "role": "Strategic Analyst", "avatar": "👩‍💻", "bio": "MSc DS, MIT"}, ]

TURKEY_CITIES = { "İstanbul": {"lat": 41.0082, "lon": 28.9784}, "Ankara": {"lat": 39.9334, "lon": 32.8597}, "İzmir": {"lat": 38.4237, "lon": 27.1428}, "Bursa": {"lat": 40.1826, "lon": 29.0665}, "Antalya": {"lat": 36.8969, "lon": 30.7133}, "Adana": {"lat": 37.0, "lon": 35.3213}, "Gaziantep": {"lat": 37.0662, "lon": 37.3833}, "Konya": {"lat": 37.8746, "lon": 32.4932}, "Mersin": {"lat": 36.8121, "lon": 34.6415}, "Kayseri": {"lat": 38.7312, "lon": 35.4787}, }

MPL_PARAMS = { "figure.figsize": (10, 5.5), "axes.titlesize": 14, "axes.labelsize": 11, "font.size": 10, "axes.grid": True, "grid.alpha": 0.18, "axes.titleweight": "bold", "savefig.bbox": "tight", }

─────────────────────────────────────────────────────────────

Data Engine — SalesAnalyzer

─────────────────────────────────────────────────────────────

class SalesAnalyzer: """Veri yükleme, temizleme ve KPI hesaplama motoru."""

def __init__(self, df: pd.DataFrame):
    self.df = df.copy()
    self.kpis = {}

@classmethod
def load_data(cls, uploaded_file_or_path=None):
    # Accept BytesIO (Streamlit uploader) or path
    if uploaded_file_or_path is None:
        # generate stub data
        dates = pd.date_range("2025-01-01", periods=28, freq="D")
        rng = np.random.default_rng(42)
        df = pd.DataFrame({
            "tarih": dates,
            "net_tutar": (rng.normal(500, 120, len(dates))).clip(min=120).round(2),
            "kategori": rng.choice(["A", "B", "C"], size=len(dates)),
            "sehir": rng.choice(list(TURKEY_CITIES.keys()), size=len(dates)),
        })
    else:
        name = getattr(uploaded_file_or_path, "name", "")
        if name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file_or_path)
        elif name.endswith(".csv"):
            df = pd.read_csv(uploaded_file_or_path)
        else:
            # try auto-detect
            try:
                df = pd.read_excel(uploaded_file_or_path)
            except Exception:
                uploaded_file_or_path.seek(0)
                df = pd.read_csv(uploaded_file_or_path)

    # Normalize columns
    colmap = {c.lower().strip(): c for c in df.columns}
    # ensure expected columns exist
    def find_col(key, candidates):
        for k in candidates:
            if k in colmap:
                return colmap[k]
        return None

    tarih_col = find_col("tarih", ["tarih", "date", "datetime"])
    tutar_col = find_col("net_tutar", ["net_tutar", "gelir", "revenue", "amount", "tutar"])
    kategori_col = find_col("kategori", ["kategori", "ürün", "urun", "category", "product"])
    sehir_col = find_col("sehir", ["sehir", "şehir", "city", "il"])

    if tarih_col is None or tutar_col is None:
        raise ValueError("Data must contain at least date (tarih) and amount (net_tutar) columns.")

    df = df.rename(columns={
        tarih_col: "tarih",
        tutar_col: "net_tutar",
        **({kategori_col: "kategori"} if kategori_col else {}),
        **({sehir_col: "sehir"} if sehir_col else {}),
    })

    df["tarih"] = pd.to_datetime(df["tarih"], errors="coerce")
    df = df.dropna(subset=["tarih", "net_tutar"]).sort_values("tarih")
    df["Hafta"] = df["tarih"].dt.isocalendar().week.astype(int)
    df["Ay"] = df["tarih"].dt.to_period("M").astype(str)
    return cls(df)

def compute_kpis(self) -> dict:
    df = self.df
    daily = df.groupby("tarih", as_index=False)["net_tutar"].sum()
    total = float(df["net_tutar"].sum())
    avg = float(df["net_tutar"].mean())

    max_date = df["tarih"].max()
    last7_start = max_date - pd.Timedelta(days=6)
    prev7_start = max_date - pd.Timedelta(days=13)

    last7 = float(df[df["tarih"] >= last7_start]["net_tutar"].sum())
    prev7 = float(df[(df["tarih"] < last7_start) & (df["tarih"] >= prev7_start)]["net_tutar"].sum())
    wow = ((last7 - prev7) / prev7 * 100) if prev7 > 0 else np.nan

    by_product = df.groupby(df.get("kategori", pd.Series(["N/A"]*len(df))))["net_tutar"].sum().sort_values(ascending=False)
    by_region = df.groupby(df.get("sehir", pd.Series(["N/A"]*len(df))))["net_tutar"].sum().sort_values(ascending=False)

    self.kpis = {
        "daily": daily,
        "total": total, "avg": avg,
        "last7": last7, "prev7": prev7, "wow": wow,
        "by_product": by_product, "by_region": by_region,
    }
    return self.kpis

def get_kpi_text(self) -> str:
    if not self.kpis:
        self.compute_kpis()
    wow = self.kpis["wow"]
    wow_txt = "N/A" if (isinstance(wow, float) and (math.isnan(wow) or math.isinf(wow))) else f"{wow:.1f}%"
    prod = self.kpis["by_product"].head(3)
    reg = self.kpis["by_region"].head(3)
    return (
        f"Toplam Gelir: {self.kpis['total']:,.0f}\n"
        f"Ortalama Günlük: {self.kpis['avg']:,.0f}\n"
        f"Son 7g: {self.kpis['last7']:,.0f} | Önceki 7g: {self.kpis['prev7']:,.0f} | WoW: {wow_txt}\n"
        f"En İyi Ürünler:\n{prod.to_string()}\n"
        f"En İyi Bölgeler:\n{reg.to_string()}"
    )

─────────────────────────────────────────────────────────────

Reporting & AI

─────────────────────────────────────────────────────────────

plt.rcParams.update(MPL_PARAMS)

def generate_graphs(kpis: dict) -> dict: files = {} # Daily trend fig, ax = plt.subplots() d = kpis["daily"] ax.plot(d["tarih"], d["net_tutar"], marker="o") ax.set_title("Günlük Gelir Trendleri") fig.autofmt_xdate() fig.savefig("daily.png", dpi=160) plt.close(fig) files["daily"] = "daily.png"

def _plot_series(series: pd.Series, title: str, out_name: str, top_n=5):
    s = series.head(top_n)
    fig, ax = plt.subplots()
    s.plot(kind="bar", ax=ax)
    ax.set_title(title); ax.set_xlabel(""); ax.set_ylabel("Toplam Gelir")
    for i, v in enumerate(s.values):
        ax.text(i, v, f"{v:,.0f}", va="bottom", ha="center", fontsize=9)
    fig.savefig(out_name, dpi=160); plt.close(fig)
    return out_name

files["top_product"] = _plot_series(kpis["by_product"], "Ürün Kırılımı (Top 5)", "top_product.png")
files["top_region"] = _plot_series(kpis["by_region"], "Bölge Kırılımı (Top 5)", "top_region.png")
return files

def ai_summary(kpi_text: str) -> str: if not (OPENAI_API_KEY and OpenAI): return f"[Stub] Yönetici özeti (AI kapalı):\n{kpi_text}" try: client = OpenAI(api_key=OPENAI_API_KEY) prompt = ( "You are Dr. Sarah Chen, a Stanford PhD data scientist (10y exp). " "Write a concise executive summary for the following metrics. " "Style: confident, analytical, strategic; 5 bullets; then 3 action items.\n\n" f"Metrics:\n{kpi_text}" ) resp = client.chat.completions.create( model="gpt-4o", messages=[{"role": "user", "content": prompt}], temperature=0.2, ) return resp.choices[0].message.content.strip() except Exception as e: return f"[Hata] AI özeti alınamadı: {e}\n\n{kpi_text}"

PDF

class _PDF(FPDF): def header(self): self.set_font("Helvetica", "B", 16) self.cell(0, 10, f"{APP_NAME} Yönetici Raporu", 0, 1, "C") self.set_font("Helvetica", "", 9) self.cell(0, 6, f"{BRAND_TAGLINE}  |  {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1, "C") self.ln(2)

def footer(self):
    self.set_y(-15)
    self.set_font("Helvetica", "I", 8)
    self.cell(0, 10, f"MetriqAI Analytics • Confidential • Page {self.page_no()}", 0, 0, "C")

def build_pdf(ai_text: str, kpis: dict, graphs: dict, out="metriqAI_report.pdf"): pdf = _PDF(); pdf.set_auto_page_break(True, margin=12) pdf.add_page()

pdf.set_font("Helvetica", "B", 13)
pdf.cell(0, 8, "AI Özet ve Öneriler", ln=True)
pdf.set_font("Helvetica", "", 11)
for line in ai_text.split("\n"):
    pdf.multi_cell(0, 6, line)

# Daily
pdf.add_page()
pdf.set_font("Helvetica", "B", 12); pdf.cell(0, 8, "Günlük Gelir Trendleri", ln=True)
if os.path.exists(graphs.get("daily", "")):
    pdf.image(graphs["daily"], w=180)

# Product
pdf.ln(2); pdf.set_font("Helvetica", "B", 12); pdf.cell(0, 8, "Ürün Kırılımı (Top 5)", ln=True)
if os.path.exists(graphs.get("top_product", "")):
    pdf.image(graphs["top_product"], w=180)

# Region
pdf.ln(2); pdf.set_font("Helvetica", "B", 12); pdf.cell(0, 8, "Bölge Kırılımı (Top 5)", ln=True)
if os.path.exists(graphs.get("top_region", "")):
    pdf.image(graphs["top_region"], w=180)

pdf.output(out)
return out

DOCX

def build_docx(df: pd.DataFrame, ai_text: str, out="metriqAI_report.docx"): doc = Document() doc.add_heading(f"{APP_NAME} — Executive Summary", 0) doc.add_paragraph(BRAND_TAGLINE) doc.add_heading("AI Strategic Analysis", level=1) for p in ai_text.split("\n"): doc.add_paragraph(p) doc.add_heading("Sample Data Preview", level=1) doc.add_paragraph(str(df.head(10))) doc.save(out) return out

PPTX

def build_ppt(ai_text: str, graphs: dict, out="metriqAI_presentation.pptx"): prs = Presentation() title_slide_layout = prs.slide_layouts[0] slide = prs.slides.add_slide(title_slide_layout) slide.shapes.title.text = f"{APP_NAME} Executive Deck" slide.placeholders[1].text = BRAND_TAGLINE

# AI text slide
layout = prs.slide_layouts[1]
s2 = prs.slides.add_slide(layout)
s2.shapes.title.text = "AI Strategic Summary"
s2.placeholders[1].text = ai_text

# Graph slides
for key, cap in [("daily", "Daily Revenue"), ("top_product", "Top Products"), ("top_region", "Top Regions")]:
    if os.path.exists(graphs.get(key, "")):
        s = prs.slides.add_slide(prs.slide_layouts[5])
        s.shapes.title.text = cap
        left = Inches(1); top = Inches(1.5); height = Inches(4)
        s.shapes.add_picture(graphs[key], left, top, height=height)

prs.save(out)
return out

Excel

def save_excel(df: pd.DataFrame, out="data_clean.xlsx"): df.to_excel(out, index=False) return out

─────────────────────────────────────────────────────────────

UI Components (CSS, hero, sidebar, animation)

─────────────────────────────────────────────────────────────

def load_custom_css(): st.markdown( """ <style> @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&family=Open+Sans:wght@300;400;600&display=swap'); .main { background: linear-gradient(135deg,#0f2027 0%,#203a43 50%,#2c5364 100%); font-family:'Open Sans',sans-serif; } .logo-container { text-align:center; padding:3rem 2rem; background:rgba(255,255,255,.05); backdrop-filter:blur(20px); border-radius:20px; margin-bottom:2rem; border:1px solid rgba(255,255,255,.1); box-shadow:0 8px 32px rgba(0,0,0,.3); } .logo-title { font-family:'Montserrat',sans-serif; font-size:3.2rem; font-weight:700; margin:0; background:linear-gradient(135deg,#00BFFF 0%,#0080FF 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; text-shadow:0 0 40px rgba(0,191,255,.5); } .logo-tagline { color:rgba(255,255,255,.9); font-size:1.1rem; font-weight:300; margin-top:.6rem; letter-spacing:2px; } div[data-testid="metric-container"]{background:linear-gradient(135deg,rgba(0,191,255,.1) 0%,rgba(0,128,255,.1) 100%); border-radius:15px; padding:20px; border-left:5px solid #00BFFF; border:1px solid rgba(0,191,255,.3); box-shadow:0 8px 16px rgba(0,0,0,.3);} .stDownloadButton button{background:linear-gradient(135deg,#00BFFF 0%,#0080FF 100%); color:#fff; border:none; border-radius:12px; padding:12px 22px; font-weight:600; box-shadow:0 4px 12px rgba(0,191,255,.4);} .stDownloadButton button:hover{transform:translateY(-2px);} .stProgress > div > div > div > div{ background:linear-gradient(90deg,#00BFFF,#0080FF,#00BFFF); background-size:200% 100%; animation: shimmer 2s infinite; } @keyframes shimmer{0%{background-position:200% 0}100%{background-position:-200% 0}} section[data-testid="stSidebar"]{ background: linear-gradient(180deg,#0f2027 0%,#203a43 100%); border-right:1px solid rgba(0,191,255,.2); } .team-card{ padding:12px; margin:8px 0; background:rgba(255,255,255,.05); border-radius:12px; border:1px solid rgba(0,191,255,.2); } .processing-container{ text-align:center; padding:2rem; background:rgba(0,191,255,.05); border-radius:15px; border:1px solid rgba(0,191,255,.3); margin:1rem 0; } .footer{ text-align:center; padding:2rem 0; color:rgba(255,255,255,.5); font-size:.9rem; border-top:1px solid rgba(255,255,255,.1); margin-top:2rem; } </style> """, unsafe_allow_html=True, )

def render_hero(): st.markdown( f""" <div class="logo-container"> <h1 class="logo-title">⚡ {APP_NAME}</h1> <p class="logo-tagline">{BRAND_TAGLINE}</p> </div> """, unsafe_allow_html=True, )

def render_package_selector(): st.sidebar.markdown("---") st.sidebar.markdown("### 💎 Select Your Package") selected = st.sidebar.radio("Choose a plan:", list(PACKAGES.keys())) pkg = PACKAGES[selected] st.sidebar.markdown( f"<div style='background:rgba(255,255,255,.05);padding:16px;border-radius:12px;border:2px solid {pkg['color']};margin:8px 0;'>" f"<h3 style='color:{pkg['color']};margin:0'>{selected}</h3>" f"<p style='font-size:1.6rem;color:#fff;margin:6px 0'>{pkg['price']}</p>" f"<p style='color:rgba(255,255,255,.7);margin:0'>⏱️ Delivery: {pkg['delivery']}</p>" f"</div>", unsafe_allow_html=True, ) st.sidebar.markdown("Features:") feature_names = { "pdf_report": "📑 PDF Report", "excel_export": "📊 Excel Export", "ai_summary": "🤖 AI Strategic Summary", "interactive_charts": "📈 Interactive Charts", "turkey_map": "🇹🇷 Turkey Heatmap", "world_map": "🌍 World Map", "powerpoint": "📊 PowerPoint Deck", "email_delivery": "📧 Email Delivery", "video_walkthrough": "🎥 Video Walkthrough", "priority_support": "⚡ Priority Support", } for key, name in feature_names.items(): st.sidebar.markdown(("✅ " if pkg["features"][key] else "❌ ") + name) return selected

def render_team_section(): st.sidebar.markdown("---") st.sidebar.markdown("### 👥 Your Analyst Team") for m in TEAM_MEMBERS: st.sidebar.markdown( f"<div class='team-card'><div style='font-size:1.6rem'>{m['avatar']}</div>" f"<strong style='color:#00BFFF'>{m['name']}</strong><br>" f"<small style='color:rgba(255,255,255,.7)'>{m['role']}</small><br>" f"<small style='color:rgba(255,255,255,.5)'>{m['bio']}</small></div>", unsafe_allow_html=True, )

def simulate_processing(package_name: str): stages_map = { "🟢 Basic": [(0, "📥 Loading data..."), (25, "🧹 Cleaning..."), (50, "📊 Stats..."), (75, "📄 PDF..."), (100, "✅ Done!")], "🔵 Pro":   [(0, "📥 Loading data..."), (20, "🧹 Preprocessing..."), (40, "📊 Analytics..."), (60, "🤖 AI..."), (80, "📈 Charts..."), (100, "✅ Complete!")], "🔴 Premium": [(0, "📥 Ingesting..."), (15, "🧹 Cleaning..."), (30, "📊 Multi-dim analysis..."), (45, "🤖 AI engines..."), (60, "🗺️ Geo maps..."), (80, "📦 Packaging..."), (100, "✅ Premium done!")], } stages = stages_map.get(package_name, stages_map["🟢 Basic"]) c = st.empty() with c.container(): st.markdown("<div class='processing-container'><div style='font-size:2rem'>⚙️</div><h4>Processing...</h4></div>", unsafe_allow_html=True) bar = st.progress(0) msg = st.empty() for p, txt in stages: msg.markdown(f"{txt}"); bar.progress(p); time.sleep(0.35) msg.success("🎉 Ready!"); time.sleep(0.5) c.empty()

def render_footer(): st.markdown( """ <div class="footer"> <p><strong>metriq.AI Analytics</strong> • Confidential & Proprietary</p> <p>📧 insights@metriq.ai • 🌐 metriq.ai • 📞 +90 XXX XXX XXXX</p> <p style='font-size:.8rem'>© 2025 MetriqAI. All rights reserved.</p> </div> """, unsafe_allow_html=True, )

─────────────────────────────────────────────────────────────

Maps & Interactive Charts

─────────────────────────────────────────────────────────────

def create_turkey_heatmap(df): if "sehir" not in df.columns: st.info("Heatmap requires 'sehir' column.") return None city_revenue = df.groupby("sehir")["net_tutar"].sum().reset_index() city_revenue["lat"] = city_revenue["sehir"].map(lambda x: TURKEY_CITIES.get(x, {}).get("lat", 39.0)) city_revenue["lon"] = city_revenue["sehir"].map(lambda x: TURKEY_CITIES.get(x, {}).get("lon", 35.0)) fig = px.scatter_mapbox( city_revenue, lat="lat", lon="lon", size="net_tutar", color="net_tutar", hover_name="sehir", hover_data={"net_tutar":":,.0f", "lat": False, "lon": False}, color_continuous_scale="Blues", size_max=50, zoom=5, center={"lat":39.0, "lon":35.0}, title="🇹🇷 Turkey Revenue Heatmap", ) fig.update_layout(mapbox_style="carto-darkmatter", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)") return fig

def create_world_map(df): dfx = df.copy() if "ulke" not in dfx.columns: dfx["ulke"] = dfx.get("sehir", pd.Series(["Turkey"]*len(dfx))).apply(lambda _: "Turkey") country = dfx.groupby("ulke")["net_tutar"].sum().reset_index().rename(columns={"ulke":"country"}) fig = px.choropleth(country, locations="country", locationmode="country names", color="net_tutar", hover_name="country", color_continuous_scale="Viridis", title="🌍 Global Revenue Distribution") fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)") return fig

def create_interactive_bar_chart(df, column, title): data = df.groupby(column)["net_tutar"].sum().sort_values(ascending=False).head(10) fig = go.Figure([go.Bar(x=data.index, y=data.values, text=data.values, texttemplate="%{text:,.0f} TL", textposition="outside")]) fig.update_layout(title=title, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)") return fig

def create_time_series_chart(df): daily = df.groupby("tarih")["net_tutar"].sum().reset_index().sort_values("tarih") fig = go.Figure() fig.add_trace(go.Scatter(x=daily["tarih"], y=daily["net_tutar"], mode="lines+markers", name="Daily Revenue")) if len(daily) >= 7: daily["ma7"] = daily["net_tutar"].rolling(7).mean() fig.add_trace(go.Scatter(x=daily["tarih"], y=daily["ma7"], mode="lines", name="7-Day Trend")) fig.update_layout(title="📈 Daily Revenue Trend", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)") return fig

─────────────────────────────────────────────────────────────

Streamlit App

─────────────────────────────────────────────────────────────

st.set_page_config(page_title=f"{APP_NAME} Dashboard", layout="wide", page_icon="⚡", initial_sidebar_state="expanded") load_custom_css()

Sidebar

selected_package = render_package_selector() render_team_section() st.sidebar.markdown("---") st.sidebar.markdown("### 📞 Contact") st.sidebar.markdown("📧 insights@metriq.ai") st.sidebar.markdown("🌐 metriq.ai") st.sidebar.markdown("📞 +90 XXX XXX XXXX")

Main

render_hero()

st.markdown("### 📂 Upload Your Data") uploaded_file = st.file_uploader("Drop your Excel or CSV file here", type=["xlsx", "xls", "csv"], help="Upload sales data for instant AI-powered analysis")

if uploaded_file: try: analyzer = SalesAnalyzer.load_data(uploaded_file) simulate_processing(selected_package) kpis = analyzer.compute_kpis()

st.markdown("---")
    st.markdown("### 🎯 Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Revenue", f"{kpis['total']:,.0f} TL")
    col2.metric("📊 Daily Average", f"{kpis['avg']:,.0f} TL")
    wow = kpis["wow"]
    col3.metric("📈 Week-over-Week", "N/A" if pd.isna(wow) else f"{wow:.1f}%")
    col4.metric("🔢 Total Transactions", f"{len(analyzer.df):,}")

    st.markdown("---")
    pkg_features = PACKAGES[selected_package]["features"]

    # AI summary
    if pkg_features["ai_summary"]:
        st.markdown("### 🤖 AI Strategic Analysis")
        if OPENAI_API_KEY:
            with st.spinner("AI is analyzing your data..."):
                summary = ai_summary(analyzer.get_kpi_text())
            st.markdown(f"<div style='background:rgba(0,191,255,.1);border-left:5px solid #00BFFF;padding:16px;border-radius:10px'>{summary}</div>", unsafe_allow_html=True)
        else:
            summary = "[AI] OpenAI API key not found in environment."
            st.warning(summary)
    else:
        summary = "[Basic Package] AI analysis not included."
        st.info(summary)

    st.markdown("---")
    st.markdown("### 📊 Data Visualization")

    # Interactive charts or static graphs
    if pkg_features["interactive_charts"]:
        st.plotly_chart(create_time_series_chart(analyzer.df), use_container_width=True)
        ca, cb = st.columns(2)
        with ca:
            if "kategori" in analyzer.df.columns:
                st.plotly_chart(create_interactive_bar_chart(analyzer.df, "kategori", "📦 Top Categories"), use_container_width=True)
        with cb:
            if "sehir" in analyzer.df.columns:
                st.plotly_chart(create_interactive_bar_chart(analyzer.df, "sehir", "🏙️ Top Cities"), use_container_width=True)
    graphs = generate_graphs(kpis)  # also needed for PDF

    if pkg_features["turkey_map"]:
        st.markdown("### 🇹🇷 Turkey Geographic Analysis")
        fig = create_turkey_heatmap(analyzer.df)
        if fig is not None:
            st.plotly_chart(fig, use_container_width=True)

    if pkg_features["world_map"]:
        st.markdown("### 🌍 Global Market Analysis")
        st.plotly_chart(create_world_map(analyzer.df), use_container_width=True)

    st.markdown("---")
    st.markdown("### 📥 Download Your Reports")

    report_paths = []
    pdf_path = build_pdf(summary, kpis, graphs, "metriqAI_report.pdf"); report_paths.append(pdf_path)
    excel_path = save_excel(analyzer.df, "data_clean.xlsx"); report_paths.append(excel_path)

    docx_path = None
    if pkg_features["ai_summary"]:
        docx_path = build_docx(analyzer.df, summary, "metriqAI_report.docx"); report_paths.append(docx_path)
    pptx_path = None
    if pkg_features["powerpoint"]:
        pptx_path = build_ppt(summary, graphs, "metriqAI_presentation.pptx"); report_paths.append(pptx_path)

    cols = st.columns(5)
    with cols[0]:
        with open(pdf_path, "rb") as f:
            st.download_button("📑 PDF", f, file_name=os.path.basename(pdf_path), mime="application/pdf")
    with cols[1]:
        with open(excel_path, "rb") as f:
            st.download_button("📈 Excel", f, file_name=os.path.basename(excel_path), mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    if docx_path:
        with cols[2]:
            with open(docx_path, "rb") as f:
                st.download_button("📝 Word", f, file_name=os.path.basename(docx_path), mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    if pptx_path:
        with cols[3]:
            with open(pptx_path, "rb") as f:
                st.download_button("📊 PowerPoint", f, file_name=os.path.basename(pptx_path), mime="application/vnd.openxmlformats-officedocument.presentationml.presentation")

    if pkg_features["ai_summary"]:
        buffer = BytesIO()
        with zipfile.ZipFile(buffer, "w") as zf:
            for pth in report_paths:
                if pth and os.path.exists(pth):
                    zf.write(pth, os.path.basename(pth))
        buffer.seek(0)
        with cols[4]:
            st.download_button("📦 ZIP", buffer, file_name="metriqAI_package.zip", mime="application/zip")

    # cleanup
    def _cleanup(paths: list, graphs_dict: dict):
        all_files = list(graphs_dict.values()) + [p for p in paths if p and os.path.exists(p)]
        all_files.extend(glob.glob("*.zip"))
        for f in set(all_files):
            try:
                if os.path.exists(f):
                    os.remove(f)
            except Exception:
                pass
    _cleanup(report_paths, graphs)

except Exception as e:
    st.error(f"⚠️ Error processing data: {str(e)}")
    st.info("Ensure your file has at least 'tarih' (date) and 'net_tutar' (amount) columns.")

else: st.markdown("---") st.info("👆 Upload an Excel/CSV to start analysis. Expected columns: tarih, net_tutar, (optional: kategori, sehir)")

render_footer()

