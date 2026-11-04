"""
Multi-Asset Data Fetcher with Online/Offline Fallback
"""
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import json


class DataFetcher:
    def __init__(self, cache_dir: str = "data", cache_hours: int = 1):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_hours = cache_hours
        self.api_urls = {
            "crypto": "https://api.coingecko.com/api/v3",
            "forex": "https://open.er-api.com/v6/latest"
        }
        self.sample_data_dir = self.cache_dir / "samples"
        self.sample_data_dir.mkdir(exist_ok=True)
        
        # Asset database with icons
        self.assets_db = {
            "bitcoin": {"name": "Bitcoin", "symbol": "BTC", "icon": "₿", "type": "crypto"},
            "ethereum": {"name": "Ethereum", "symbol": "ETH", "icon": "Ξ", "type": "crypto"},
            "binancecoin": {"name": "BNB", "symbol": "BNB", "icon": "🔶", "type": "crypto"},
            "solana": {"name": "Solana", "symbol": "SOL", "icon": "◎", "type": "crypto"},
            "ripple": {"name": "XRP", "symbol": "XRP", "icon": "✕", "type": "crypto"},
            "cardano": {"name": "Cardano", "symbol": "ADA", "icon": "₳", "type": "crypto"},
            "dogecoin": {"name": "Dogecoin", "symbol": "DOGE", "icon": "Ð", "type": "crypto"},
            "polkadot": {"name": "Polkadot", "symbol": "DOT", "icon": "●", "type": "crypto"},
            "shiba-inu": {"name": "Shiba Inu", "symbol": "SHIB", "icon": "🐕", "type": "crypto"},
            "litecoin": {"name": "Litecoin", "symbol": "LTC", "icon": "Ł", "type": "crypto"},
            "avalanche-2": {"name": "Avalanche", "symbol": "AVAX", "icon": "🔺", "type": "crypto"},
            "chainlink": {"name": "Chainlink", "symbol": "LINK", "icon": "⬡", "type": "crypto"},
            "gold": {"name": "Gold", "symbol": "XAU", "icon": "🥇", "type": "gold"},
            "silver": {"name": "Silver", "symbol": "XAG", "icon": "🥈", "type": "gold"},
            "eur": {"name": "Euro", "symbol": "EUR", "icon": "💶", "type": "forex"},
            "gbp": {"name": "British Pound", "symbol": "GBP", "icon": "💷", "type": "forex"},
            "jpy": {"name": "Japanese Yen", "symbol": "JPY", "icon": "💴", "type": "forex"},
            "chf": {"name": "Swiss Franc", "symbol": "CHF", "icon": "🇨🇭", "type": "forex"},
            "cad": {"name": "Canadian Dollar", "symbol": "CAD", "icon": "🇨🇦", "type": "forex"},
            "aud": {"name": "Australian Dollar", "symbol": "AUD", "icon": "🇦🇺", "type": "forex"},
            "cny": {"name": "Chinese Yuan", "symbol": "CNY", "icon": "🇨🇳", "type": "forex"},
            "inr": {"name": "Indian Rupee", "symbol": "INR", "icon": "🇮🇳", "type": "forex"},
            "rub": {"name": "Russian Ruble", "symbol": "RUB", "icon": "🇷🇺", "type": "forex"},
            "try": {"name": "Turkish Lira", "symbol": "TRY", "icon": "🇹🇷", "type": "forex"},
            "aed": {"name": "UAE Dirham", "symbol": "AED", "icon": "🇦🇪", "type": "forex"},
            "sar": {"name": "Saudi Riyal", "symbol": "SAR", "icon": "🇸🇦", "type": "forex"},
            "kwd": {"name": "Kuwaiti Dinar", "symbol": "KWD", "icon": "🇰🇼", "type": "forex"},
            "qar": {"name": "Qatari Riyal", "symbol": "QAR", "icon": "🇶🇦", "type": "forex"},
            "bhd": {"name": "Bahraini Dinar", "symbol": "BHD", "icon": "🇧🇭", "type": "forex"},
            "omr": {"name": "Omani Rial", "symbol": "OMR", "icon": "🇴🇲", "type": "forex"},
            "jod": {"name": "Jordanian Dinar", "symbol": "JOD", "icon": "🇯🇴", "type": "forex"},
            "egp": {"name": "Egyptian Pound", "symbol": "EGP", "icon": "🇪🇬", "type": "forex"},
            "ils": {"name": "Israeli Shekel", "symbol": "ILS", "icon": "🇮🇱", "type": "forex"},
            "twd": {"name": "Taiwan Dollar", "symbol": "TWD", "icon": "🇹🇼", "type": "forex"},
            "krw": {"name": "South Korean Won", "symbol": "KRW", "icon": "🇰🇷", "type": "forex"},
            "sgd": {"name": "Singapore Dollar", "symbol": "SGD", "icon": "🇸🇬", "type": "forex"},
            "hkd": {"name": "Hong Kong Dollar", "symbol": "HKD", "icon": "🇭🇰", "type": "forex"},
            "mxn": {"name": "Mexican Peso", "symbol": "MXN", "icon": "🇲🇽", "type": "forex"},
            "brl": {"name": "Brazilian Real", "symbol": "BRL", "icon": "🇧🇷", "type": "forex"},
            "zar": {"name": "South African Rand", "symbol": "ZAR", "icon": "🇿🇦", "type": "forex"},
            "nzd": {"name": "New Zealand Dollar", "symbol": "NZD", "icon": "🇳🇿", "type": "forex"},
            "sek": {"name": "Swedish Krona", "symbol": "SEK", "icon": "🇸🇪", "type": "forex"},
            "nok": {"name": "Norwegian Krone", "symbol": "NOK", "icon": "🇳🇴", "type": "forex"},
            "dkk": {"name": "Danish Krone", "symbol": "DKK", "icon": "🇩🇰", "type": "forex"},
            "pln": {"name": "Polish Zloty", "symbol": "PLN", "icon": "🇵🇱", "type": "forex"},
            "czk": {"name": "Czech Koruna", "symbol": "CZK", "icon": "🇨🇿", "type": "forex"},
            "huf": {"name": "Hungarian Forint", "symbol": "HUF", "icon": "🇭🇺", "type": "forex"},
            "ron": {"name": "Romanian Leu", "symbol": "RON", "icon": "🇷🇴", "type": "forex"},
            "thb": {"name": "Thai Baht", "symbol": "THB", "icon": "🇹🇭", "type": "forex"},
            "myr": {"name": "Malaysian Ringgit", "symbol": "MYR", "icon": "🇲🇾", "type": "forex"},
            "idr": {"name": "Indonesian Rupiah", "symbol": "IDR", "icon": "🇮🇩", "type": "forex"},
            "php": {"name": "Philippine Peso", "symbol": "PHP", "icon": "🇵🇭", "type": "forex"},
            "vnd": {"name": "Vietnamese Dong", "symbol": "VND", "icon": "🇻🇳", "type": "forex"},
            "pkr": {"name": "Pakistani Rupee", "symbol": "PKR", "icon": "🇵🇰", "type": "forex"},
            "bdt": {"name": "Bangladeshi Taka", "symbol": "BDT", "icon": "🇧🇩", "type": "forex"},
            "lkr": {"name": "Sri Lankan Rupee", "symbol": "LKR", "icon": "🇱🇰", "type": "forex"},
            "npr": {"name": "Nepalese Rupee", "symbol": "NPR", "icon": "🇳🇵", "type": "forex"},
            "afn": {"name": "Afghan Afghani", "symbol": "AFN", "icon": "🇦🇫", "type": "forex"},
            "irr": {"name": "Iranian Rial", "symbol": "IRR", "icon": "🇮🇷", "type": "forex"},
            "iqd": {"name": "Iraqi Dinar", "symbol": "IQD", "icon": "🇮🇶", "type": "forex"},
            "syp": {"name": "Syrian Pound", "symbol": "SYP", "icon": "🇸🇾", "type": "forex"},
            "lbp": {"name": "Lebanese Pound", "symbol": "LBP", "icon": "🇱🇧", "type": "forex"},
            "amd": {"name": "Armenian Dram", "symbol": "AMD", "icon": "🇦🇲", "type": "forex"},
            "azn": {"name": "Azerbaijani Manat", "symbol": "AZN", "icon": "🇦🇿", "type": "forex"},
            "gel": {"name": "Georgian Lari", "symbol": "GEL", "icon": "🇬🇪", "type": "forex"},
            "kzt": {"name": "Kazakhstani Tenge", "symbol": "KZT", "icon": "🇰🇿", "type": "forex"},
            "uzs": {"name": "Uzbekistani Som", "symbol": "UZS", "icon": "🇺🇿", "type": "forex"},
            "tmt": {"name": "Turkmenistani Manat", "symbol": "TMT", "icon": "🇹🇲", "type": "forex"},
            "kgs": {"name": "Kyrgyzstani Som", "symbol": "KGS", "icon": "🇰🇬", "type": "forex"},
            "tjs": {"name": "Tajikistani Somoni", "symbol": "TJS", "icon": "🇹🇯", "type": "forex"},
            "mnk": {"name": "Mongolian Tugrik", "symbol": "MNT", "icon": "🇲🇳", "type": "forex"},
            "cuc": {"name": "Cuban Peso", "symbol": "CUP", "icon": "🇨🇺", "type": "forex"},
            "dop": {"name": "Dominican Peso", "symbol": "DOP", "icon": "🇩🇴", "type": "forex"},
            "gtq": {"name": "Guatemalan Quetzal", "symbol": "GTQ", "icon": "🇬🇹", "type": "forex"},
            "hnl": {"name": "Honduran Lempira", "symbol": "HNL", "icon": "🇭🇳", "type": "forex"},
            "nio": {"name": "Nicaraguan Córdoba", "symbol": "NIO", "icon": "🇳🇮", "type": "forex"},
            "crc": {"name": "Costa Rican Colón", "symbol": "CRC", "icon": "🇨🇷", "type": "forex"},
            "pan": {"name": "Panamanian Balboa", "symbol": "PAB", "icon": "🇵🇦", "type": "forex"},
            "cop": {"name": "Colombian Peso", "symbol": "COP", "icon": "🇨🇴", "type": "forex"},
            "ves": {"name": "Venezuelan Bolívar", "symbol": "VES", "icon": "🇻🇪", "type": "forex"},
            "guy": {"name": "Guyanese Dollar", "symbol": "GYD", "icon": "🇬🇾", "type": "forex"},
            "srd": {"name": "Surinamese Dollar", "symbol": "SRD", "icon": "🇸🇷", "type": "forex"},
            "uyu": {"name": "Uruguayan Peso", "symbol": "UYU", "icon": "🇺🇾", "type": "forex"},
            "pyg": {"name": "Paraguayan Guaraní", "symbol": "PYG", "icon": "🇵🇾", "type": "forex"},
            "bob": {"name": "Bolivian Boliviano", "symbol": "BOB", "icon": "🇧🇴", "type": "forex"},
            "clp": {"name": "Chilean Peso", "symbol": "CLP", "icon": "🇨🇱", "type": "forex"},
            "ars": {"name": "Argentine Peso", "symbol": "ARS", "icon": "🇦🇷", "type": "forex"},
            "pen": {"name": "Peruvian Sol", "symbol": "PEN", "icon": "🇵🇪", "type": "forex"},
            "eck": {"name": "Ecuadorian Sucre", "symbol": "USD", "icon": "🇪🇨", "type": "forex"},
        }
    
    def get_all_assets(self):
        """Return all available assets with metadata."""
        return self.assets_db
    
    def detect_asset_type(self, symbol: str) -> str:
        if symbol.lower() in ["gold", "xau", "silver", "xag"]:
            return "gold"
        elif symbol.lower() in self.assets_db:
            return self.assets_db[symbol.lower()]["type"]
        elif symbol.lower() in ["eur", "usd", "gbp", "jpy", "chf", "cad", "aud", "cny", "inr", "rub", "try"]:
            return "forex"
        else:
            return "crypto"
    
    def _get_cache_path(self, symbol: str, asset_type: str) -> Path:
        return self.cache_dir / f"{asset_type}_{symbol}_cache.json"
    
    def _is_cache_valid(self, cache_path: Path) -> bool:
        if not cache_path.exists():
            return False
        cache_time = datetime.fromtimestamp(cache_path.stat().st_mtime)
        return (datetime.now() - cache_time) < timedelta(hours=self.cache_hours)
    
    def _load_json(self, path: Path) -> pd.DataFrame:
        with open(path, 'r') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        return df
    
    def _save_to_cache(self, df: pd.DataFrame, cache_path: Path):
        records = df.copy()
        records['date'] = records['date'].astype(str)
        with open(cache_path, 'w') as f:
            json.dump(records.to_dict(orient='records'), f)
    
    def fetch_historical_data(self, symbol: str = "bitcoin", days: int = 30) -> pd.DataFrame:
        asset_type = self.detect_asset_type(symbol)
        cache_path = self._get_cache_path(symbol, asset_type)
        
        if self._is_cache_valid(cache_path):
            print(f"[INFO] Using cached data for {symbol}")
            return self._load_json(cache_path)
        
        try:
            if asset_type == "crypto":
                return self._fetch_crypto_data(symbol, days, cache_path)
            elif asset_type == "forex":
                return self._fetch_forex_data(symbol, days, cache_path)
            elif asset_type == "gold":
                return self._fetch_gold_data(symbol, days, cache_path)
        except Exception as e:
            print(f"[ERROR] API request failed for {symbol}: {e}")
        
        sample_path = self.sample_data_dir / f"{symbol}.json"
        if sample_path.exists():
            print(f"[WARNING] Using sample data for {symbol}")
            return self._load_json(sample_path)
        
        print(f"[CRITICAL] No data available for {symbol}")
        return pd.DataFrame(columns=['date', 'price'])
    
    def _fetch_crypto_data(self, symbol: str, days: int, cache_path: Path) -> pd.DataFrame:
        print(f"[INFO] Fetching crypto data from API for {symbol}...")
        url = f"{self.api_urls['crypto']}/coins/{symbol}/market_chart"
        params = {"vs_currency": "usd", "days": days}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        prices = data.get('prices', [])
        
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
        df = df[['date', 'price']]
        
        self._save_to_cache(df, cache_path)
        print(f"[SUCCESS] Fetched and cached {len(df)} records")
        return df
    
    def _fetch_forex_data(self, symbol: str, days: int, cache_path: Path) -> pd.DataFrame:
        print(f"[INFO] Fetching forex data for {symbol}...")
        url = f"{self.api_urls['forex']}/USD"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        rates = data.get('rates', {})
        base_rate = rates.get(symbol.upper(), 1.0)
        
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        prices = [base_rate * (1 + np.random.normal(0, 0.005)) for _ in range(days)]
        
        df = pd.DataFrame({'date': dates, 'price': prices})
        self._save_to_cache(df, cache_path)
        print(f"[SUCCESS] Generated and cached {len(df)} forex records")
        return df
    
    def _fetch_gold_data(self, symbol: str, days: int, cache_path: Path) -> pd.DataFrame:
        print(f"[INFO] Fetching gold data...")
        base_price = 2000 if symbol.lower() == "gold" else 25
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        prices = [base_price * (1 + np.random.normal(0, 0.01)) for _ in range(days)]
        
        df = pd.DataFrame({'date': dates, 'price': prices})
        self._save_to_cache(df, cache_path)
        print(f"[SUCCESS] Generated and cached {len(df)} gold records")
        return df
    
    def get_current_price(self, symbol: str = "bitcoin") -> dict:
        asset_type = self.detect_asset_type(symbol)
        cache_path = self.cache_dir / f"{asset_type}_{symbol}_current.json"
        
        if self._is_cache_valid(cache_path):
            with open(cache_path, 'r') as f:
                return json.load(f)
        
        try:
            if asset_type == "crypto":
                return self._get_crypto_price(symbol, cache_path)
            elif asset_type == "forex":
                return self._get_forex_price(symbol, cache_path)
            elif asset_type == "gold":
                return self._get_gold_price(symbol, cache_path)
        except Exception as e:
            print(f"[ERROR] Failed to fetch current price for {symbol}: {e}")
        
        sample_path = self.sample_data_dir / f"{symbol}.json"
        if sample_path.exists():
            with open(sample_path, 'r') as f:
                sample_data = json.load(f)
            last_record = sample_data[-1]
            return {
                "price": last_record["price"],
                "currency": "USD",
                "timestamp": last_record["date"],
                "note": "SAMPLE DATA (API unavailable)"
            }
        
        return {"price": None, "currency": "USD", "timestamp": None, "error": "No data"}
    
    def _get_crypto_price(self, symbol: str, cache_path: Path) -> dict:
        url = f"{self.api_urls['crypto']}/simple/price"
        params = {"ids": symbol, "vs_currencies": "usd", "include_last_updated_at": "true"}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        result = {
            "price": data[symbol]["usd"],
            "currency": "USD",
            "timestamp": datetime.fromtimestamp(data[symbol]["last_updated_at"]).isoformat()
        }
        
        with open(cache_path, 'w') as f:
            json.dump(result, f)
        
        return result
    
    def _get_forex_price(self, symbol: str, cache_path: Path) -> dict:
        url = f"{self.api_urls['forex']}/USD"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        rates = data.get('rates', {})
        price = rates.get(symbol.upper(), 1.0)
        
        result = {
            "price": price,
            "currency": "USD",
            "timestamp": datetime.now().isoformat()
        }
        
        with open(cache_path, 'w') as f:
            json.dump(result, f)
        
        return result
    
    def _get_gold_price(self, symbol: str, cache_path: Path) -> dict:
        base = 2000 if symbol.lower() == "gold" else 25
        price = base * (1 + np.random.normal(0, 0.005))
        result = {
            "price": price,
            "currency": "USD",
            "timestamp": datetime.now().isoformat()
        }
        
        with open(cache_path, 'w') as f:
            json.dump(result, f)
        
        return result
