"""
Dual Calendar Engine (Gregorian + Persian/Shamsi)
"""
from datetime import datetime, timedelta
import json
from pathlib import Path

try:
    import jdatetime
    HAS_JDATETIME = True
except ImportError:
    HAS_JDATETIME = False


class CalendarEngine:
    def __init__(self):
        self.events_file = Path("data/events.json")
        self.events = self._load_events()
    
    def _load_events(self):
        if self.events_file.exists():
            with open(self.events_file, 'r') as f:
                return json.load(f)
        return self._default_events()
    
    def _default_events(self):
        return {
            "gregorian_events": [
                {"date": "2026-12-25", "name": "Christmas", "name_fa": "کریسمس", "icon": "🎄", "impact": "high", "markets": ["forex", "crypto", "gold"], "description": "Markets closed", "description_fa": "بازارها تعطیل"},
                {"date": "2027-01-01", "name": "New Year", "name_fa": "سال نو", "icon": "🎆", "impact": "high", "markets": ["all"], "description": "Global markets closed", "description_fa": "بازارهای جهانی تعطیل"},
                {"date": "2026-11-05", "name": "US Elections", "name_fa": "انتخابات آمریکا", "icon": "🗳️", "impact": "extreme", "markets": ["forex", "crypto", "gold"], "description": "Major volatility", "description_fa": "نوسان شدید"},
                {"date": "2026-12-14", "name": "FOMC Meeting", "name_fa": "فدرال رزرو", "icon": "🏦", "impact": "extreme", "markets": ["forex", "gold"], "description": "Interest rate decision", "description_fa": "تصمیم نرخ بهره"},
            ],
            "persian_events": [
                {"date": "1405-01-01", "name": "Nowruz", "name_fa": "نوروز", "icon": "🌸", "impact": "medium", "markets": ["gold"], "description": "Iranian New Year", "description_fa": "سال نو ایرانی"},
            ]
        }
    
    def get_upcoming_events(self, days_ahead: int = 30):
        today = datetime.now().date()
        end_date = today + timedelta(days=days_ahead)
        upcoming = []
        
        for event in self.events.get("gregorian_events", []):
            event_date = datetime.strptime(event["date"], "%Y-%m-%d").date()
            if today <= event_date <= end_date:
                days_until = (event_date - today).days
                upcoming.append({**event, "days_until": days_until})
        
        upcoming.sort(key=lambda x: x["days_until"])
        return upcoming
    
    def get_today_events(self):
        today = datetime.now().date()
        today_str = today.strftime("%Y-%m-%d")
        return [e for e in self.events.get("gregorian_events", []) if e["date"] == today_str]
    
    def get_today_persian_date(self):
        if HAS_JDATETIME:
            today = jdatetime.date.today()
            return {"year": today.year, "month": today.month, "day": today.day,
                    "month_name": today.strftime('%B'), "weekday": today.strftime('%A')}
        else:
            today = datetime.now()
            return {"year": today.year - 621, "month": (today.month + 2) % 12 or 12,
                    "day": today.day, "month_name": "آبان", "weekday": "دوشنبه"}
    
    def get_persian_calendar_month(self):
        persian_date = self.get_today_persian_date()
        days = [{"day": d, "is_today": d == persian_date["day"], "is_weekend": False} for d in range(1, 31)]
        return {"year": persian_date["year"], "month": persian_date["month"],
                "month_name": persian_date["month_name"], "days": days}
    
    def get_gregorian_calendar_month(self):
        today = datetime.now()
        year, month = today.year, today.month
        last_day = (datetime(year, month + 1, 1) - timedelta(days=1)) if month < 12 else datetime(year + 1, 1, 1) - timedelta(days=1)
        days = [{"day": d, "is_today": d == today.day, "is_weekend": datetime(year, month, d).weekday() >= 5}
                for d in range(1, last_day.day + 1)]
        return {"year": year, "month": month, "month_name": today.strftime('%B'), "days": days}
