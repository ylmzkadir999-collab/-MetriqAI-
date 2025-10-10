"""
maps.py - Geographic Visualization Module
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from config import TURKEY_CITIES


def create_turkey_heatmap(df):
    """Create Turkey heatmap"""
    city_revenue = df.groupby('sehir')['net_tutar'].sum().reset_index()
    city_revenue.columns = ['city', 'revenue']
    
    city_revenue['lat'] = city_revenue['city'].map(lambda x: TURKEY_CITIES.get(x, {}).get('lat', 39.0))
    city_revenue['lon'] = city_revenue['city'].map(lambda x: TURKEY_CITIES.get(x, {}).get('lon', 35.0))
    
    fig = px.scatter_mapbox(
        city_revenue,
        lat='lat',
        lon='lon',
        size='revenue',
        color='revenue',
        hover_name='city',
        hover_data={'revenue': ':,.0f', 'lat': False, 'lon': False},
        color_continuous_scale='Blues',
        size_max=50,
        zoom=5,
        center={"lat": 39.0, "lon": 35.0},
        title='Turkey Revenue Heatmap'
    )
    
    fig.update_layout(
        mapbox_style="carto-darkmatter",
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=500,
        margin={"r":0,"t":40,"l":0,"b":0}
    )
    
    return fig


def create_world_map(df):
    """Create world map"""
    if 'ulke' not in df.columns:
        df['ulke'] = 'Turkey'
    
    country_revenue = df.groupby('ulke')['net_tutar'].sum().reset_index()
    country_revenue.columns = ['country', 'revenue']
    
    fig = px.choropleth(
        country_revenue,
        locations='country',
        locationmode='country names',
        color='revenue',
        hover_name='country',
        hover_data={'revenue': ':,.0f'},
        color_continuous_scale='Viridis',
        title='Global Revenue Distribution'
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=500,
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth',
            bgcolor='rgba(0,0,0,0)'
        ),
        margin={"r":0,"t":40,"l":0,"b":0}
    )
    
    return fig


def create_interactive_bar_chart(df, column, title):
    """Create interactive bar chart"""
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
            hovertemplate='<b>%{x}</b><br>Revenue: %{y:,.0f} TL<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=title,
        xaxis_title=column.capitalize(),
        yaxis_title='Revenue (TL)',
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


def create_time_series_chart(df):
    """Create time series chart"""
    daily_revenue = df.groupby('tarih')['net_tutar'].sum().reset_index()
    daily_revenue = daily_revenue.sort_values('tarih')
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=daily_revenue['tarih'],
        y=daily_revenue['net_tutar'],
        mode='lines+markers',
        name='Daily Revenue',
        line=dict(color='#00BFFF', width=3),
        marker=dict(size=8, color='#0080FF'),
        fill='tozeroy',
        fillcolor='rgba(0, 191, 255, 0.2)',
        hovertemplate='<b>%{x}</b><br>Revenue: %{y:,.0f} TL<extra></extra>'
    ))
    
    if len(daily_revenue) >= 7:
        daily_revenue['ma7'] = daily_revenue['net_tutar'].rolling(window=7).mean()
        fig.add_trace(go.Scatter(
            x=daily_revenue['tarih'],
            y=daily_revenue['ma7'],
            mode='lines',
            name='7-Day Trend',
            line=dict(color='#FF6B6B', width=2, dash='dash'),
            hovertemplate='<b>%{x}</b><br>Trend: %{y:,.0f} TL<extra></extra>'
        ))
    
    fig.update_layout(
        title='Daily Revenue Trend',
        xaxis_title='Date',
        yaxis_title='Revenue (TL)',
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
