"""
maps.py - Geographic Visualization Module
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from config import TURKEY_CITIES


def create_turkey_heatmap(df):
    """Create Turkey heatmap"""
    try:
        # Veri kontrolü
        if 'sehir' not in df.columns or 'net_tutar' not in df.columns:
            print(f"Sütunlar: {df.columns.tolist()}")
            return go.Figure().update_layout(
                title="Veri sütunları bulunamadı",
                annotations=[dict(text="'sehir' veya 'net_tutar' sütunu bulunamadı", showarrow=False)]
            )
        
        city_revenue = df.groupby('sehir')['net_tutar'].sum().reset_index()
        city_revenue.columns = ['city', 'revenue']
        
        # Koordinatları ekle
        city_revenue['lat'] = city_revenue['city'].map(
            lambda x: TURKEY_CITIES.get(x, {}).get('lat', 39.0)
        )
        city_revenue['lon'] = city_revenue['city'].map(
            lambda x: TURKEY_CITIES.get(x, {}).get('lon', 35.0)
        )
        
        # Geçersiz koordinatları filtrele
        city_revenue = city_revenue[
            (city_revenue['lat'] != 39.0) | (city_revenue['lon'] != 35.0)
        ]
        
        if city_revenue.empty:
            return go.Figure().update_layout(
                title="Şehir koordinatları bulunamadı",
                annotations=[dict(text="TURKEY_CITIES verisini kontrol edin", showarrow=False)]
            )
        
        # Mapbox yerine scatter_geo kullan (token gerektirmez)
        fig = px.scatter_geo(
            city_revenue,
            lat='lat',
            lon='lon',
            size='revenue',
            color='revenue',
            hover_name='city',
            hover_data={
                'revenue': ':,.0f TL', 
                'lat': False, 
                'lon': False
            },
            color_continuous_scale='Blues',
            size_max=50,
            title='Türkiye Gelir Haritası',
            projection='natural earth'
        )
        
        # Türkiye'ye odaklan
        fig.update_geos(
            center=dict(lat=39.0, lon=35.0),
            projection_scale=15,  # Zoom seviyesi
            visible=True,
            resolution=50,
            showcountries=True,
            countrycolor="rgba(255,255,255,0.3)",
            showcoastlines=True,
            coastlinecolor="rgba(255,255,255,0.5)",
            showland=True,
            landcolor="rgba(30,30,30,1)",
            showocean=True,
            oceancolor="rgba(20,20,40,1)",
            showlakes=True,
            lakecolor="rgba(20,20,40,1)"
        )
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=500,
            margin={"r":0,"t":40,"l":0,"b":0}
        )
        
        return fig
        
    except Exception as e:
        print(f"Türkiye haritası hatası: {str(e)}")
        return go.Figure().update_layout(
            title=f"Hata: {str(e)}",
            annotations=[dict(text="Harita oluşturulamadı", showarrow=False)]
        )


def create_world_map(df):
    """Create world map"""
    try:
        # Ülke sütunu kontrolü
        if 'ulke' not in df.columns:
            df['ulke'] = 'Turkey'
        
        if 'net_tutar' not in df.columns:
            print(f"Sütunlar: {df.columns.tolist()}")
            return go.Figure().update_layout(
                title="'net_tutar' sütunu bulunamadı"
            )
        
        country_revenue = df.groupby('ulke')['net_tutar'].sum().reset_index()
        country_revenue.columns = ['country', 'revenue']
        
        # Ülke isimlerini standartlaştır
        country_mapping = {
            'Turkey': 'TUR',
            'Türkiye': 'TUR',
            'USA': 'USA',
            'United States': 'USA',
            'Germany': 'DEU',
            'Almanya': 'DEU'
            # Diğer ülkeleri ekleyin
        }
        
        country_revenue['country_code'] = country_revenue['country'].map(
            lambda x: country_mapping.get(x, x)
        )
        
        fig = px.choropleth(
            country_revenue,
            locations='country_code',
            locationmode='ISO-3',  # ISO-3 ülke kodları
            color='revenue',
            hover_name='country',
            hover_data={'revenue': ':,.0f TL', 'country_code': False},
            color_continuous_scale='Viridis',
            title='Küresel Gelir Dağılımı'
        )
        
        fig.update_geos(
            visible=True,
            showcountries=True,
            countrycolor="rgba(255,255,255,0.3)",
            showcoastlines=True,
            coastlinecolor="rgba(255,255,255,0.5)",
            showland=True,
            landcolor="rgba(30,30,30,1)",
            showocean=True,
            oceancolor="rgba(20,20,40,1)",
            projection_type='natural earth'
        )
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=500,
            margin={"r":0,"t":40,"l":0,"b":0}
        )
        
        return fig
        
    except Exception as e:
        print(f"Dünya haritası hatası: {str(e)}")
        return go.Figure().update_layout(
            title=f"Hata: {str(e)}",
            annotations=[dict(text="Harita oluşturulamadı", showarrow=False)]
        )


def create_interactive_bar_chart(df, column, title):
    """Create interactive bar chart"""
    try:
        if column not in df.columns or 'net_tutar' not in df.columns:
            return go.Figure().update_layout(title=f"Gerekli sütunlar bulunamadı")
        
        data = df.groupby(column)['net_tutar'].sum().sort_values(ascending=False).head(10)
        
        fig = go.Figure(data=[
            go.Bar(
                x=data.index,
                y=data.values,
                marker=dict(
                    color=data.values,
                    colorscale='Blues',
                    showscale=False
                ),
                text=data.values,
                texttemplate='%{text:,.0f} TL',
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Gelir: %{y:,.0f} TL<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title=title,
            xaxis_title=column.capitalize(),
            yaxis_title='Gelir (TL)',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12),
            title_font=dict(size=18, color='#00BFFF'),
            showlegend=False,
            height=400,
            margin={"r":20,"t":60,"l":60,"b":60},
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
        )
        
        return fig
        
    except Exception as e:
        print(f"Bar chart hatası: {str(e)}")
        return go.Figure().update_layout(title=f"Hata: {str(e)}")


def create_time_series_chart(df):
    """Create time series chart"""
    try:
        if 'tarih' not in df.columns or 'net_tutar' not in df.columns:
            return go.Figure().update_layout(title="Gerekli sütunlar bulunamadı")
        
        daily_revenue = df.groupby('tarih')['net_tutar'].sum().reset_index()
        daily_revenue = daily_revenue.sort_values('tarih')
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=daily_revenue['tarih'],
            y=daily_revenue['net_tutar'],
            mode='lines+markers',
            name='Günlük Gelir',
            line=dict(color='#00BFFF', width=3),
            marker=dict(size=8, color='#0080FF'),
            fill='tozeroy',
            fillcolor='rgba(0, 191, 255, 0.2)',
            hovertemplate='<b>%{x}</b><br>Gelir: %{y:,.0f} TL<extra></extra>'
        ))
        
        if len(daily_revenue) >= 7:
            daily_revenue['ma7'] = daily_revenue['net_tutar'].rolling(window=7).mean()
            fig.add_trace(go.Scatter(
                x=daily_revenue['tarih'],
                y=daily_revenue['ma7'],
                mode='lines',
                name='7 Günlük Trend',
                line=dict(color='#FF6B6B', width=2, dash='dash'),
                hovertemplate='<b>%{x}</b><br>Trend: %{y:,.0f} TL<extra></extra>'
            ))
        
        fig.update_layout(
            title='Günlük Gelir Trendi',
            xaxis_title='Tarih',
            yaxis_title='Gelir (TL)',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12),
            title_font=dict(size=18, color='#00BFFF'),
            height=400,
            margin={"r":20,"t":60,"l":60,"b":60},
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            hovermode='x unified',
            legend=dict(
                bgcolor='rgba(0,0,0,0.5)',
                bordercolor='rgba(0, 191, 255, 0.5)',
                borderwidth=1
            )
        )
        
        return fig
        
    except Exception as e:
        print(f"Zaman serisi hatası: {str(e)}")
        return go.Figure().update_layout(title=f"Hata: {str(e)}")
