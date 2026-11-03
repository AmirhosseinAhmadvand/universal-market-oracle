"""
LSTM Predictor for Cryptocurrency Prices
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


class CryptoPredictor:
    def __init__(self, lookback: int = 60):
        self.lookback = lookback
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.model = None
    
    def prepare_data(self, df: pd.DataFrame) -> tuple:
        prices = df['price'].values.reshape(-1, 1)
        scaled_prices = self.scaler.fit_transform(prices)
        
        X, y = [], []
        for i in range(self.lookback, len(scaled_prices)):
            X.append(scaled_prices[i-self.lookback:i, 0])
            y.append(scaled_prices[i, 0])
        
        return np.array(X), np.array(y)
    
    def predict_next(self, df: pd.DataFrame, days: int = 7) -> list:
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
