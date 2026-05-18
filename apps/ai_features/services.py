#!/usr/bin/env python
"""
OpenAI Integration Service
Demo version - ready for production use
"""

import openai
from django.conf import settings
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)

class OpenAIService:
    """Service class for OpenAI API interactions"""
    
    def __init__(self):
        """Initialize OpenAI client"""
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
            self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            self.enabled = True
        else:
            self.client = None
            self.enabled = False
            logger.warning("OpenAI API key not configured. Running in demo mode.")
    
    def generate_summary(self, workspace_name: str, stats: Dict) -> str:
        """Generate AI-powered summary for workspace"""
        
        if not self.enabled:
            return self._generate_demo_summary(workspace_name, stats)
        
        try:
            prompt = f"""Generate a professional business summary in Uzbek language:

Workspace: {workspace_name}
Statistics:
- Total clients: {stats.get('total_clients', 0)}
- Total orders: {stats.get('total_orders', 0)}
- Today's orders: {stats.get('today_orders', 0)}
- Today's revenue: {stats.get('today_revenue', 0)} UZS

Please provide:
1. Summary of current performance
2. Key insights
3. Actionable recommendations

Format: Markdown with emojis"""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a business analyst AI assistant. Provide professional, concise insights in Uzbek language."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return self._generate_demo_summary(workspace_name, stats)
    
    def analyze_client(self, client_data: Dict) -> str:
        """Generate AI insights for a client"""
        
        if not self.enabled:
            return self._generate_demo_client_insights(client_data)
        
        try:
            prompt = f"""Analyze this client and provide insights in Uzbek language:

Client Name: {client_data.get('name', 'Unknown')}
Total Orders: {client_data.get('order_count', 0)}
Total Spent: {client_data.get('total_spent', 0)} UZS
Source: {client_data.get('source', 'Unknown')}
Tags: {client_data.get('tags', '')}

Provide:
1. Client behavior analysis
2. Recommendations for engagement
3. Potential upsell opportunities

Format: Markdown with emojis"""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a customer relationship AI assistant. Provide personalized insights in Uzbek language."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=400
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return self._generate_demo_client_insights(client_data)
    
    def generate_email(self, template_type: str, context: Dict) -> str:
        """Generate email content using AI"""
        
        if not self.enabled:
            return f"Demo email for {template_type}"
        
        try:
            prompt = f"""Generate a professional email in Uzbek language:

Template Type: {template_type}
Context: {context}

Requirements:
- Professional tone
- Clear call-to-action
- Proper formatting

Output: Email content only"""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional email writer. Create engaging, professional emails in Uzbek language."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return f"Demo email for {template_type}"
    
    def _generate_demo_summary(self, workspace_name: str, stats: Dict) -> str:
        """Generate demo summary when OpenAI is not configured"""
        return f"""🤖 **AI Kunlik Hisobot (DEMO)**

📊 **Umumiy Ko'rsatkichlar:**
• Jami mijozlar: {stats.get('total_clients', 0)}
• Jami buyurtmalar: {stats.get('total_orders', 0)}

📅 **Bugungi Statistikasi:**
• Bugungi buyurtmalar: {stats.get('today_orders', 0)}
• Bugungi tushum: {stats.get('today_revenue', 0)} so'm

💡 **AI Tavsiyalari:**
1. Mijozlar bazangiz o'smoqda, tabriklaymiz!
2. Buyurtmalar sonini oshirish uchun marketing kampaniyasini boshlang
3. Telegram bot orqali mijozlar bilan aloqani kuchaytiring

⚡ **Keyingi Qadamlar:**
• Yangi mijozlar qo'shing
• Buyurtmalarni kuzatib boring
• Hisobotlarni tahlil qiling

*Bu demo versiya. To'liq AI xususiyatlar OpenAI API ulangandan keyin ishlaydi.*"""
    
    def _generate_demo_client_insights(self, client_data: Dict) -> str:
        """Generate demo client insights when OpenAI is not configured"""
        return f"""🤖 **AI Mijoz Tahlili (DEMO)**

👤 **{client_data.get('name', 'Unknown')}**

📈 **Faoliyat:**
• Buyurtmalar soni: {client_data.get('order_count', 0)}
• Jami xarajat: {client_data.get('total_spent', 0)} so'm
• Manbasi: {client_data.get('source', 'Unknown')}

💡 **Tavsiyalar:**
1. Mijoz faol, maxsus takliflar yuboring
2. Doimiy mijoz dasturiga qo'shing
3. Telegram orqali aloqani davom ettiring

*Bu demo versiya.*"""

# Singleton instance
openai_service = OpenAIService()
