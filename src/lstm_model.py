"""
LSTM Model for Cryptocurrency Price Prediction
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
from pathlib import Path


class LSTMModel:
    def __init__(self, lookback: int = 60, epochs: int = 50, batch_size: int = 32):
        self.lookback = lookback
        self.epochs = epochs
        self.batch_size = batch_size
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.model = None
        self.model_path = Path("models/lstm_model.h5")
        self.model_path.parent.mkdir(exist_ok=True)
    
    def create_model(self, input_shape: tuple) -> Sequential:
        """Create LSTM model architecture."""
        model = Sequential()
        
        # First LSTM layer with Dropout
        model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
        model.add(Dropout(0.2))
        
        # Second LSTM layer
        model.add(LSTM(units=50, return_sequences=False))
        model.add(Dropout(0.2))
        
        # Dense layer
        model.add(Dense(units=25))
        
        # Output layer
        model.add(Dense(units=1))
        
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model
    
    def prepare_data(self, df: pd.DataFrame) -> tuple:
        """Prepare data for LSTM training."""
        prices = df['price'].values.reshape(-1, 1)
        scaled_prices = self.scaler.fit_transform(prices)
        
        X, y = [], []
        for i in range(self.lookback, len(scaled_prices)):
            X.append(scaled_prices[i-self.lookback:i, 0])
            y.append(scaled_prices[i, 0])
        
        X, y = np.array(X), np.array(y)
        X = np.reshape(X, (X.shape[0], X.shape[1], 1))
        
        return X, y
    
    def train(self, df: pd.DataFrame) -> dict:
        """Train LSTM model on historical data."""
        print(f"[INFO] Training LSTM model on {len(df)} records...")
        
        X, y = self.prepare_data(df)
        
        # Split into train and test
        train_size = int(len(X) * 0.8)
        X_train, X_test = X[:train_size], X[train_size:]
        y_train, y_test = y[:train_size], y[train_size:]
        
        # Create model
        self.model = self.create_model((X_train.shape[1], 1))
        
        # Train
        history = self.model.fit(
            X_train, y_train,
            epochs=self.epochs,
            batch_size=self.batch_size,
            validation_data=(X_test, y_test),
            verbose=1
        )
        
        # Save model
        self.model.save(self.model_path)
        print(f"[SUCCESS] Model saved to {self.model_path}")
        
        # Calculate metrics
        train_loss = history.history['loss'][-1]
        val_loss = history.history['val_loss'][-1]
        
        return {
            "train_loss": train_loss,
            "val_loss": val_loss,
            "epochs": self.epochs
        }
    
    def load_model(self):
        """Load trained model from disk."""
        if self.model_path.exists():
            self.model = load_model(self.model_path)
            print(f"[SUCCESS] Model loaded from {self.model_path}")
            return True
        else:
            print(f"[WARNING] No trained model found at {self.model_path}")
            return False
    
    def predict_next(self, df: pd.DataFrame, days: int = 7) -> list:
        """Predict future prices using trained model."""
        if self.model is None:
            if not self.load_model():
                print("[ERROR] No model available for prediction")
                return []
        
        prices = df['price'].values.reshape(-1, 1)
        scaled_prices = self.scaler.fit_transform(prices)
        
        predictions = []
        last_sequence = scaled_prices[-self.lookback:].reshape(1, self.lookback, 1)
        
        for _ in range(days):
            # Predict next value
            predicted_scaled = self.model.predict(last_sequence, verbose=0)
            predicted_price = self.scaler.inverse_transform(predicted_scaled)[0, 0]
            predictions.append(predicted_price)
            
            # Update sequence
            last_sequence = np.append(last_sequence[:, 1:, :], predicted_scaled.reshape(1, 1, 1), axis=1)
        
        return predictions
    
    def is_trained(self) -> bool:
        """Check if model is trained and saved."""
        return self.model_path.exists()
