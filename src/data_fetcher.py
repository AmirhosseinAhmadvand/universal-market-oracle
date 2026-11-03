"""
Data Fetcher with Online/Offline Fallback - Multi Asset Support
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
            "forex": "https://open.er-api.com/v6/latest",
            "gold": "https://api.metalpriceapi.com/v1"
        }
        self.sample_data_dir = self.cache_dir / "samples"
        self.sample_data_dir.mkdir(exist_ok=True)
    
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
    
    def detect_asset_type(self, symbol: str) -> str:
        """Detect asset type from symbol."""
        crypto_symbols = ["bitcoin", "ethereum", "binancecoin", "solana", "ripple", "cardano", "dogecoin", "polkadot", "shiba-inu", "litecoin"]
        forex_symbols = ["eur", "usd", "gbp", "jpy", "chf", "cad", "aud"]
        
        if symbol.lower() in crypto_symbols:
            return "crypto"
        elif symbol.lower() in forex_symbols:
            return "forex"
        elif symbol.lower() in ["gold", "xau"]:
            return "gold"
        else:
            return "crypto"  # Default
    
    def fetch_historical_data(self, symbol: str = "bitcoin", days: int = 30) -> pd.DataFrame:
        asset_type = self.detect_asset_type(symbol)
        cache_path = self._get_cache_path(symbol, asset_type)
        
        # Try cache first
        if self._is_cache_valid(cache_path):
            print(f"[INFO] Using cached data for {symbol}")
            return self._load_json(cache_path)
        
        # Try API based on asset type
        try:
            if asset_type == "crypto":
                return self._fetch_crypto_data(symbol, days, cache_path)
            elif asset_type == "forex":
                return self._fetch_forex_data(symbol, days, cache_path)
            elif asset_type == "gold":
                return self._fetch_gold_data(symbol, days, cache_path)
        except Exception as e:
            print(f"[ERROR] API request failed for {symbol}: {e}")
        
        # Fallback to sample data
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
        # For forex, we'll use a simple conversion rate API
        url = f"{self.api_urls['forex']}/USD"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        rates = data.get('rates', {})
        
        # Generate historical data based on current rate
        base_rate = rates.get(symbol.upper(), 1.0)
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        prices = [base_rate * (1 + np.random.normal(0, 0.005)) for _ in range(days)]
        
        df = pd.DataFrame({'date': dates, 'price': prices})
        self._save_to_cache(df, cache_path)
        print(f"[SUCCESS] Generated and cached {len(df)} forex records")
        return df
    
    def _fetch_gold_data(self, symbol: str, days: int, cache_path: Path) -> pd.DataFrame:
        print(f"[INFO] Fetching gold data...")
        # Gold price simulation (around $2000 per ounce)
        base_price = 2000
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        prices = [base_price * (1 + np.random.normal(0, 0.01)) for _ in range(days)]
        
        df = pd.DataFrame({'date': dates, 'price': prices})
        self._save_to_cache(df, cache_path)
        print(f"[SUCCESS] Generated and cached {len(df)} gold records")
        return df
    
    def get_current_price(self, symbol: str = "bitcoin") -> dict:
        asset_type = self.detect_asset_type(symbol)
        cache_path = self.cache_dir / f"{asset_type}_{symbol}_current.json"
        
        # Try cache first (5 minutes)
        if self._is_cache_valid(cache_path):
            with open(cache_path, 'r') as f:
                return json.load(f)
        
        # Try API
        try:
            if asset_type == "crypto":
                return self._get_crypto_price(symbol, cache_path)
            elif asset_type == "forex":
                return self._get_forex_price(symbol, cache_path)
            elif asset_type == "gold":
                return self._get_gold_price(cache_path)
        except Exception as e:
            print(f"[ERROR] Failed to fetch current price for {symbol}: {e}")
        
        # Fallback
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
    
    def _get_gold_price(self, cache_path: Path) -> dict:
        # Simulated gold price
        price = 2000 * (1 + np.random.normal(0, 0.005))
        result = {
            "price": price,
            "currency": "USD",
            "timestamp": datetime.now().isoformat()
        }
        
        with open(cache_path, 'w') as f:
            json.dump(result, f)
        
        return result
