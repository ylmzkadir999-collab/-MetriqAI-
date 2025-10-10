import warnings
import sys
import streamlit as st

# Streamlit ve frontend kaynaklı gereksiz uyarıları sustur
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# Tarayıcı (frontend) tarafında çıkan DOM hatalarını yok say
def silence_streamlit_exceptions(exc_type, exc_value, traceback):
    if exc_type.__name__ in ["RuntimeError", "ValueError", "Exception"]:
        print(f"[MetriqAI Silent Mode] Caught harmless error: {exc_value}")
        return True
    return False

sys.excepthook = silence_streamlit_exceptions


# --- Geçici kurtarma ekranı ---
st.set_page_config(page_title="metriq.AI - Recovery Mode", page_icon="⚡")

st.markdown("""
# ⚙️ metriq.AI Safe Mode
Merhaba kanki 😎  
Uygulama şu anda **sessiz modda (crash korumalı)** çalışıyor.

Eğer ana kodları geri yüklemek istiyorsan:
1️⃣ `app.py` dosyasına asıl metriqAI kodlarını tekrar yapıştır.  
2️⃣ Sonra Streamlit’i yeniden başlat (`Rerun` tuşuna bas).  
""")
