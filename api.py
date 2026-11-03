from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import uvicorn
import webbrowser
import threading
import time

from src.data_fetcher import DataFetcher
from src.predictor import CryptoPredictor

app = FastAPI(title="Universal Market Oracle")

HTML_CONTENT = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Universal Market Oracle</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lightweight-charts@4.1.0/dist/lightweight-charts.standalone.production.js"></script>
    <style>
        * { font-family: 'Inter', sans-serif; }
        body {
            background: linear-gradient(-45deg, #0a0e27, #1a1f3a, #0f1629, #1a1a2e);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
            min-height: 100vh;
            color: white;
        }
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
        }
        .glow-text { text-shadow: 0 0 20px rgba(0, 255, 255, 0.5); }
        .live-dot {
            width: 8px; height: 8px;
            background: #00ff88; border-radius: 50%;
            display: inline-block; margin-right: 6px;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .timeframe-btn {
            padding: 8px 16px; border-radius: 8px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            cursor: pointer; transition: all 0.3s ease;
            color: white;
        }
        .timeframe-btn:hover, .timeframe-btn.active {
            background: linear-gradient(135deg, rgba(0, 255, 255, 0.3), rgba(0, 255, 255, 0.1));
            border-color: #00ffff;
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.4);
        }
        .asset-btn {
            padding: 12px 20px; border-radius: 12px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            cursor: pointer; transition: all 0.3s ease;
            color: white; font-size: 16px;
        }
        .asset-btn:hover, .asset-btn.active {
            background: linear-gradient(135deg, rgba(0, 255, 255, 0.3), rgba(0, 255, 255, 0.1));
            border-color: #00ffff;
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.4);
            transform: scale(1.05);
        }
        #chart-container { height: 500px; width: 100%; }
    </style>
