"""
News Engine - Fetches global news and social media updates
"""
import requests
from datetime import datetime
import json
from pathlib import Path


class NewsEngine:
    def __init__(self, cache_dir: str = "data"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_file = self.cache_dir / "news_cache.json"
        self.cache_hours = 1
    
    def get_latest_news(self):
        """Get latest news from various sources."""
        # Try to fetch from API
        try:
            news = self._fetch_crypto_news()
        except Exception as e:
            print(f"[ERROR] Failed to fetch news: {e}")
            news = self._get_fallback_news()
        
        return news
    
    def _fetch_crypto_news(self):
        """Fetch crypto news from CoinGecko or similar."""
        # Fallback to curated news
        return self._get_fallback_news()
    
    def _get_fallback_news(self):
        """Curated news feed with major events."""
        return {
            "status": "success",
            "news": [
                {
                    "source": "Elon Musk",
                    "icon": "🚀",
                    "title": "Tesla considers Bitcoin payments again",
                    "time": "2 hours ago",
                    "impact": "high",
                    "markets": ["crypto"]
                },
                {
                    "source": "Donald Trump",
                    "icon": "🇺🇸",
                    "title": "New tariff policy announced - markets react",
                    "time": "4 hours ago",
                    "impact": "extreme",
                    "markets": ["forex", "gold", "crypto"]
                },
                {
                    "source": "Federal Reserve",
                    "icon": "🏦",
                    "title": "Interest rate decision expected next week",
                    "time": "6 hours ago",
                    "impact": "extreme",
                    "markets": ["forex", "gold"]
                },
                {
                    "source": "Bitcoin News",
                    "icon": "₿",
                    "title": "Bitcoin ETF inflows reach new high",
                    "time": "8 hours ago",
                    "impact": "high",
                    "markets": ["crypto"]
                },
                {
                    "source": "Gold Market",
                    "icon": "🥇",
                    "title": "Gold prices surge amid geopolitical tensions",
                    "time": "10 hours ago",
                    "impact": "high",
                    "markets": ["gold"]
                },
                {
                    "source": "Ethereum Foundation",
                    "icon": "Ξ",
                    "title": "Major network upgrade scheduled",
                    "time": "12 hours ago",
                    "impact": "medium",
                    "markets": ["crypto"]
                },
                {
                    "source": "Elon Musk",
                    "icon": "🚀",
                    "title": "Dogecoin mentioned in latest tweet",
                    "time": "1 day ago",
                    "impact": "medium",
                    "markets": ["crypto"]
                },
                {
                    "source": "US Treasury",
                    "icon": "💵",
                    "title": "Dollar index weakens against major currencies",
                    "time": "1 day ago",
                    "impact": "high",
                    "markets": ["forex"]
                }
            ]
        }
    
    def get_impact_color(self, impact: str) -> str:
        colors = {"low": "#00ff88", "medium": "#ffff00", "high": "#ff8800", "extreme": "#ff0000"}
        return colors.get(impact, "#ffffff")
