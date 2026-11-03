"""
LSTM Model for Cryptocurrency Price Prediction
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from pathlib import Path


class LSTMModel:
    def __init__(self, lookback: int = 60):
        self.lookback = lookback
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.model = None
        self.model_path = Path("models/lstm_model.h5")
        self.model_path.parent.mkdir(exist_ok=True)
    
    def is_trained(self) -> bool:
        """Check if model is trained and saved."""
        return self.model_path.exists()
    
    def predict_next(self, df: pd.DataFrame, days: int = 7) -> list:
        """Predict using moving average (LSTM placeholder)."""
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
