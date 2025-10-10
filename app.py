import streamlit as st
import pandas as pd
from datetime import datetime


def generate_summary_report(df):
    """
    DataFrame'den özet rapor oluştur
    """
    try:
        # Summary verilerini hesapla
        total_revenue = df['net_tutar'].sum()
        daily_average = df.groupby('tarih')['net_tutar'].sum().mean()
        total_transactions = len(df)
        
        # Tarih aralığı
        start_date = df['tarih'].min()
        end_date = df['tarih'].max()
        
        # Haftalık büyüme hesapla
        df_sorted = df.sort_values('tarih')
        if len(df_sorted) >= 7:
            last_week = df_sorted.tail(7)['net_tutar'].sum()
            prev_week = df_sorted.iloc[-14:-7]['net_tutar'].sum() if len(df_sorted) >= 14 else last_week
            wow_growth = ((last_week - prev_week) / prev_week * 100) if prev_week > 0 else 0
        else:
            wow_growth = 0
        
        # En yüksek gelirli şehir
        if 'sehir' in df.columns:
            top_city = df.groupby('sehir')['net_tutar'].sum().idxmax()
            top_city_revenue = df.groupby('sehir')['net_tutar'].sum().max()
        else:
            top_city = "N/A"
            top_city_revenue = 0
        
        # En yüksek gelirli kategori
        if 'kategori' in df.columns:
            top_category = df.groupby('kategori')['net_tutar'].sum().idxmax()
            top_category_revenue = df.groupby('kategori')['net_tutar'].sum().max()
        else:
            top_category = "N/A"
            top_category_revenue = 0
        
        # Rapor metni oluştur
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║              MetriqAI Analytics - Özet Rapor                 ║
╚══════════════════════════════════════════════════════════════╝

📅 RAPOR TARİHİ: {datetime.now().strftime('%d.%m.%Y %H:%M')}
📊 VERİ DÖNEMİ: {start_date} - {end_date}

═══════════════════════════════════════════════════════════════

💰 GELİR ÖZETİ
───────────────────────────────────────────────────────────────
   Toplam Gelir          : {total_revenue:,.2f} TL
   Günlük Ortalama       : {daily_average:,.2f} TL
   Haftalık Büyüme       : {wow_growth:,.1f}%

═══════════════════════════════════════════════════════════════

📦 İŞLEM BİLGİLERİ
───────────────────────────────────────────────────────────────
   Toplam İşlem Sayısı   : {total_transactions:,}
   İşlem Başı Ortalama   : {(total_revenue/total_transactions):,.2f} TL

═══════════════════════════════════════════════════════════════

🏆 EN YÜKSEK PERFORMANS
───────────────────────────────────────────────────────────────
   En İyi Şehir          : {top_city}
   Şehir Geliri          : {top_city_revenue:,.2f} TL
   
   En İyi Kategori       : {top_category}
   Kategori Geliri       : {top_category_revenue:,.2f} TL

═══════════════════════════════════════════════════════════════

📈 ŞEHİRLERE GÖRE DAĞILIM
───────────────────────────────────────────────────────────────
"""
        
        # Şehir bazlı detaylar ekle
        if 'sehir' in df.columns:
            city_summary = df.groupby('sehir')['net_tutar'].agg(['sum', 'count']).sort_values('sum', ascending=False).head(10)
            for city, row in city_summary.iterrows():
                report += f"   {city:<20} : {row['sum']:>15,.2f} TL  ({row['count']:>5,} işlem)\n"
        
        report += f"""
═══════════════════════════════════════════════════════════════

📊 KATEGORİLERE GÖRE DAĞILIM
───────────────────────────────────────────────────────────────
"""
        
        # Kategori bazlı detaylar ekle
        if 'kategori' in df.columns:
            cat_summary = df.groupby('kategori')['net_tutar'].agg(['sum', 'count']).sort_values('sum', ascending=False).head(10)
            for category, row in cat_summary.iterrows():
                report += f"   {category:<20} : {row['sum']:>15,.2f} TL  ({row['count']:>5,} işlem)\n"
        
        report += f"""
═══════════════════════════════════════════════════════════════

Bu rapor MetriqAI Analytics tarafından otomatik oluşturulmuştur.
📧 İletişim: insights@metriq.ai
🌐 Web: metriq.ai

© 2025 MetriqAI. Tüm hakları saklıdır.
"""
        
        return report
        
    except Exception as e:
        return f"HATA: Rapor oluşturulamadı.\nDetay: {str(e)}"


def create_excel_report(df):
    """
    Excel formatında rapor oluştur
    """
    from io import BytesIO
    
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Ana veri
        df.to_excel(writer, sheet_name='Ana Veri', index=False)
        
        # Şehir özeti
        if 'sehir' in df.columns:
            city_summary = df.groupby('sehir')['net_tutar'].agg(['sum', 'count', 'mean']).round(2)
            city_summary.columns = ['Toplam Gelir', 'İşlem Sayısı', 'Ortalama']
            city_summary.to_excel(writer, sheet_name='Şehir Özeti')
        
        # Günlük özet
        daily_summary = df.groupby('tarih')['net_tutar'].agg(['sum', 'count', 'mean']).round(2)
        daily_summary.columns = ['Toplam Gelir', 'İşlem Sayısı', 'Ortalama']
        daily_summary.to_excel(writer, sheet_name='Günlük Özet')
        
        # Kategori özeti
        if 'kategori' in df.columns:
            cat_summary = df.groupby('kategori')['net_tutar'].agg(['sum', 'count', 'mean']).round(2)
            cat_summary.columns = ['Toplam Gelir', 'İşlem Sayısı', 'Ortalama']
            cat_summary.to_excel(writer, sheet_name='Kategori Özeti')
    
    output.seek(0)
    return output


# Ana app.py dosyanızda bu şekilde kullanın:

st.markdown("## 📥 Rapor İndir")

col1, col2 = st.columns(2)

with col1:
    # TXT Raporu
    if st.button("📄 Metin Raporu İndir", use_container_width=True):
        try:
            report_text = generate_summary_report(df)
            
            st.download_button(
                label="💾 Raporu Kaydet (.txt)",
                data=report_text,
                file_name=f"metriqAI_rapor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
            
            # Önizleme göster
            with st.expander("📋 Rapor Önizleme"):
                st.text(report_text)
                
        except Exception as e:
            st.error(f"❌ Rapor oluşturma hatası: {str(e)}")

with col2:
    # Excel Raporu
    if st.button("📊 Excel Raporu İndir", use_container_width=True):
        try:
            excel_data = create_excel_report(df)
            
            st.download_button(
                label="💾 Excel'i Kaydet (.xlsx)",
                data=excel_data,
                file_name=f"metriqAI_rapor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            
            st.success("✅ Excel raporu hazır!")
            
        except Exception as e:
            st.error(f"❌ Excel oluşturma hatası: {str(e)}")pip install openpyxl
