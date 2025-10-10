"""
data_analysis.py - Data Analysis Module
"""

import pandas as pd
import numpy as np


class SalesAnalyzer:
    """Sales Data Analyzer"""
    
    def __init__(self, df):
        self.df = df
        self._prepare_data()
    
    @classmethod
    def load_data(cls, file_source=None):
        """Load data from file or create stub"""
        if file_source is None:
            df = cls._create_stub_data()
        else:
            if hasattr(file_source, 'name'):
                filename = file_source.name.lower()
                if filename.endswith('.csv'):
                    df = pd.read_csv(file_source)
                else:
                    df = pd.read_excel(file_source)
            else:
                df = pd.read_csv(file_source)
        
        return cls(df)
    
    @staticmethod
    def _create_stub_data():
        """Create sample data for demo"""
        dates = pd.date_range('2024-01-01', periods=180, freq='D')
        categories = ['Electronics', 'Clothing', 'Home', 'Sports', 'Books']
        cities = ['Istanbul', 'Ankara', 'Izmir', 'Bursa', 'Antalya']
        
        data = []
        for _ in range(1000):
            data.append({
                'tarih': np.random.choice(dates),
                'net_tutar': np.random.randint(50, 5000),
                'kategori': np.random.choice(categories),
                'sehir': np.random.choice(cities),
                'durum': np.random.choice(['Completed', 'Cancelled'], p=[0.9, 0.1])
            })
        
        return pd.DataFrame(data)
    
    def _prepare_data(self):
        """Prepare and clean data"""
        if 'tarih' in self.df.columns:
            self.df['tarih'] = pd.to_datetime(self.df['tarih'], errors='coerce')
        
        if 'net_tutar' in self.df.columns:
            self.df['net_tutar'] = pd.to_numeric(self.df['net_tutar'], errors='coerce').fillna(0)
    
    def compute_kpis(self):
        """Compute key performance indicators"""
        total_revenue = self.df['net_tutar'].sum()
        avg_daily = self.df.groupby('tarih')['net_tutar'].sum().mean()
        
        daily_revenue = self.df.groupby('tarih')['net_tutar'].sum().sort_index()
        if len(daily_revenue) >= 14:
            last_7 = daily_revenue.iloc[-7:].sum()
            prev_7 = daily_revenue.iloc[-14:-7].sum()
            wow_change = ((last_7 - prev_7) / prev_7 * 100) if prev_7 > 0 else 0
        else:
            wow_change = np.nan
        
        return {
            'total': total_revenue,
            'avg': avg_daily,
            'wow': wow_change,
            'count': len(self.df)
        }
    
    def get_kpi_text(self):
        """Get KPI summary as text for AI"""
        kpis = self.compute_kpis()
        return f"""
        Total Revenue: {kpis['total']:,.0f} TL
        Average Daily Revenue: {kpis['avg']:,.0f} TL
        Week-over-Week Change: {kpis['wow']:.1f}%
        Total Transactions: {kpis['count']:,}
        """
