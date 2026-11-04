"""
Smart Chatbot - Works Online and Offline
"""
import re
from datetime import datetime


class ChatBot:
    def __init__(self):
        self.responses = self._load_responses()
    
    def _load_responses(self):
        return {
            "greetings": {
                "patterns": ["hello", "hi", "hey", "سلام", "درود", "سلام علیکم"],
                "response": "Hello! I'm your Market Oracle Assistant. How can I help you today? 🤖"
            },
            "price_queries": {
                "patterns": ["price", "قیمت", "how much", "چقدر", "rate", "نرخ"],
                "response": "You can check real-time prices on the dashboard. Select any asset from the search bar to see live prices updated every 3 seconds! 📊"
            },
            "buy_sell": {
                "patterns": ["buy", "sell", "خرید", "فروش", "should i buy", "should i sell", "time to buy", "time to sell"],
                "response": "Check the 'Trading Signal' card on the dashboard. It shows BUY/SELL/HOLD signals with confidence percentage based on RSI and Moving Averages. Always do your own research! ⚠️"
            },
            "bitcoin": {
                "patterns": ["bitcoin", "btc", "بیت کوین", "بیت‌کوین"],
                "response": "Bitcoin (BTC) is the world's first cryptocurrency. Select it from the search bar to see live price, predictions, and technical analysis! ₿"
            },
            "ethereum": {
                "patterns": ["ethereum", "eth", "اتریوم"],
                "response": "Ethereum (ETH) is the second-largest cryptocurrency. It powers smart contracts and DeFi. Check its live price on the dashboard! Ξ"
            },
            "gold": {
                "patterns": ["gold", "طلا", "xau"],
                "response": "Gold (XAU) is a safe-haven asset. Its price is influenced by inflation, geopolitical tensions, and dollar strength. Check live prices on the dashboard! 🥇"
            },
            "prediction": {
                "patterns": ["predict", "forecast", "پیش بینی", "future price", "قیمت آینده"],
                "response": "Our AI predicts prices using Moving Average analysis. Check the 'AI Prediction' card and the purple dashed line on the chart for 7-day forecasts! 🔮"
            },
            "calendar": {
                "patterns": ["calendar", "تقویم", "event", "رویداد", "holiday"],
                "response": "Check the Global Events Calendar section! It shows both Gregorian and Persian (Shamsi) dates with market-impacting events. 📅"
            },
            "news": {
                "patterns": ["news", "اخبار", "latest", "جدید"],
                "response": "Check the News Feed section for latest updates from Elon Musk, Donald Trump, Federal Reserve, and major market events! 📰"
            },
            "help": {
                "patterns": ["help", "کمک", "how to use", "راهنما"],
                "response": "1️⃣ Search any asset in the search bar\n2️⃣ Select timeframe (1m, 5m, 1D, 1W, 1M)\n3️⃣ Check live price (updates every 3s)\n4️⃣ View AI predictions\n5️⃣ Read news and calendar events\n6️⃣ Ask me anything! 🤖"
            },
            "thanks": {
                "patterns": ["thanks", "thank you", "ممنون", "مرسی", "تشکر"],
                "response": "You're welcome! Happy trading! 🚀"
            },
            "trump": {
                "patterns": ["trump", "ترامپ"],
                "response": "Donald Trump's policies significantly impact markets. Check the News Feed for his latest statements and their market impact! 🇺🇸"
            },
            "elon": {
                "patterns": ["elon", "musk", "ایلان", "ماسک"],
                "response": "Elon Musk's tweets can move crypto markets! Check the News Feed for his latest posts about Bitcoin, Dogecoin, and Tesla! 🚀"
            }
        }
    
    def get_response(self, message: str) -> str:
        """Get response based on user message."""
        message_lower = message.lower().strip()
        
        if not message_lower:
            return "Please type a message! 💬"
        
        # Check each category
        for category, data in self.responses.items():
            for pattern in data["patterns"]:
                if pattern in message_lower:
                    return data["response"]
        
        # Default response
        return "I'm not sure about that. Try asking about:\n• Prices (bitcoin, ethereum, gold)\n• Buy/Sell signals\n• Predictions\n• Calendar events\n• News\n• Or type 'help' for more options! 🤖"
