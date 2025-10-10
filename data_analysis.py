"""
data_analysis.py - Metriq.AI Veri Analiz Motoru
Yazar: Abdulkadir Yılmaz
Versiyon: 2.0
"""

import pandas as pd
import numpy as np

class SalesAnalyzer:
    def __init__(self, df):
        self.df = df

    # ─────────────────────────────
    # 1️⃣ Veri Yükleme Fonksiyonu
    # ─────────────────────────────
    @staticmethod
    def load_data(uploaded_file):
        """Excel veya CSV dosyasını yükle ve DataFrame döndür"""
        if uploaded_file.name.endswith(".xlsx") or uploaded_file.name.endswith(".xls"):
            df = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file, encoding="utf-8")
        else:
            raise ValueError("Dosya formatı desteklenmiyor. Sadece .xlsx veya .csv yükleyin.")
        
        # Kolon adlarını normalize et
        df.columns = [c.strip().lower() for c in df.columns]
        
        # Tarih kolonunu parse et
        if "tarih" in df.columns:
            df["tarih"] = pd.to_datetime(df["tarih"], errors="coerce")
        
        # Net tutar hatalarını temizle
        if "net_tutar" in df.columns:
            df["net_tutar"] = pd.to_numeric(df["net_tutar"], errors="coerce").fillna(0)
        
        return SalesAnalyzer(df)

    # ─────────────────────────────
    # 2️⃣ KPI Hesaplama
    # ─────────────────────────────
    def compute_kpis(self):
        """Temel KPI’ları döndürür"""
        total = float(self.df["net_tutar"].sum()) if "net_tutar" in self.df else 0
        avg = float(self.df["net_tutar"].mean()) if "net_tutar" in self.df else 0
        count = len(self.df)

        # Haftalık değişim (basit simülasyon)
        if "tarih" in self.df:
            last_week = self.df[self.df["tarih"] > (self.df["tarih"].max() - pd.Timedelta(days=7))]
            prev_week = self.df[self.df["tarih"] <= (self.df["tarih"].max() - pd.Timedelta(days=7))]
            if len(prev_week) > 0:
                wow = ((last_week["net_tutar"].sum() - prev_week["net_tutar"].sum()) /
                       prev_week["net_tutar"].sum()) * 100
            else:
                wow = 0
        else:
            wow = 0

        return {
            "total": total,
            "avg": avg,
            "wow": wow,
            "count": count
        }

    # ─────────────────────────────
    # 3️⃣ KPI Text Formatlama
    # ─────────────────────────────
    def get_kpi_text(self):
        """AI özetleri için KPI verisini metin formatında döndürür"""
        kpis = self.compute_kpis()
        text = (
            f"Toplam gelir: {kpis['total']:,.0f} TL\n"
            f"Günlük ortalama: {kpis['avg']:,.0f} TL\n"
            f"Haftalık değişim: {kpis['wow']:.2f}%\n"
            f"Toplam işlem: {kpis['count']}"
        )
        return text
