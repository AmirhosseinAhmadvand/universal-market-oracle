"""
Bilingual News Engine
"""
class NewsEngine:
    def get_latest_news(self, lang: str = "en"):
        news = [
            {"source": "Elon Musk", "source_fa": "ایلان ماسک", "icon": "🚀",
             "title": "Tesla considers Bitcoin payments again",
             "title_fa": "تسلا پرداخت با بیت‌کوین را بررسی می‌کند",
             "time": "2h ago", "time_fa": "۲ ساعت پیش", "impact": "high", "markets": ["crypto"]},
            {"source": "Donald Trump", "source_fa": "دونالد ترامپ", "icon": "🇺🇸",
             "title": "New tariff policy announced",
             "title_fa": "سیاست تعرفه جدید اعلام شد",
             "time": "4h ago", "time_fa": "۴ ساعت پیش", "impact": "extreme", "markets": ["forex", "gold"]},
            {"source": "Federal Reserve", "source_fa": "فدرال رزرو", "icon": "🏦",
             "title": "Interest rate decision next week",
             "title_fa": "تصمیم نرخ بهره هفته آینده",
             "time": "6h ago", "time_fa": "۶ ساعت پیش", "impact": "extreme", "markets": ["forex", "gold"]},
            {"source": "Bitcoin News", "source_fa": "اخبار بیت‌کوین", "icon": "₿",
             "title": "Bitcoin ETF inflows reach new high",
             "title_fa": "ورودی ETF بیت‌کوین رکورد زد",
             "time": "8h ago", "time_fa": "۸ ساعت پیش", "impact": "high", "markets": ["crypto"]},
            {"source": "Gold Market", "source_fa": "بازار طلا", "icon": "🥇",
             "title": "Gold prices surge amid tensions",
             "title_fa": "قیمت طلا افزایش یافت",
             "time": "10h ago", "time_fa": "۱۰ ساعت پیش", "impact": "high", "markets": ["gold"]},
        ]
        
        if lang == "fa":
            return {"status": "success", "news": [{"source": n["source_fa"], "icon": n["icon"],
                     "title": n["title_fa"], "time": n["time_fa"], "impact": n["impact"],
                     "markets": n["markets"]} for n in news]}
        return {"status": "success", "news": [{"source": n["source"], "icon": n["icon"],
                 "title": n["title"], "time": n["time"], "impact": n["impact"],
                 "markets": n["markets"]} for n in news]}
