"""
Train LSTM Model on Historical Data
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.data_fetcher import DataFetcher
from src.lstm_model import LSTMModel


def main():
    print("=" * 60)
    print("TRAINING LSTM MODEL")
    print("=" * 60)
    
    # Fetch historical data (90 days for better training)
    fetcher = DataFetcher(cache_dir="data", cache_hours=24)
    df = fetcher.fetch_historical_data("bitcoin", days=90)
    
    if df.empty:
        print("[ERROR] No data available for training")
        return
    
    print(f"[INFO] Loaded {len(df)} records for training")
    
    # Create and train model
    model = LSTMModel(lookback=60, epochs=50, batch_size=32)
    metrics = model.train(df)
    
    print("\n" + "=" * 60)
    print("TRAINING COMPLETE")
    print("=" * 60)
    print(f"Train Loss: {metrics['train_loss']:.6f}")
    print(f"Validation Loss: {metrics['val_loss']:.6f}")
    print(f"Epochs: {metrics['epochs']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
