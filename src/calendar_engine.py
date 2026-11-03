"""
Global Events Calendar Engine
"""
from datetime import datetime, timedelta
import json
from pathlib import Path


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
            "fixed_events": [
                {"date": "2026-12-25", "name": "Christmas", "name_fa": "کریسمس", "icon": "🎄", "impact": "high", "markets": ["forex", "crypto", "gold"], "description": "Markets closed"},
                {"date": "2026-10-31", "name": "Halloween", "name_fa": "هالوین", "icon": "🎃", "impact": "low", "markets": [], "description": "Cultural event"},
                {"date": "2027-03-21", "name": "Nowruz", "name_fa": "نوروز", "icon": "🌸", "impact": "medium", "markets": ["gold"], "description": "Iranian New Year"},
                {"date": "2026-11-26", "name": "US Thanksgiving", "name_fa": "شکرگزاری", "icon": "🦃", "impact": "high", "markets": ["forex"], "description": "US markets closed"},
                {"date": "2027-01-01", "name": "New Year", "name_fa": "سال نو", "icon": "🎆", "impact": "high", "markets": ["all"], "description": "Global markets closed"},
                {"date": "2026-11-05", "name": "US Elections", "name_fa": "انتخابات", "icon": "🗳️", "impact": "extreme", "markets": ["forex", "crypto", "gold"], "description": "Major volatility"},
                {"date": "2026-12-14", "name": "FOMC Meeting", "name_fa": "فدرال رزرو", "icon": "🏦", "impact": "extreme", "markets": ["forex", "gold", "crypto"], "description": "Interest rate decision"}
            ],
            "recurring_events": []
        }
    
    def get_upcoming_events(self, days_ahead: int = 30):
        today = datetime.now().date()
        end_date = today + timedelta(days=days_ahead)
        upcoming = []
        
        for event in self.events.get("fixed_events", []):
            event_date = datetime.strptime(event["date"], "%Y-%m-%d").date()
            if today <= event_date <= end_date:
                days_until = (event_date - today).days
                upcoming.append({**event, "days_until": days_until, "type": "fixed"})
        
        upcoming.sort(key=lambda x: x["days_until"])
        return upcoming
    
    def get_today_events(self):
        today = datetime.now().date()
        today_str = today.strftime("%Y-%m-%d")
        events = []
        
        for event in self.events.get("fixed_events", []):
            if event["date"] == today_str:
                events.append({**event, "type": "fixed"})
        
        return events
    
    def get_impact_color(self, impact: str) -> str:
        colors = {"low": "#00ff88", "medium": "#ffff00", "high": "#ff8800", "extreme": "#ff0000"}
        return colors.get(impact, "#ffffff")
