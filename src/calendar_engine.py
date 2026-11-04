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
                {"date": "2026-12-25", "name": "Christmas", "name_fa": "کریسمس", "icon": "🎄", "impact": "high", "markets": ["forex", "crypto", "gold"], "description": "Markets closed in US and Europe", "description_fa": "بازارها در آمریکا و اروپا تعطیل"},
                {"date": "2026-10-31", "name": "Halloween", "name_fa": "هالوین", "icon": "🎃", "impact": "low", "markets": [], "description": "Cultural event", "description_fa": "رویداد فرهنگی"},
                {"date": "2027-01-01", "name": "New Year", "name_fa": "سال نو میلادی", "icon": "🎆", "impact": "high", "markets": ["all"], "description": "Global markets closed", "description_fa": "بازارهای جهانی تعطیل"},
                {"date": "2026-11-05", "name": "US Elections", "name_fa": "انتخابات آمریکا", "icon": "🗳️", "impact": "extreme", "markets": ["forex", "crypto", "gold"], "description": "Major market volatility expected", "description_fa": "نوسان شدید بازار انتظار می‌رود"},
                {"date": "2026-12-14", "name": "FOMC Meeting", "name_fa": "جلسه فدرال رزرو", "icon": "🏦", "impact": "extreme", "markets": ["forex", "gold", "crypto"], "description": "Interest rate decision", "description_fa": "تصمیم نرخ بهره"},
                {"date": "2027-02-14", "name": "Valentine's Day", "name_fa": "ولنتاین", "icon": "❤️", "impact": "low", "markets": ["gold"], "description": "Slight increase in gold demand", "description_fa": "افزایش جزئی تقاضای طلا"},
                {"date": "2026-11-27", "name": "Black Friday", "name_fa": "بلک فرایدی", "icon": "🛍️", "impact": "medium", "markets": ["stocks"], "description": "Retail stocks surge", "description_fa": "رشد سهام خرده‌فروشی"},
                {"date": "2026-11-26", "name": "US Thanksgiving", "name_fa": "شکرگزاری آمریکا", "icon": "🦃", "impact": "high", "markets": ["forex"], "description": "US markets closed", "description_fa": "بازارهای آمریکا تعطیل"},
                {"date": "2027-03-17", "name": "St. Patrick's Day", "name_fa": "سنت پاتریک", "icon": "☘️", "impact": "low", "markets": [], "description": "Cultural event", "description_fa": "رویداد فرهنگی"},
                {"date": "2026-12-31", "name": "New Year's Eve", "name_fa": "شب سال نو", "icon": "🎉", "impact": "medium", "markets": ["all"], "description": "Early market close", "description_fa": "بسته شدن زودهنگام بازار"},
            ],
            "persian_events": [
                {"date": "1405-01-01", "name": "Nowruz", "name_fa": "نوروز", "icon": "🌸", "impact": "medium", "markets": ["gold"], "description": "Iranian New Year - gold demand increases", "description_fa": "سال نو ایرانی - افزایش تقاضای طلا"},
                {"date": "1405-01-13", "name": "Sizdah Bedar", "name_fa": "سیزده‌بدر", "icon": "🌿", "impact": "low", "markets": [], "description": "Nature Day in Iran", "description_fa": "روز طبیعت در ایران"},
                {"date": "1405-03-14", "name": "Death of Khomeini", "name_fa": "رحلت امام خمینی", "icon": "🕌", "impact": "low", "markets": [], "description": "National holiday in Iran", "description_fa": "تعطیلی رسمی در ایران"},
                {"date": "1405-03-15", "name": "Revolt of 15 Khordad", "name_fa": "قیام ۱۵ خرداد", "icon": "📜", "impact": "low", "markets": [], "description": "National holiday in Iran", "description_fa": "تعطیلی رسمی در ایران"},
                {"date": "1405-11-22", "name": "Islamic Revolution", "name_fa": "پیروزی انقلاب اسلامی", "icon": "🇮🇷", "impact": "low", "markets": [], "description": "National holiday in Iran", "description_fa": "تعطیلی رسمی در ایران"},
                {"date": "1405-12-29", "name": "Nationalization of Oil", "name_fa": "ملی شدن صنعت نفت", "icon": "🛢️", "impact": "low", "markets": ["gold"], "description": "National holiday in Iran", "description_fa": "تعطیلی رسمی در ایران"},
            ],
            "recurring_events": []
        }
    
    def get_upcoming_events(self, days_ahead: int = 30):
        today = datetime.now().date()
        end_date = today + timedelta(days=days_ahead)
        upcoming = []
        
        for event in self.events.get("gregorian_events", []):
            event_date = datetime.strptime(event["date"], "%Y-%m-%d").date()
            if today <= event_date <= end_date:
                days_until = (event_date - today).days
                upcoming.append({**event, "days_until": days_until, "type": "gregorian"})
        
        upcoming.sort(key=lambda x: x["days_until"])
        return upcoming
    
    def get_today_events(self):
        today = datetime.now().date()
        today_str = today.strftime("%Y-%m-%d")
        events = []
        
        for event in self.events.get("gregorian_events", []):
            if event["date"] == today_str:
                events.append({**event, "type": "gregorian"})
        
        return events
    
    def get_today_persian_date(self):
        if HAS_JDATETIME:
            today = jdatetime.date.today()
            return {
                "year": today.year,
                "month": today.month,
                "day": today.day,
                "month_name": today.strftime('%B'),
                "weekday": today.strftime('%A'),
                "formatted": today.strftime('%Y/%m/%d')
            }
        else:
            today = datetime.now()
            persian_year = today.year - 621
            persian_month = today.month + 2
            persian_day = today.day - 20
            if persian_day <= 0:
                persian_day += 30
                persian_month -= 1
            if persian_month > 12:
                persian_month -= 12
                persian_year += 1
            
            month_names = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", 
                          "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
            weekday_names = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه", "شنبه", "یکشنبه"]
            
            return {
                "year": persian_year,
                "month": persian_month,
                "day": persian_day,
                "month_name": month_names[persian_month - 1] if 0 < persian_month <= 12 else "",
                "weekday": weekday_names[today.weekday()],
                "formatted": f"{persian_year}/{persian_month:02d}/{persian_day:02d}"
            }
    
    def get_persian_calendar_month(self):
        today = datetime.now()
        persian_date = self.get_today_persian_date()
        
        days = []
        for day in range(1, 31):
            days.append({
                "day": day,
                "is_today": day == persian_date["day"],
                "is_weekend": (today + timedelta(days=day - persian_date["day"])).weekday() >= 4
            })
        
        return {
            "year": persian_date["year"],
            "month": persian_date["month"],
            "month_name": persian_date["month_name"],
            "days": days
        }
    
    def get_gregorian_calendar_month(self):
        today = datetime.now()
        year = today.year
        month = today.month
        
        first_day = datetime(year, month, 1)
        last_day = datetime(year, month + 1, 1) - timedelta(days=1) if month < 12 else datetime(year + 1, 1, 1) - timedelta(days=1)
        
        days = []
        for day in range(1, last_day.day + 1):
            date = datetime(year, month, day)
            days.append({
                "day": day,
                "is_today": day == today.day,
                "is_weekend": date.weekday() >= 5,
                "weekday": date.strftime('%a')
            })
        
        return {
            "year": year,
            "month": month,
            "month_name": today.strftime('%B'),
            "days": days
        }
    
    def get_impact_color(self, impact: str) -> str:
        colors = {"low": "#00ff88", "medium": "#ffff00", "high": "#ff8800", "extreme": "#ff0000"}
        return colors.get(impact, "#ffffff")
