"""
ui_components.py - UI Components Module
"""

import streamlit as st
import time
from config import APP_NAME, BRAND_TAGLINE, PACKAGES, TEAM_MEMBERS


def load_custom_css():
    """Load custom CSS styles"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&family=Open+Sans:wght@300;400;600&display=swap');
    
    .main {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        font-family: 'Open Sans', sans-serif;
    }
    
    .logo-container {
        text-align: center;
        padding: 3rem 2rem;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .logo-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 4rem;
        font-weight: 700;
        margin: 0;
        background: linear-gradient(135deg, #00BFFF 0%, #0080FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { filter: brightness(100%); }
        to { filter: brightness(150%); }
    }
    
    .logo-tagline {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.4rem;
        font-weight: 300;
        margin-top: 1rem;
    }
    
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(0, 191, 255, 0.1) 0%, rgba(0, 128, 255, 0.1) 100%);
        border-radius: 15px;
        padding: 25px;
        border-left: 5px solid #00BFFF;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0, 191, 255, 0.4);
    }
    
    .stDownloadButton button {
        background: linear-gradient(135deg, #00BFFF 0%, #0080FF 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 14px 28px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 191, 255, 0.4);
    }
    
    .stDownloadButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0, 191, 255, 0.6);
    }
    
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #00BFFF, #0080FF, #00BFFF);
        background-size: 200% 100%;
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f2027 0%, #203a43 100%);
    }
    
    .team-card {
        padding: 15px;
        margin: 10px 0;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        border: 1px solid rgba(0, 191, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .team-card:hover {
        background: rgba(0, 191, 255, 0.1);
        transform: translateX(5px);
    }
    
    h2, h3 {
        font-family: 'Montserrat', sans-serif;
        color: rgba(255, 255, 255, 0.95);
    }
    
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: rgba(255, 255, 255, 0.5);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 3rem;
    }
    </style>
    """, unsafe_allow_html=True)


def render_hero():
    """Render hero section"""
    st.markdown(f"""
    <div class="logo-container">
        <h1 class="logo-title">⚡ {APP_NAME}</h1>
        <p class="logo-tagline">{BRAND_TAGLINE}</p>
    </div>
    """, unsafe_allow_html=True)


def render_package_selector():
    """Render package selector in sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💎 Select Your Package")
    
    package_names = list(PACKAGES.keys())
    selected = st.sidebar.radio("Choose a plan:", package_names, label_visibility="collapsed")
    
    pkg = PACKAGES[selected]
    
    st.sidebar.markdown(f"""
    <div style='background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; border: 2px solid {pkg['color']}; margin: 15px 0;'>
        <h3 style='color: {pkg['color']}; margin: 0;'>{pkg['emoji']} {selected}</h3>
        <p style='font-size: 1.8rem; font-weight: bold; color: white; margin: 10px 0;'>{pkg['price']}</p>
        <p style='color: rgba(255,255,255,0.7); margin: 5px 0;'>Delivery: {pkg['delivery']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    return selected


def render_team_section():
    """Render team section"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👥 Your Analyst Team")
    
    for member in TEAM_MEMBERS:
        st.sidebar.markdown(f"""
        <div class="team-card">
            <span style='font-size: 2rem;'>{member['avatar']}</span><br>
            <strong style='color: #00BFFF;'>{member['name']}</strong><br>
            <small style='color: rgba(255,255,255,0.7);'>{member['role']}</small><br>
            <small style='color: rgba(255,255,255,0.5);'>{member['bio']}</small>
        </div>
        """, unsafe_allow_html=True)


def simulate_processing(package_name):
    """Simulate processing animation"""
    stages_map = {
        "Basic": [
            (0, "Loading data..."),
            (25, "Cleaning and validating..."),
            (50, "Generating statistics..."),
            (75, "Building PDF report..."),
            (100, "Complete!")
        ],
        "Pro": [
            (0, "Loading data..."),
            (15, "Data preprocessing..."),
            (30, "Statistical analysis..."),
            (45, "AI model initialization..."),
            (60, "Deep learning analysis..."),
            (75, "Creating interactive charts..."),
            (90, "Compiling reports..."),
            (100, "Analysis complete!")
        ],
        "Premium": [
            (0, "Ingesting data streams..."),
            (10, "Advanced data cleaning..."),
            (20, "Multi-dimensional analysis..."),
            (30, "Initializing AI engines..."),
            (40, "Neural network processing..."),
            (50, "Generating geospatial maps..."),
            (60, "Building interactive dashboards..."),
            (70, "Creating PowerPoint deck..."),
            (80, "Recording video walkthrough..."),
            (90, "Packaging deliverables..."),
            (100, "Premium analysis complete!")
        ]
    }
    
    stages = stages_map.get(package_name, stages_map["Basic"])
    
    container = st.empty()
    
    with container.container():
        st.markdown("<div style='text-align: center; padding: 2rem; background: rgba(0, 191, 255, 0.05); border-radius: 15px;'><h3 style='color: #00BFFF;'>⚙️ Analysis in Progress</h3></div>", unsafe_allow_html=True)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for progress, text in stages:
            status_text.markdown(f"**{text}**")
            progress_bar.progress(progress)
            time.sleep(0.3)
        
        status_text.success("🎉 Your analysis is ready!")
        time.sleep(0.5)
    
    container.empty()


def render_footer():
    """Render footer"""
    st.markdown("""
    <div class="footer">
        <p><strong>metriq.AI Analytics</strong> | Confidential & Proprietary</p>
        <p>📧 insights@metriq.ai | 🌐 metriq.ai</p>
        <p style='font-size: 0.8rem; margin-top: 1rem;'>© 2025 MetriqAI. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)
