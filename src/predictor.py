"""
Smart Predictor with Buy/Sell Signals
"""
import numpy as np
import pandas as pd


class CryptoPredictor:
    def __init__(self, lookback: int = 60):
        self.lookback = lookback
    
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
    
    def get_signal(self, df: pd.DataFrame) -> dict:
        """Generate buy/sell signal based on technical analysis."""
        prices = df['price'].values
        
        if len(prices) < 14:
            return {"signal": "HOLD", "confidence": 50, "reason": "Not enough data"}
        
        # Calculate RSI
        rsi = self._calculate_rsi(prices, 14)
        
        # Calculate Moving Averages
        ma7 = np.mean(prices[-7:]) if len(prices) >= 7 else prices[-1]
        ma25 = np.mean(prices[-25:]) if len(prices) >= 25 else prices[-1]
        
        # Generate signal
        if rsi < 30:
            signal = "BUY"
            confidence = min(95, 70 + (30 - rsi))
            reason = f"RSI is oversold ({rsi:.1f}) - Strong buy signal"
        elif rsi > 70:
            signal = "SELL"
            confidence = min(95, 70 + (rsi - 70))
            reason = f"RSI is overbought ({rsi:.1f}) - Strong sell signal"
        elif ma7 > ma25:
            signal = "BUY"
            confidence = 60
            reason = f"MA7 ({ma7:.2f}) > MA25 ({ma25:.2f}) - Uptrend"
        elif ma7 < ma25:
            signal = "SELL"
            confidence = 60
            reason = f"MA7 ({ma7:.2f}) < MA25 ({ma25:.2f}) - Downtrend"
        else:
            signal = "HOLD"
            confidence = 50
            reason = "No clear trend - Hold position"
        
        return {
            "signal": signal,
            "confidence": int(confidence),
            "reason": reason,
            "rsi": round(rsi, 2),
            "ma7": round(ma7, 2),
            "ma25": round(ma25, 2)
        }
    
    def _calculate_rsi(self, prices: np.ndarray, period: int = 14) -> float:
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