</head>
<body class="p-6">
    <div class="max-w-7xl mx-auto">
        <header class="text-center mb-10">
            <h1 class="text-6xl font-extrabold mb-4 glow-text bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600">
                Universal Market Oracle
            </h1>
            <p class="text-gray-400 text-xl">AI-Powered Market Prediction Platform</p>
        </header>

        <!-- Asset Selector -->
        <div class="glass-card p-6 mb-8">
            <h3 class="text-xl font-bold text-gray-300 mb-4 text-center">Select Asset</h3>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <button onclick="loadAssetData('bitcoin')" class="asset-btn active" id="btn-bitcoin">₿ Bitcoin</button>
                <button onclick="loadAssetData('ethereum')" class="asset-btn" id="btn-ethereum">Ξ Ethereum</button>
                <button onclick="loadAssetData('gold')" class="asset-btn" id="btn-gold">🥇 Gold</button>
                <button onclick="loadAssetData('eur')" class="asset-btn" id="btn-eur">💶 EUR/USD</button>
            </div>
        </div>

        <!-- Stats -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div class="glass-card p-6 text-center">
                <div class="flex items-center justify-center text-sm text-gray-400 mb-2">
                    <span class="live-dot"></span> Live Price
                </div>
                <div id="priceDisplay" class="text-4xl font-bold text-cyan-400">$--</div>
                <div id="assetName" class="text-gray-500 text-sm mt-2">--</div>
            </div>
            <div class="glass-card p-6 text-center">
                <div class="text-sm text-gray-400 mb-2">24h High</div>
                <div id="high24h" class="text-2xl font-bold text-green-400">$--</div>
            </div>
            <div class="glass-card p-6 text-center">
                <div class="text-sm text-gray-400 mb-2">24h Low</div>
                <div id="low24h" class="text-2xl font-bold text-red-400">$--</div>
            </div>
            <div class="glass-card p-6 text-center">
                <div class="text-sm text-gray-400 mb-2">AI Prediction</div>
                <div id="prediction" class="text-2xl font-bold text-purple-400">--</div>
            </div>
        </div>

        <!-- Timeframes -->
        <div class="glass-card p-6 mb-8 flex justify-center gap-3">
            <button class="timeframe-btn active" onclick="changeTimeframe('1d')">1D</button>
            <button class="timeframe-btn" onclick="changeTimeframe('1w')">1W</button>
            <button class="timeframe-btn" onclick="changeTimeframe('1m')">1M</button>
        </div>

        <!-- Chart -->
        <div class="glass-card p-6 mb-8">
            <div class="flex justify-between items-center mb-4">
                <h3 class="text-xl font-bold text-gray-300">Price Chart with AI Prediction</h3>
            </div>
            <div id="chart-container"></div>
        </div>
    </div>

    <script>
        let chart = null;
        let lineSeries = null;
        let predictionSeries = null;
        let currentAsset = 'bitcoin';
        let currentTimeframe = '1d';
        let priceUpdateInterval = null;

        window.onload = () => {
            loadAssetData('bitcoin');
            startLiveUpdates('bitcoin');
        };

        async function loadAssetData(assetId) {
            currentAsset = assetId;
            
            // Update active button
            document.querySelectorAll('.asset-btn').forEach(btn => btn.classList.remove('active'));
            const activeBtn = document.getElementById('btn-' + assetId);
            if (activeBtn) activeBtn.classList.add('active');
            
            try {
                const days = getTimeframeDays(currentTimeframe);
                const response = await fetch(`/api/data/${assetId}?days=${days}`);
                const data = await response.json();
                
                if (data.status === 'success') {
                    document.getElementById('priceDisplay').innerText = `$${data.current_price.toLocaleString()}`;
                    document.getElementById('assetName').innerText = data.symbol;
                    document.getElementById('high24h').innerText = `$${data.high_24h.toLocaleString()}`;
                    document.getElementById('low24h').innerText = `$${data.low_24h.toLocaleString()}`;
                    document.getElementById('prediction').innerText = `$${data.predicted_price.toLocaleString()}`;
                    
                    updateChart(data.chart_data, data.predictions);
                }
            } catch (error) {
                console.error("Failed to load data:", error);
            }
        }

        function getTimeframeDays(timeframe) {
            const map = { '1d': 1, '1w': 7, '1m': 30 };
            return map[timeframe] || 1;
        }

        function updateChart(chartData, predictions) {
            const container = document.getElementById('chart-container');
            container.innerHTML = '';
            
            chart = LightweightCharts.createChart(container, {
                width: container.clientWidth,
                height: 500,
                layout: { background: { color: 'transparent' }, textColor: '#d1d4dc' },
                grid: { vertLines: { color: 'rgba(0, 255, 255, 0.1)' }, horzLines: { color: 'rgba(0, 255, 255, 0.1)' } },
                crosshair: { mode: LightweightCharts.CrosshairMode.Normal },
                rightPriceScale: { borderColor: 'rgba(0, 255, 255, 0.3)' },
                timeScale: { borderColor: 'rgba(0, 255, 255, 0.3)', timeVisible: true },
            });
            
            lineSeries = chart.addLineSeries({ color: '#00ffff', lineWidth: 2 });
            lineSeries.setData(chartData.map(d => ({ time: d.time, value: d.price })));
            
            predictionSeries = chart.addLineSeries({ 
                color: '#ff00ff', 
                lineWidth: 2, 
                lineStyle: 2
            });
            predictionSeries.setData(predictions);
            
            chart.timeScale().fitContent();
        }

        function changeTimeframe(timeframe) {
            currentTimeframe = timeframe;
            document.querySelectorAll('.timeframe-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            loadAssetData(currentAsset);
        }

        async function startLiveUpdates(assetId) {
            if (priceUpdateInterval) clearInterval(priceUpdateInterval);
            priceUpdateInterval = setInterval(async () => {
                try {
                    const response = await fetch(`/api/price/${assetId}`);
                    const data = await response.json();
                    if (data.status === 'success') {
                        document.getElementById('priceDisplay').innerText = `$${data.price.toLocaleString()}`;
                    }
                } catch (error) {
                    console.error("Failed to update price:", error);
                }
            }, 3000);
        }
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTML_CONTENT


@app.get("/api/data/{symbol}")
async def get_asset_data(symbol: str, days: int = 1):
    try:
        fetcher = DataFetcher(cache_dir="data", cache_hours=1)
        df = fetcher.fetch_historical_data(symbol, days=days)
        
        if df.empty:
            raise HTTPException(status_code=404, detail="No data available")
        
        current_data = fetcher.get_current_price(symbol)
        
        predictor = CryptoPredictor(lookback=60)
        predictions = predictor.predict_next(df, days=7)
        
        last_timestamp = int(df.iloc[-1]['date'].timestamp())
        prediction_data = []
        for i, pred in enumerate(predictions):
            prediction_data.append({
                "time": last_timestamp + (i + 1) * 86400,
                "value": round(pred, 2)
            })
        
        chart_data = []
        for _, row in df.iterrows():
            chart_data.append({
                "time": int(row['date'].timestamp()),
                "price": round(row['price'], 2)
            })
        
        return {
            "status": "success",
            "symbol": symbol.upper(),
            "current_price": current_data.get("price", 0),
            "high_24h": df['price'].max(),
            "low_24h": df['price'].min(),
            "predicted_price": predictions[-1],
            "chart_data": chart_data,
            "predictions": prediction_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/price/{symbol}")
async def get_live_price(symbol: str):
    try:
        fetcher = DataFetcher(cache_dir="data", cache_hours=0.1)
        current_data = fetcher.get_current_price(symbol)
        return {"status": "success", "price": current_data.get("price", 0)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def open_browser():
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:8000")


if __name__ == "__main__":
    threading.Thread(target=open_browser).start()
    uvicorn.run(app, host="127.0.0.1", port=8000)
