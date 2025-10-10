"""
reporting.py - Report Generation Module
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from config import OPENAI_API_KEY

try:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
except ImportError:
    client = None


def generate_graphs(kpis):
    """Generate static graphs for PDF"""
    graphs = {}
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot([1, 2, 3, 4, 5], [kpis['avg']] * 5, marker='o', linewidth=2, color='#00BFFF')
    ax.set_title('Daily Revenue Trend', fontsize=16, fontweight='bold')
    ax.set_xlabel('Days')
    ax.set_ylabel('Revenue (TL)')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('daily_trend.png', dpi=150, bbox_inches='tight')
    plt.close()
    graphs['daily'] = 'daily_trend.png'
    
    fig, ax = plt.subplots(figsize=(10, 6))
    categories = ['Category A', 'Category B', 'Category C']
    values = [30000, 25000, 20000]
    ax.bar(categories, values, color='#00BFFF')
    ax.set_title('Top Categories', fontsize=16, fontweight='bold')
    ax.set_ylabel('Revenue (TL)')
    plt.tight_layout()
    plt.savefig('top_product.png', dpi=150, bbox_inches='tight')
    plt.close()
    graphs['top_product'] = 'top_product.png'
    
    fig, ax = plt.subplots(figsize=(10, 6))
    cities = ['City 1', 'City 2', 'City 3']
    values = [40000, 35000, 25000]
    ax.barh(cities, values, color='#3498DB')
    ax.set_title('Regional Distribution', fontsize=16, fontweight='bold')
    ax.set_xlabel('Revenue (TL)')
    plt.tight_layout()
    plt.savefig('top_region.png', dpi=150, bbox_inches='tight')
    plt.close()
    graphs['top_region'] = 'top_region.png'
    
    return graphs


def ai_summary(kpi_text):
    """Generate AI summary using OpenAI"""
    if not client:
        return "AI analysis unavailable. Please configure OpenAI API key in .env file."
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a business analyst expert providing strategic insights."},
                {"role": "user", "content": f"Analyze this business data and provide strategic insights in 3-4 paragraphs:\n\n{kpi_text}"}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI analysis error: {str(e)}"


def build_pdf(summary, kpis, graphs, filename):
    """Build PDF report"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib.utils import ImageReader
        
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        
        c.setFont("Helvetica-Bold", 24)
        c.drawString(100, height - 100, "MetriqAI Analysis Report")
        
        c.setFont("Helvetica", 12)
        y = height - 150
        c.drawString(100, y, f"Total Revenue: {kpis['total']:,.0f} TL")
        c.drawString(100, y - 20, f"Daily Average: {kpis['avg']:,.0f} TL")
        c.drawString(100, y - 40, f"WoW Change: {kpis['wow']:.1f}%")
        
        y -= 100
        c.drawString(100, y, "AI Analysis Summary:")
        c.setFont("Helvetica", 10)
        words = summary.split()[:80]
        line = ""
        for word in words:
            if len(line + word) < 70:
                line += word + " "
            else:
                c.drawString(100, y, line)
                y -= 15
                line = word + " "
        if line:
            c.drawString(100, y, line)
        
        c.showPage()
        c.save()
        return filename
    except Exception as e:
        print(f"PDF Error: {e}")
        return None


def build_docx(df, summary, filename):
    """Build Word document"""
    try:
        from docx import Document
        
        doc = Document()
        doc.add_heading('MetriqAI Analysis Report', 0)
        doc.add_paragraph(f'Total Records: {len(df)}')
        doc.add_heading('AI Strategic Analysis', level=1)
        doc.add_paragraph(summary)
        doc.save(filename)
        return filename
    except Exception as e:
        print(f"DOCX Error: {e}")
        return None


def build_ppt(summary, graphs, filename):
    """Build PowerPoint presentation"""
    try:
        from pptx import Presentation
        
        prs = Presentation()
        
        title_slide = prs.slides.add_slide(prs.slide_layouts[0])
        title = title_slide.shapes.title
        subtitle = title_slide.placeholders[1]
        title.text = "MetriqAI Business Intelligence"
        subtitle.text = "Strategic Insights Report"
        
        bullet_slide = prs.slides.add_slide(prs.slide_layouts[1])
        shapes = bullet_slide.shapes
        title_shape = shapes.title
        body_shape = shapes.placeholders[1]
        title_shape.text = 'AI Strategic Analysis'
        tf = body_shape.text_frame
        tf.text = summary[:300]
        
        prs.save(filename)
        return filename
    except Exception as e:
        print(f"PPT Error: {e}")
        return None


def save_excel(df, filename):
    """Save dataframe to Excel"""
    try:
        df.to_excel(filename, index=False)
        return filename
    except Exception as e:
        print(f"Excel Error: {e}")
        return None
