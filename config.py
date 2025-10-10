"""
config.py - MetriqAI Configuration
"""

import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "metriq.AI"
BRAND_TAGLINE = "Insights at the Speed of Thought"
VERSION = "2.0"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

PACKAGES = {
    "Basic": {
        "emoji": "🟢",
        "price": "$497",
        "delivery": "24 hours",
        "features": {
            "pdf_report": True,
            "excel_export": True,
            "ai_summary": False,
            "interactive_charts": False,
            "turkey_map": False,
            "world_map": False,
            "powerpoint": False,
            "email_delivery": False,
            "video_walkthrough": False,
            "priority_support": False
        },
        "color": "#27AE60"
    },
    "Pro": {
        "emoji": "🔵",
        "price": "$997",
        "delivery": "12 hours",
        "features": {
            "pdf_report": True,
            "excel_export": True,
            "ai_summary": True,
            "interactive_charts": True,
            "turkey_map": True,
            "world_map": False,
            "powerpoint": True,
            "email_delivery": True,
            "video_walkthrough": False,
            "priority_support": True
        },
        "color": "#3498DB"
    },
    "Premium": {
        "emoji": "🔴",
        "price": "$1,997",
        "delivery": "6 hours",
        "features": {
            "pdf_report": True,
            "excel_export": True,
            "ai_summary": True,
            "interactive_charts": True,
            "turkey_map": True,
            "world_map": True,
            "powerpoint": True,
            "email_delivery": True,
            "video_walkthrough": True,
            "priority_support": True
        },
        "color": "#E74C3C"
    }
}

TEAM_MEMBERS = [
    {
        "name": "Dr. Sarah Chen",
        "role": "Lead Data Scientist",
        "avatar": "👩‍🔬",
        "bio": "PhD Machine Learning, Stanford"
    },
    {
        "name": "Marcus Rodriguez",
        "role": "Senior BI Consultant",
        "avatar": "👨‍💼",
        "bio": "MBA Harvard, Ex-McKinsey"
    },
    {
        "name": "Emily Thompson",
        "role": "Strategic Analyst",
        "avatar": "👩‍💻",
        "bio": "MSc Data Science, MIT"
    }
]

TURKEY_CITIES = {
    "Istanbul": {"lat": 41.0082, "lon": 28.9784},
    "Ankara": {"lat": 39.9334, "lon": 32.8597},
    "Izmir": {"lat": 38.4237, "lon": 27.1428},
    "Bursa": {"lat": 40.1826, "lon": 29.0665},
    "Antalya": {"lat": 36.8969, "lon": 30.7133},
    "Adana": {"lat": 37.0000, "lon": 35.3213},
    "Gaziantep": {"lat": 37.0662, "lon": 37.3833},
    "Konya": {"lat": 37.8746, "lon": 32.4932},
    "Mersin": {"lat": 36.8121, "lon": 34.6415},
    "Kayseri": {"lat": 38.7312, "lon": 35.4787}
}
