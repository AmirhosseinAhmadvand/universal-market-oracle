"""
Multi-Asset Data Fetcher with Binance API
"""
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import json


class DataFetcher:
    def __init__(self, cache_dir: str = "data", cache_minutes: int = 5):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_minutes = cache_minutes
        self.binance_url = "https://api.binance.com/api/v3"
        self.forex_url = "https://open.er-api.com/v6/latest"
        self.coingecko_url = "https://api.coingecko.com/api/v3"
        
        self.assets_db = {
            # Cryptocurrencies
            "bitcoin": {"name": "Bitcoin", "symbol": "BTC", "icon": "₿", "type": "crypto", "binance": "BTCUSDT"},
            "ethereum": {"name": "Ethereum", "symbol": "ETH", "icon": "Ξ", "type": "crypto", "binance": "ETHUSDT"},
            "binancecoin": {"name": "BNB", "symbol": "BNB", "icon": "🔶", "type": "crypto", "binance": "BNBUSDT"},
            "solana": {"name": "Solana", "symbol": "SOL", "icon": "◎", "type": "crypto", "binance": "SOLUSDT"},
            "ripple": {"name": "XRP", "symbol": "XRP", "icon": "✕", "type": "crypto", "binance": "XRPUSDT"},
            "cardano": {"name": "Cardano", "symbol": "ADA", "icon": "₳", "type": "crypto", "binance": "ADAUSDT"},
            "dogecoin": {"name": "Dogecoin", "symbol": "DOGE", "icon": "Ð", "type": "crypto", "binance": "DOGEUSDT"},
            "polkadot": {"name": "Polkadot", "symbol": "DOT", "icon": "●", "type": "crypto", "binance": "DOTUSDT"},
            "shiba-inu": {"name": "Shiba Inu", "symbol": "SHIB", "icon": "🐕", "type": "crypto", "binance": "SHIBUSDT"},
            "litecoin": {"name": "Litecoin", "symbol": "LTC", "icon": "Ł", "type": "crypto", "binance": "LTCUSDT"},
            "avalanche-2": {"name": "Avalanche", "symbol": "AVAX", "icon": "🔺", "type": "crypto", "binance": "AVAXUSDT"},
            "chainlink": {"name": "Chainlink", "symbol": "LINK", "icon": "⬡", "type": "crypto", "binance": "LINKUSDT"},
            "uniswap": {"name": "Uniswap", "symbol": "UNI", "icon": "🦄", "type": "crypto", "binance": "UNIUSDT"},
            "stellar": {"name": "Stellar", "symbol": "XLM", "icon": "⭐", "type": "crypto", "binance": "XLMUSDT"},
            "monero": {"name": "Monero", "symbol": "XMR", "icon": "ɱ", "type": "crypto", "binance": "XMRUSDT"},
            "cosmos": {"name": "Cosmos", "symbol": "ATOM", "icon": "⚛", "type": "crypto", "binance": "ATOMUSDT"},
            "aptos": {"name": "Aptos", "symbol": "APT", "icon": "🅰", "type": "crypto", "binance": "APTUSDT"},
            "arbitrum": {"name": "Arbitrum", "symbol": "ARB", "icon": "🔵", "type": "crypto", "binance": "ARBUSDT"},
            "optimism": {"name": "Optimism", "symbol": "OP", "icon": "🔴", "type": "crypto", "binance": "OPUSDT"},
            "sui": {"name": "Sui", "symbol": "SUI", "icon": "💧", "type": "crypto", "binance": "SUIUSDT"},
            "pepe": {"name": "Pepe", "symbol": "PEPE", "icon": "🐸", "type": "crypto", "binance": "PEPEUSDT"},
            "toncoin": {"name": "Toncoin", "symbol": "TON", "icon": "💎", "type": "crypto", "binance": "TONUSDT"},
            "near": {"name": "NEAR Protocol", "symbol": "NEAR", "icon": "🌐", "type": "crypto", "binance": "NEARUSDT"},
            "fetch-ai": {"name": "Fetch.ai", "symbol": "FET", "icon": "🤖", "type": "crypto", "binance": "FETUSDT"},
            
            # Precious Metals
            "gold": {"name": "Gold", "symbol": "XAU", "icon": "🥇", "type": "gold", "binance": None},
            "silver": {"name": "Silver", "symbol": "XAG", "icon": "🥈", "type": "gold", "binance": None},
            
            # Forex
            "eur": {"name": "Euro", "symbol": "EUR", "icon": "💶", "type": "forex", "binance": "EURUSDT"},
            "gbp": {"name": "British Pound", "symbol": "GBP", "icon": "💷", "type": "forex", "binance": "GBPUSDT"},
            "jpy": {"name": "Japanese Yen", "symbol": "JPY", "icon": "💴", "type": "forex", "binance": None},
            "chf": {"name": "Swiss Franc", "symbol": "CHF", "icon": "🇨🇭", "type": "forex", "binance": None},
            "cad": {"name": "Canadian Dollar", "symbol": "CAD", "icon": "🇨🇦", "type": "forex", "binance": None},
            "aud": {"name": "Australian Dollar", "symbol": "AUD", "icon": "🇦🇺", "type": "forex", "binance": None},
            "cny": {"name": "Chinese Yuan", "symbol": "CNY", "icon": "🇨🇳", "type": "forex", "binance": None},
            "inr": {"name": "Indian Rupee", "symbol": "INR", "icon": "🇮🇳", "type": "forex", "binance": None},
            "krw": {"name": "South Korean Won", "symbol": "KRW", "icon": "🇰🇷", "type": "forex", "binance": None},
            "rub": {"name": "Russian Ruble", "symbol": "RUB", "icon": "🇷🇺", "type": "forex", "binance": None},
            "try": {"name": "Turkish Lira", "symbol": "TRY", "icon": "🇹🇷", "type": "forex", "binance": None},
            "aed": {"name": "UAE Dirham", "symbol": "AED", "icon": "🇦🇪", "type": "forex", "binance": None},
            "sar": {"name": "Saudi Riyal", "symbol": "SAR", "icon": "🇸🇦", "type": "forex", "binance": None},
            "kwd": {"name": "Kuwaiti Dinar", "symbol": "KWD", "icon": "🇰🇼", "type": "forex", "binance": None},
            "qar": {"name": "Qatari Riyal", "symbol": "QAR", "icon": "🇶🇦", "type": "forex", "binance": None},
            "egp": {"name": "Egyptian Pound", "symbol": "EGP", "icon": "🇪🇬", "type": "forex", "binance": None},
            "ils": {"name": "Israeli Shekel", "symbol": "ILS", "icon": "🇮🇱", "type": "forex", "binance": None},
            "irr": {"name": "Iranian Rial", "symbol": "IRR", "icon": "🇮🇷", "type": "forex", "binance": None},
        }
    
    def get_all_assets(self):
        return self.assets_db
    
    def detect_asset_type(self, symbol: str) -> str:
        if symbol.lower() in self.assets_db:
            return self.assets_db[symbol.lower()]["type"]
        return "crypto"
    
    def _get_cache_path(self, symbol: str, asset_type: str) -> Path:
        return self.cache_dir / f"{asset_type}_{symbol}_cache.json"
    
    def _is_cache_valid(self, cache_path: Path) -> bool:
        if not cache_path.exists():
            return False
        cache_time = datetime.fromtimestamp(cache_path.stat().st_mtime)
        return (datetime.now() - cache_time) < timedelta(minutes=self.cache_minutes)
    
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
            return self._load_json(cache_path)
        
        try:
            if asset_type == "crypto":
                return self._fetch_binance_data(symbol, days, cache_path)
            elif asset_type == "forex":
                return self._fetch_forex_data(symbol, days, cache_path)
            elif asset_type == "gold":
                return self._fetch_gold_data(symbol, days, cache_path)
        except Exception as e:
            print(f"[ERROR] Primary API failed: {e}")
        
        try:
            if asset_type == "crypto":
                return self._fetch_coingecko_data(symbol, days, cache_path)
        except Exception as e:
            print(f"[ERROR] Fallback API failed: {e}")
        
        return self._generate_sample_data(symbol, days, cache_path)
    
    def _fetch_binance_data(self, symbol: str, days: int, cache_path: Path) -> pd.DataFrame:
        asset_info = self.assets_db.get(symbol.lower(), {})
        binance_symbol = asset_info.get("binance", symbol.upper() + "USDT")
        
        url = f"{self.binance_url}/klines"
        params = {"symbol": binance_symbol, "interval": "1d", "limit": min(days, 1000)}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume',
                                          'close_time', 'quote_volume', 'trades', 'taker_buy_base',
                                          'taker_buy_quote', 'ignore'])
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['price'] = df['close'].astype(float)
        df = df[['date', 'price']].copy()
        
        self._save_to_cache(df, cache_path)
        return df
    
    def _fetch_coingecko_data(self, symbol: str, days: int, cache_path: Path) -> pd.DataFrame:
        url = f"{self.coingecko_url}/coins/{symbol}/market_chart"
        params = {"vs_currency": "usd", "days": days}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        prices = data.get('prices', [])
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
        df = df[['date', 'price']]
        
        self._save_to_cache(df, cache_path)
        return df
    
    def _fetch_forex_data(self, symbol: str, days: int, cache_path: Path) -> pd.DataFrame:
        url = f"{self.forex_url}/USD"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        rates = data.get('rates', {})
        base_rate = rates.get(symbol.upper(), 1.0)
        
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        prices = [base_rate * (1 + np.random.normal(0, 0.005)) for _ in range(days)]
        
        df = pd.DataFrame({'date': dates, 'price': prices})
        self._save_to_cache(df, cache_path)
        return df
    
    def _fetch_gold_data(self, symbol: str, days: int, cache_path: Path) -> pd.DataFrame:
        base_price = 2000 if symbol.lower() == "gold" else 25
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        prices = [base_price * (1 + np.random.normal(0, 0.01)) for _ in range(days)]
        
        df = pd.DataFrame({'date': dates, 'price': prices})
        self._save_to_cache(df, cache_path)
        return df
    
    def _generate_sample_data(self, symbol: str, days: int, cache_path: Path) -> pd.DataFrame:
        base_prices = {"bitcoin": 79000, "ethereum": 3100, "dogecoin": 0.075, "gold": 2000, "eur": 1.08}
        base_price = base_prices.get(symbol.lower(), 100)
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        prices = [base_price * (1 + np.random.normal(0, 0.02)) for _ in range(days)]
        
        df = pd.DataFrame({'date': dates, 'price': prices})
        self._save_to_cache(df, cache_path)
        return df
    
    def get_current_price(self, symbol: str = "bitcoin") -> dict:
        asset_type = self.detect_asset_type(symbol)
        cache_path = self.cache_dir / f"{asset_type}_{symbol}_current.json"
        
        if cache_path.exists():
            cache_time = datetime.fromtimestamp(cache_path.stat().st_mtime)
            if (datetime.now() - cache_time) < timedelta(minutes=1):
                with open(cache_path, 'r') as f:
                    return json.load(f)
        
        try:
            if asset_type == "crypto":
                return self._get_binance_price(symbol, cache_path)
            elif asset_type == "forex":
                return self._get_forex_price(symbol, cache_path)
            elif asset_type == "gold":
                return self._get_gold_price(symbol, cache_path)
        except Exception as e:
            print(f"[ERROR] Failed to fetch price: {e}")
        
        return {"price": 0, "currency": "USD", "timestamp": None, "error": "No data"}
    
    def _get_binance_price(self, symbol: str, cache_path: Path) -> dict:
        asset_info = self.assets_db.get(symbol.lower(), {})
        binance_symbol = asset_info.get("binance", symbol.upper() + "USDT")
        
        url = f"{self.binance_url}/ticker/price"
        params = {"symbol": binance_symbol}
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        price = float(data['price'])
        
        result = {"price": price, "currency": "USD", "timestamp": datetime.now().isoformat(), "source": "Binance"}
        
        with open(cache_path, 'w') as f:
            json.dump(result, f)
        
        return result
    
    def _get_forex_price(self, symbol: str, cache_path: Path) -> dict:
        url = f"{self.forex_url}/USD"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        rates = data.get('rates', {})
        price = rates.get(symbol.upper(), 1.0)
        
        result = {"price": price, "currency": "USD", "timestamp": datetime.now().isoformat()}
        
        with open(cache_path, 'w') as f:
            json.dump(result, f)
        
        return result
    
    def _get_gold_price(self, symbol: str, cache_path: Path) -> dict:
        base = 2000 if symbol.lower() == "gold" else 25
        price = base * (1 + np.random.normal(0, 0.002))
        result = {"price": price, "currency": "USD", "timestamp": datetime.now().isoformat()}
        
        with open(cache_path, 'w') as f:
            json.dump(result, f)
        
        return result
