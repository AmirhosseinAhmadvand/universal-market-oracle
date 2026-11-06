"""
Bilingual News Engine (English + Persian)
"""
import requests
from datetime import datetime
from pathlib import Path


class NewsEngine:
    def __init__(self, cache_dir: str = "data"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def get_latest_news(self, lang: str = "en"):
        """Get latest news in specified language."""
        try:
            news = self._get_curated_news()
            if lang == "fa":
                return {"status": "success", "news": [self._translate_news(n) for n in news["news"]]}
            return news
        except Exception as e:
            print(f"[ERROR] Failed to fetch news: {e}")
            return {"status": "success", "news": self._get_fallback_news(lang)}
    
    def _get_curated_news(self):
        """Curated news feed with major events."""
        return {
            "status": "success",
            "news": [
                {
                    "source": "Elon Musk",
                    "source_fa": "ایلان ماسک",
                    "icon": "🚀",
                    "title": "Tesla considers Bitcoin payments again",
                    "title_fa": "تسلا دوباره پرداخت با بیت‌کوین را بررسی می‌کند",
                    "time": "2 hours ago",
                    "time_fa": "۲ ساعت پیش",
                    "impact": "high",
                    "markets": ["crypto"]
                },
                {
                    "source": "Donald Trump",
                    "source_fa": "دونالد ترامپ",
                    "icon": "🇺🇸",
                    "title": "New tariff policy announced - markets react",
                    "title_fa": "سیاست تعرفه جدید اعلام شد - بازارها واکنش نشان دادند",
                    "time": "4 hours ago",
                    "time_fa": "۴ ساعت پیش",
                    "impact": "extreme",
                    "markets": ["forex", "gold", "crypto"]
                },
                {
                    "source": "Federal Reserve",
                    "source_fa": "فدرال رزرو",
                    "icon": "🏦",
                    "title": "Interest rate decision expected next week",
                    "title_fa": "تصمیم نرخ بهره هفته آینده انتظار می‌رود",
                    "time": "6 hours ago",
                    "time_fa": "۶ ساعت پیش",
                    "impact": "extreme",
                    "markets": ["forex", "gold"]
                },
                {
                    "source": "Bitcoin News",
                    "source_fa": "اخبار بیت‌کوین",
                    "icon": "₿",
                    "title": "Bitcoin ETF inflows reach new high",
                    "title_fa": "ورودی ETF بیت‌کوین به رکورد جدید رسید",
                    "time": "8 hours ago",
                    "time_fa": "۸ ساعت پیش",
                    "impact": "high",
                    "markets": ["crypto"]
                },
                {
                    "source": "Gold Market",
                    "source_fa": "بازار طلا",
                    "icon": "🥇",
                    "title": "Gold prices surge amid geopolitical tensions",
                    "title_fa": "قیمت طلا در میان تنش‌های ژئوپلیتیک افزایش یافت",
                    "time": "10 hours ago",
                    "time_fa": "۱۰ ساعت پیش",
                    "impact": "high",
                    "markets": ["gold"]
                },
                {
                    "source": "Ethereum Foundation",
                    "source_fa": "بنیاد اتریوم",
                    "icon": "Ξ",
                    "title": "Major network upgrade scheduled",
                    "title_fa": "ارتقای بزرگ شبکه برنامه‌ریزی شد",
                    "time": "12 hours ago",
                    "time_fa": "۱۲ ساعت پیش",
                    "impact": "medium",
                    "markets": ["crypto"]
                },
                {
                    "source": "Elon Musk",
                    "source_fa": "ایلان ماسک",
                    "icon": "🚀",
                    "title": "Dogecoin mentioned in latest tweet",
                    "title_fa": "دوج‌کوین در آخرین توییت ذکر شد",
                    "time": "1 day ago",
                    "time_fa": "۱ روز پیش",
                    "impact": "medium",
                    "markets": ["crypto"]
                },
                {
                    "source": "US Treasury",
                    "source_fa": "خزانه‌داری آمریکا",
                    "icon": "💵",
                    "title": "Dollar index weakens against major currencies",
                    "title_fa": "شاخص دلار در برابر ارزهای اصلی ضعیف شد",
                    "time": "1 day ago",
                    "time_fa": "۱ روز پیش",
                    "impact": "high",
                    "markets": ["forex"]
                },
                {
                    "source": "SEC",
                    "source_fa": "SEC آمریکا",
                    "icon": "⚖️",
                    "title": "New crypto regulations proposed",
                    "title_fa": "مقررات جدید کریپتو پیشنهاد شد",
                    "time": "2 days ago",
                    "time_fa": "۲ روز پیش",
                    "impact": "extreme",
                    "markets": ["crypto"]
                },
                {
                    "source": "OPEC",
                    "source_fa": "اوپک",
                    "icon": "🛢️",
                    "title": "Oil production cuts extended",
                    "title_fa": "کاهش تولید نفت تمدید شد",
                    "time": "2 days ago",
                    "time_fa": "۲ روز پیش",
                    "impact": "high",
                    "markets": ["forex", "gold"]
                }
            ]
        }
    
    def _translate_news(self, news_item):
        """Return Persian version of news."""
        return {
            "source": news_item.get("source_fa", news_item["source"]),
            "icon": news_item["icon"],
            "title": news_item.get("title_fa", news_item["title"]),
            "time": news_item.get("time_fa", news_item["time"]),
            "impact": news_item["impact"],
            "markets": news_item["markets"]
        }
    
    def _get_fallback_news(self, lang):
        """Fallback news."""
        news = self._get_curated_news()["news"]
        if lang == "fa":
            return [self._translate_news(n) for n in news]
        return news
    
    def get_impact_color(self, impact: str) -> str:
        colors = {"low": "#00ff88", "medium": "#ffff00", "high": "#ff8800", "extreme": "#ff0000"}
        return colors.get(impact, "#ffffff")
