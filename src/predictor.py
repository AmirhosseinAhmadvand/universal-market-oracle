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
                trend = (prices[-1] - prices[-7]) / prices[-7]
                next_price = prices[-1] * (1 + trend * 0.3 + np.random.normal(0, 0.01))
            else:
                next_price = prices[-1] * (1 + np.random.normal(0, 0.02))
            
            predictions.append(next_price)
            prices = np.append(prices, next_price)
        
        return predictions
    
    def get_signal(self, df: pd.DataFrame) -> dict:
        prices = df['price'].values
        
        if len(prices) < 14:
            return {"signal": "HOLD", "confidence": 50, "reason": "Not enough data"}
        
        rsi = self._calculate_rsi(prices, 14)
        ma7 = np.mean(prices[-7:]) if len(prices) >= 7 else prices[-1]
        ma25 = np.mean(prices[-25:]) if len(prices) >= 25 else prices[-1]
        
        # RSI-based signal
        if rsi < 30:
            signal = "BUY"
            confidence = min(95, 70 + (30 - rsi))
            reason_fa = f"RSI اشباع فروش ({rsi:.1f}) - سیگنال خرید قوی"
            reason_en = f"RSI is oversold ({rsi:.1f}) - Strong buy signal"
        elif rsi > 70:
            signal = "SELL"
            confidence = min(95, 70 + (rsi - 70))
            reason_fa = f"RSI اشباع خرید ({rsi:.1f}) - سیگنال فروش قوی"
            reason_en = f"RSI is overbought ({rsi:.1f}) - Strong sell signal"
        elif ma7 > ma25 * 1.02:
            signal = "BUY"
            confidence = 65
            reason_fa = f"MA7 > MA25 - روند صعودی"
            reason_en = f"MA7 ({ma7:.2f}) > MA25 ({ma25:.2f}) - Uptrend"
        elif ma7 < ma25 * 0.98:
            signal = "SELL"
            confidence = 65
            reason_fa = f"MA7 < MA25 - روند نزولی"
            reason_en = f"MA7 ({ma7:.2f}) < MA25 ({ma25:.2f}) - Downtrend"
        else:
            signal = "HOLD"
            confidence = 50
            reason_fa = "روند خنثی - صبر کنید"
            reason_en = "No clear trend - Hold position"
        
        return {
            "signal": signal,
            "confidence": int(confidence),
            "reason_fa": reason_fa,
            "reason_en": reason_en,
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
        return 100 - (100 / (1 + rs))
