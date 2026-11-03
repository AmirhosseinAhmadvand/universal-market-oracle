"""
Train LSTM Model (placeholder)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.data_fetcher import DataFetcher
from src.lstm_model import LSTMModel


def main():
    print("=" * 60)
    print("TRAINING LSTM MODEL")
    print("=" * 60)
    
    fetcher = DataFetcher(cache_dir="data", cache_hours=24)
    df = fetcher.fetch_historical_data("bitcoin", days=90)
    
    if df.empty:
        print("[ERROR] No data available")
        return
    
    print(f"[INFO] Loaded {len(df)} records")
    
    model = LSTMModel(lookback=60)
    print("[INFO] Model training complete (using moving average baseline)")
    print("[SUCCESS] Model ready for predictions")


if __name__ == "__main__":
    main()
