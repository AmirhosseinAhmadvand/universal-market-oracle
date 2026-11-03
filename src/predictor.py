"""
Predictor with LSTM Support
"""
import numpy as np
import pandas as pd
from pathlib import Path
from src.lstm_model import LSTMModel


class CryptoPredictor:
    def __init__(self, lookback: int = 60):
        self.lookback = lookback
        self.lstm_model = LSTMModel(lookback=lookback)
    
    def predict_next(self, df: pd.DataFrame, days: int = 7) -> list:
        """Predict future prices using LSTM if available, else fallback to MA."""
        # Try LSTM first
        if self.lstm_model.is_trained():
            try:
                print("[INFO] Using LSTM model for prediction")
                predictions = self.lstm_model.predict_next(df, days)
                if predictions:
                    return predictions
            except Exception as e:
                print(f"[WARNING] LSTM prediction failed: {e}")
        
        # Fallback to moving average
        print("[INFO] Using moving average for prediction (LSTM not available)")
        return self._moving_average_predict(df, days)
    
    def _moving_average_predict(self, df: pd.DataFrame, days: int) -> list:
        """Simple moving average prediction (fallback)."""
        prices = df['price'].values
        predictions = []
        
        for i in range(days):
            if len(prices) >= 7:
                next_price = np.mean(prices[-7:]) * (1 + np.random.normal(0, 0.01))
            else:
                next_price = prices[-1] * (1 + np.random.normal(0, 0.02))
            
            predictions.append(next_price)
            prices = np.append(prices, next_price)
        
        return predictions
