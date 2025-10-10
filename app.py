<app.py içeriği buraya yerleşecek>
import warnings
import sys

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
