"""
Global Events Calendar Engine
Shows important events that affect markets
"""
from datetime import datetime, timedelta
import json
from pathlib import Path


class CalendarEngine:
    def __init__(self):
        self.events_file = Path("data/events.json")
        self.events = self._load_events()
    
    def _load_events(self):
        """Load events from JSON file."""
        if self.events_file.exists():
            with open(self.events_file, 'r') as f:
                return json.load(f)
        return self._default_events()
    
    def _default_events(self):
        """Default important events."""
        return {
            "fixed_events": [
                {
                    "date": "2026-12-25",
                    "name": "Christmas Day",
                    "name_fa": "کریسمس",
                    "icon": "🎄",
                    "impact": "high",
                    "markets": ["forex", "crypto", "gold"],
                    "description": "Markets closed in US and Europe"
                },
                {
                    "date": "2026-10-31",
                    "name": "Halloween",
                    "name_fa": "هالوین",
                    "icon": "🎃",
                    "impact": "low",
                    "markets": [],
                    "description": "Cultural event, minimal market impact"
                },
                {
                    "date": "2027-03-21",
                    "name": "Nowruz (Persian New Year)",
                    "name_fa": "عید نوروز",
                    "icon": "🌸",
                    "impact": "medium",
                    "markets": ["gold"],
                    "description": "Iranian New Year - gold demand increases"
                },
                {
                    "date": "2026-11-26",
                    "name": "US Thanksgiving",
                    "name_fa": "روز شکرگزاری آمریکا",
                    "icon": "🦃",
                    "impact": "high",
                    "markets": ["forex", "stocks"],
                    "description": "US markets closed, low liquidity"
                },
                {
                    "date": "2027-01-01",
                    "name": "New Year",
                    "name_fa": "سال نو میلادی",
                    "icon": "🎆",
                    "impact": "high",
                    "markets": ["all"],
                    "description": "Global markets closed"
                },
                {
                    "date": "2026-11-05",
                    "name": "US Elections Day",
                    "name_fa": "انتخابات آمریکا",
                    "icon": "🗳️",
                    "impact": "extreme",
                    "markets": ["forex", "crypto", "gold"],
                    "description": "Major market volatility expected"
                },
                {
                    "date": "2026-12-14",
                    "name": "FOMC Meeting",
                    "name_fa": "جلسه فدرال رزرو",
                    "icon": "🏦",
                    "impact": "extreme",
                    "markets": ["forex", "gold", "crypto"],
                    "description": "Interest rate decision - huge market impact"
                },
                {
                    "date": "2027-02-14",
                    "name": "Valentine's Day",
                    "name_fa": "ولنتاین",
                    "icon": "❤️",
                    "impact": "low",
                    "markets": ["gold"],
                    "description": "Slight increase in gold/jewelry demand"
                },
                {
                    "date": "2027-03-17",
                    "name": "St. Patrick's Day",
                    "name_fa": "سنت پاتریک",
                    "icon": "☘️",
                    "impact": "low",
                    "markets": [],
                    "description": "Cultural event"
                },
                {
                    "date": "2026-11-27",
                    "name": "Black Friday",
                    "name_fa": "بلک فرایدی",
                    "icon": "🛍️",
                    "impact": "medium",
                    "markets": ["stocks"],
                    "description": "Retail stocks surge"
                }
            ],
            "recurring_events": [
                {
                    "day_of_month": 1,
                    "name": "Month Start",
                    "name_fa": "اول ماه",
                    "icon": "📅",
                    "impact": "medium",
                    "markets": ["all"],
                    "description": "Monthly rebalancing by institutions"
                },
                {
                    "day_of_week": 5,
                    "name": "Friday Close",
                    "name_fa": "بازار جمعه",
                    "icon": "📊",
                    "impact": "medium",
                    "markets": ["forex"],
                    "description": "Weekly position closing"
                }
            ]
        }
    
    def get_upcoming_events(self, days_ahead: int = 30):
        """Get events coming in the next X days."""
        today = datetime.now().date()
        end_date = today + timedelta(days=days_ahead)
        
        upcoming = []
        
        for event in self.events.get("fixed_events", []):
            event_date = datetime.strptime(event["date"], "%Y-%m-%d").date()
            if today <= event_date <= end_date:
                days_until = (event_date - today).days
                upcoming.append({
                    **event,
                    "days_until": days_until,
                    "type": "fixed"
                })
        
        # Sort by days until
        upcoming.sort(key=lambda x: x["days_until"])
        
        return upcoming
    
   
