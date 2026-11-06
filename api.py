from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn
import webbrowser
import threading
import time

from src.data_fetcher import DataFetcher
from src.predictor import CryptoPredictor
from src.calendar_engine import CalendarEngine
from src.news_engine import NewsEngine
from src.chatbot import ChatBot

app = FastAPI(title="Universal Market Oracle - Empire Edition v4.0")

data_fetcher = DataFetcher(cache_dir="data", cache_minutes=5)
predictor = CryptoPredictor(lookback=60)
calendar_engine = CalendarEngine()
news_engine = NewsEngine()
chatbot = ChatBot()

class ChatRequest(BaseModel):
    message: str

HTML_CONTENT = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Universal Market Oracle - Empire Edition v4.0</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lightweight-charts@4.1.0/dist/lightweight-charts.standalone.production.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
        * { font-family: 'Inter', sans-serif; box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background: linear-gradient(-45deg, #0a0e27, #1a1f3a, #0f1629, #1a1a2e);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
            min-height: 100vh;
            color: white;
            padding: 20px;
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
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
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
        #chart-container { height: 500px; width: 100%; }
        
        /* Search Bar - FIXED */
        .search-wrapper {
            position: relative;
            z-index: 10000;
        }
        .search-input {
            width: 100%;
            padding: 16px 24px;
            background: rgba(0, 0, 0, 0.6);
            border: 2px solid rgba(0, 255, 255, 0.3);
            border-radius: 12px;
            color: white;
            font-size: 18px;
            outline: none;
            transition: all 0.3s;
        }
        .search-input:focus {
            border-color: #00ffff;
            box-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
        }
        .search-dropdown {
            position: absolute;
            top: calc(100% + 8px);
            left: 0;
            right: 0;
            background: rgba(10, 14, 39, 0.98);
            border: 2px solid rgba(0, 255, 255, 0.5);
            border-radius: 12px;
            max-height: 400px;
            overflow-y: auto;
            z-index: 99999;
            display: none;
            box-shadow: 0 10px 50px rgba(0, 0, 0, 0.9);
        }
        .search-item {
            padding: 12px 16px;
            cursor: pointer;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            display: flex;
            align-items: center;
            gap: 12px;
            transition: all 0.2s;
        }
        .search-item:hover { background: rgba(0, 255, 255, 0.15); }
        .search-item-icon { font-size: 24px; }
        .search-item-name { font-weight: 600; color: white; }
        .search-item-symbol { color: #9ca3af; font-size: 12px; }
        .search-item-type {
            margin-left: auto;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 10px;
            text-transform: uppercase;
        }
        .type-crypto { background: rgba(247, 147, 26, 0.2); color: #f7931a; }
        .type-forex { background: rgba(0, 255, 255, 0.2); color: #00ffff; }
        .type-gold { background: rgba(255, 215, 0, 0.2); color: #ffd700; }
        
        /* Chatbot */
        .chatbot-container {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 99999;
        }
        .chatbot-button {
            width: 60px; height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, #00ffff, #0088ff);
            border: none;
            cursor: pointer;
            box-shadow: 0 4px 20px rgba(0, 255, 255, 0.5);
            display: flex; align-items: center; justify-content: center;
            font-size: 28px; transition: all 0.3s;
        }
        .chatbot-button:hover { transform: scale(1.1); box-shadow: 0 6px 30px rgba(0, 255, 255, 0.7); }
        .chatbot-window {
            position: absolute;
            bottom: 80px; right: 0;
            width: 380px; height: 550px;
            background: rgba(10, 14, 39, 0.98);
            border: 2px solid rgba(0, 255, 255, 0.4);
            border-radius: 16px;
            display: none; flex-direction: column;
            overflow: hidden;
            box-shadow: 0 8px 40px rgba(0, 0, 0, 0.8);
        }
        .chatbot-window.active { display: flex; }
        .chatbot-header {
            padding: 16px;
            background: linear-gradient(135deg, rgba(0, 255, 255, 0.2), rgba(0, 136, 255, 0.2));
            border-bottom: 1px solid rgba(0, 255, 255, 0.3);
        }
        .chatbot-messages { flex: 1; overflow-y: auto; padding: 16px; }
        .chat-message {
            margin-bottom: 12px; padding: 10px 14px;
            border-radius: 12px; max-width: 85%;
            font-size: 14px; line-height: 1.4;
            white-space: pre-wrap;
        }
        .chat-message.bot {
            background: rgba(0, 255, 255, 0.1);
            border: 1px solid rgba(0, 255, 255, 0.2);
            margin-right: auto;
        }
        .chat-message.user {
            background: rgba(0, 136, 255, 0.2);
            border: 1px solid rgba(0, 136, 255, 0.3);
            margin-left: auto; text-align: right;
        }
        .chatbot-input-container {
            padding: 12px; border-top: 1px solid rgba(255, 255, 255, 0.1);
            display: flex; gap: 8px;
        }
        .chatbot-input {
            flex: 1; padding: 10px 14px;
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px; color: white; outline: none;
        }
        .chatbot-send {
            padding: 10px 16px;
            background: linear-gradient(135deg, #00ffff, #0088ff);
            border: none; border-radius: 8px;
            color: white; cursor: pointer; font-weight: 600;
        }
        
        .signal-buy { color: #00ff88; text-shadow: 0 0 20px rgba(0, 255, 136, 0.5); }
        .signal-sell { color: #ff4757; text-shadow: 0 0 20px rgba(255, 71, 87, 0.5); }
        .signal-hold { color: #ffd700; text-shadow: 0 0 20px rgba(255, 215, 0, 0.5); }
        
        .calendar-day {
            padding: 8px; text-align: center;
            border-radius: 8px; cursor: pointer;
            transition: all 0.2s;
        }
        .calendar-day:hover { background: rgba(0, 255, 255, 0.1); }
        .calendar-day.today { background: rgba(0, 255, 255, 0.3); border: 2px solid #00ffff; }
        .calendar-day.weekend { color: #ff4757; }
        
        .news-item {
            padding: 12px; border-left: 3px solid;
            background: rgba(255, 255, 255, 0.02);
            border-radius: 8px; margin-bottom: 8px;
            transition: all 0.2s;
        }
        .news-item:hover { background: rgba(255, 255, 255, 0.05); }
        
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: rgba(0, 0, 0, 0.2); }
        ::-webkit-scrollbar-thumb { background: rgba(0, 255, 255, 0.3); border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(0, 255, 255, 0.5); }
    </style>
</head>
<body>
    <div class="max-w-7xl mx-auto">
        <header class="text-center mb-10">
            <h1 class="text-6xl font-extrabold mb-4 glow-text bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600">
                Universal Market Oracle
            </h1>
            <p class="text-gray-400 text-xl">Empire Edition v4.0 - AI-Powered Market Prediction Platform</p>
        </header>

        <!-- Search Bar -->
        <div class="glass-card p-6 mb-8">
            <div class="search-wrapper max-w-3xl mx-auto">
                <input type="text" id="assetSearch" class="search-input" 
                       placeholder="🔍 Search: Bitcoin, Ethereum, Gold, EUR, USD, JPY..."
                       oninput="searchAssets(this.value)" onfocus="if(this.value.length>0) searchAssets(this.value)"
                       onblur="setTimeout(() => document.getElementById('searchDropdown').style.display='none', 200)">
                <div id="searchDropdown" class="search-dropdown"></div>
            </div>
        </div>

        <!-- Selected Asset Info -->
        <div class="glass-card p-6 mb-8" id="selectedAssetInfo" style="display: none;">
            <div class="flex items-center justify-between">
                <div>
                    <div class="text-3xl font-bold text-white" id="selectedAssetName">--</div>
                    <div class="text-gray-400" id="selectedAssetSymbol">--</div>
                </div>
                <div class="text-right">
                    <div class="flex items-center text-sm text-gray-400 mb-2">
                        <span class="live-dot"></span> Live Price
                    </div>
                    <div id="priceDisplay" class="text-4xl font-bold text-cyan-400">$--</div>
                    <div id="priceChange" class="text-sm mt-2">--</div>
                </div>
            </div>
        </div>

        <!-- Stats Grid -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div class="glass-card p-6 text-center">
                <div class="text-sm text-gray-400 mb-2">24h High</div>
                <div id="high24h" class="text-2xl font-bold text-green-400">$--</div>
            </div>
            <div class="glass-card p-6 text-center">
                <div class="text-sm text-gray-400 mb-2">24h Low</div>
                <div id="low24h" class="text-2xl font-bold text-red-400">$--</div>
            </div>
            <div class="glass-card p-6 text-center">
                <div class="text-sm text-gray-400 mb-2">AI Prediction (7D)</div>
                <div id="prediction" class="text-2xl font-bold text-purple-400">$--</div>
            </div>
            <div class="glass-card p-6 text-center">
                <div class="text-sm text-gray-400 mb-2">Trading Signal</div>
                <div id="signalBadge" class="text-2xl font-bold">--</div>
                <div id="signalReason" class="text-xs text-gray-500 mt-2">--</div>
            </div>
        </div>

        <!-- Timeframes -->
        <div class="glass-card p-6 mb-8 flex justify-center gap-3">
            <button class="timeframe-btn" onclick="changeTimeframe('1m')">1m</button>
            <button class="timeframe-btn" onclick="changeTimeframe('5m')">5m</button>
            <button class="timeframe-btn active" onclick="changeTimeframe('1d')">1D</button>
            <button class="timeframe-btn" onclick="changeTimeframe('1w')">1W</button>
            <button class="timeframe-btn" onclick="changeTimeframe('1m_month')">1M</button>
        </div>

        <!-- Chart -->
        <div class="glass-card p-6 mb-8">
            <div class="flex justify-between items-center mb-4">
                <h3 class="text-xl font-bold text-gray-300">📊 Professional Price Chart</h3>
            </div>
            <div id="chart-container"></div>
        </div>

        <!-- Calendar -->
        <div class="glass-card p-6 mb-8">
            <h3 class="text-2xl font-bold text-gray-300 mb-6">📅 Global Events Calendar</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <div>
                    <h4 class="text-lg font-bold text-cyan-400 mb-3">🌍 Gregorian Calendar</h4>
                    <div id="gregorianCalendar" class="glass-card p-4"></div>
                </div>
                <div>
                    <h4 class="text-lg font-bold text-cyan-400 mb-3">🇮🇷 Persian Calendar</h4>
                    <div id="persianCalendar" class="glass-card p-4"></div>
                </div>
            </div>
            <div id="todayEvents" class="mb-6">
                <h4 class="text-lg font-bold text-cyan-400 mb-3">🔴 Today's Events</h4>
                <div id="todayEventsList" class="grid grid-cols-1 md:grid-cols-2 gap-3"></div>
            </div>
            <h4 class="text-lg font-bold text-cyan-400 mb-3">📆 Upcoming Events</h4>
            <div id="upcomingEventsList" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"></div>
        </div>

        <!-- News -->
        <div class="glass-card p-6 mb-8">
            <div class="flex justify-between items-center mb-6">
                <h3 class="text-2xl font-bold text-gray-300">📰 Global News Feed</h3>
                <div class="flex gap-2">
                    <button onclick="loadNews('en')" class="timeframe-btn active" id="btn-en">English</button>
                    <button onclick="loadNews('fa')" class="timeframe-btn" id="btn-fa">فارسی</button>
                </div>
            </div>
            <div id="newsFeed" class="space-y-3"></div>
        </div>
    </div>

    <!-- Chatbot -->
    <div class="chatbot-container">
        <div class="chatbot-window" id="chatbotWindow">
            <div class="chatbot-header">
                <div class="flex items-center justify-between">
                    <div>
                        <div class="font-bold text-white">🤖 Market Oracle AI</div>
                        <div class="text-xs text-gray-400">Online & Offline • Multilingual</div>
                    </div>
                    <button onclick="toggleChatbot()" class="text-white hover:text-cyan-400">✕</button>
                </div>
            </div>
            <div class="chatbot-messages" id="chatMessages">
                <div class="chat-message bot">Hello! I'm Market Oracle AI. Ask me about markets, capitals, famous people, or anything! 🚀</div>
            </div>
            <div class="chatbot-input-container">
                <input type="text" id="chatInput" class="chatbot-input" placeholder="Type your question..." onkeypress="if(event.key==='Enter')sendMessage()">
                <button onclick="sendMessage()" class="chatbot-send">Send</button>
            </div>
        </div>
        <button class="chatbot-button" onclick="toggleChatbot()">🤖</button>
    </div>

    <script>
        let chart = null;
        let lineSeries = null;
        let predictionSeries = null;
        let currentAsset = null;
        let currentTimeframe = '1d';
        let priceUpdateInterval = null;
        let allAssets = [];

        window.onload = async () => {
            await loadAssets();
            loadCalendar();
            loadNews('en');
        };

        async function loadAssets() {
            try {
                const response = await fetch('/api/assets');
                const data = await response.json();
                if (data.status === 'success') allAssets = data.assets;
            } catch (error) { console.error("Failed to load assets:", error); }
        }

        function searchAssets(query) {
            const dropdown = document.getElementById('searchDropdown');
            if (!query || query.length < 1) { dropdown.style.display = 'none'; return; }
            
            const filtered = Object.entries(allAssets).filter(([id, asset]) => 
                asset.name.toLowerCase().includes(query.toLowerCase()) ||
                asset.symbol.toLowerCase().includes(query.toLowerCase()) ||
                id.toLowerCase().includes(query.toLowerCase())
            ).slice(0, 15);
            
            if (filtered.length === 0) { dropdown.style.display = 'none'; return; }
            
            dropdown.innerHTML = filtered.map(([id, asset]) => `
                <div class="search-item" onclick="selectAsset('${id}')">
                    <span class="search-item-icon">${asset.icon}</span>
                    <div>
                        <div class="search-item-name">${asset.name}</div>
                        <div class="search-item-symbol">${asset.symbol}</div>
                    </div>
                    <span class="search-item-type type-${asset.type}">${asset.type}</span>
                </div>
            `).join('');
            dropdown.style.display = 'block';
        }

        async function selectAsset(assetId) {
            currentAsset = assetId;
            document.getElementById('searchDropdown').style.display = 'none';
            document.getElementById('assetSearch').value = '';
            
            const asset = allAssets[assetId];
            document.getElementById('selectedAssetInfo').style.display = 'block';
            document.getElementById('selectedAssetName').innerText = `${asset.icon} ${asset.name}`;
            document.getElementById('selectedAssetSymbol').innerText = asset.symbol;
            
            await loadAssetData(assetId);
            startLiveUpdates(assetId);
        }

        async function loadAssetData(assetId) {
            try {
                const days = getTimeframeDays(currentTimeframe);
                const response = await fetch(`/api/data/${assetId}?days=${days}`);
                const data = await response.json();
                
                if (data.status === 'success') {
                    document.getElementById('priceDisplay').innerText = `$${data.current_price.toLocaleString()}`;
                    document.getElementById('high24h').innerText = `$${data.high_24h.toLocaleString()}`;
                    document.getElementById('low24h').innerText = `$${data.low_24h.toLocaleString()}`;
                    document.getElementById('prediction').innerText = `$${data.predicted_price.toLocaleString()}`;
                    
                    const signalEl = document.getElementById('signalBadge');
                    const reasonEl = document.getElementById('signalReason');
                    signalEl.innerText = data.signal.signal;
                    reasonEl.innerText = data.signal.reason_en;
                    signalEl.className = `text-2xl font-bold signal-${data.signal.signal.toLowerCase()}`;
                    
                    updateChart(data.chart_data, data.predictions);
                }
            } catch (error) { console.error("Failed to load data:", error); }
        }

        function getTimeframeDays(timeframe) {
            const map = { '1m': 1, '5m': 1, '1d': 30, '1w': 90, '1m_month': 365 };
            return map[timeframe] || 30;
        }

        function updateChart(chartData, predictions) {
            const container = document.getElementById('chart-container');
            container.innerHTML = '';
            
            chart = LightweightCharts.createChart(container, {
                width: container.clientWidth,
                height: 500,
                layout: { 
                    background: { color: 'transparent' }, 
                    textColor: '#d1d4dc',
                    fontSize: 12,
                },
                grid: { 
                    vertLines: { color: 'rgba(0, 255, 255, 0.1)', style: 2 }, 
                    horzLines: { color: 'rgba(0, 255, 255, 0.1)', style: 2 } 
                },
                crosshair: { 
                    mode: LightweightCharts.CrosshairMode.Normal,
                    vertLine: { width: 1, color: 'rgba(0, 255, 255, 0.5)', style: 3, labelBackgroundColor: '#00ffff' },
                    horzLine: { width: 1, color: 'rgba(0, 255, 255, 0.5)', style: 3, labelBackgroundColor: '#00ffff' },
                },
                rightPriceScale: { 
                    borderColor: 'rgba(0, 255, 255, 0.3)',
                    scaleMargins: { top: 0.1, bottom: 0.1 }
                },
                timeScale: { 
                    borderColor: 'rgba(0, 255, 255, 0.3)', 
                    timeVisible: true,
                    secondsVisible: false,
                },
                handleScroll: { vertTouchDrag: false, mouseWheel: true, pressedMouseMove: true },
                handleScale: { axisPressedMouseMove: true, mouseWheel: true, pinch: true },
            });
            
            lineSeries = chart.addLineSeries({ 
                color: '#00ffff', 
                lineWidth: 2,
                priceLineVisible: true,
                lastValueVisible: true,
            });
            lineSeries.setData(chartData.map(d => ({ time: d.time, value: d.price })));
            
            predictionSeries = chart.addLineSeries({ 
                color: '#ff00ff', 
                lineWidth: 2, 
                lineStyle: 2,
                priceLineVisible: false,
                lastValueVisible: true,
            });
            predictionSeries.setData(predictions);
            
            chart.timeScale().fitContent();
            
            window.addEventListener('resize', () => {
                if (chart) chart.applyOptions({ width: container.clientWidth });
            });
        }

        function changeTimeframe(timeframe) {
            currentTimeframe = timeframe;
            document.querySelectorAll('.timeframe-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            if (currentAsset) loadAssetData(currentAsset);
        }

        async function startLiveUpdates(assetId) {
            if (priceUpdateInterval) clearInterval(priceUpdateInterval);
            priceUpdateInterval = setInterval(async () => {
                try {
                    const response = await fetch(`/api/price/${assetId}`);
                    const data = await response.json();
                    if (data.status === 'success') {
                        const priceEl = document.getElementById('priceDisplay');
                        const oldPrice = parseFloat(priceEl.innerText.replace(/[$,]/g, ''));
                        const newPrice = data.price;
                        priceEl.innerText = `$${newPrice.toLocaleString()}`;
                        
                        const change = ((newPrice - oldPrice) / oldPrice * 100).toFixed(2);
                        const changeEl = document.getElementById('priceChange');
                        if (change > 0) {
                            changeEl.innerText = `▲ +${change}%`;
                            changeEl.className = 'text-sm mt-2 text-green-400';
                        } else if (change < 0) {
                            changeEl.innerText = `▼ ${change}%`;
                            changeEl.className = 'text-sm mt-2 text-red-400';
                        }
                    }
                } catch (error) { console.error("Failed to update price:", error); }
            }, 3000);
        }

        async function loadCalendar() {
            try {
                const response = await fetch('/api/calendar');
                const data = await response.json();
                if (data.status === 'success') {
                    renderGregorianCalendar(data.gregorian_calendar);
                    renderPersianCalendar(data.persian_calendar);
                    renderTodayEvents(data.today_events);
                    renderUpcomingEvents(data.upcoming_events);
                }
            } catch (error) { console.error("Failed to load calendar:", error); }
        }

        function renderGregorianCalendar(cal) {
            const container = document.getElementById('gregorianCalendar');
            container.innerHTML = `
                <div class="text-center mb-4"><div class="text-xl font-bold text-cyan-400">${cal.month_name} ${cal.year}</div></div>
                <div class="grid grid-cols-7 gap-1">
                    ${['S','M','T','W','T','F','S'].map(d => `<div class="text-xs text-gray-500 text-center">${d}</div>`).join('')}
                    ${cal.days.map(d => `<div class="calendar-day ${d.is_today ? 'today' : ''} ${d.is_weekend ? 'weekend' : ''}">${d.day}</div>`).join('')}
                </div>`;
        }

        function renderPersianCalendar(cal) {
            const container = document.getElementById('persianCalendar');
            container.innerHTML = `
                <div class="text-center mb-4"><div class="text-xl font-bold text-cyan-400">${cal.month_name} ${cal.year}</div></div>
                <div class="grid grid-cols-7 gap-1">
                    ${['ش','ی','د','س','چ','پ','ج'].map(d => `<div class="text-xs text-gray-500 text-center">${d}</div>`).join('')}
                    ${cal.days.map(d => `<div class="calendar-day ${d.is_today ? 'today' : ''} ${d.is_weekend ? 'weekend' : ''}">${d.day}</div>`).join('')}
                </div>`;
        }

        function renderTodayEvents(events) {
            const container = document.getElementById('todayEventsList');
            const section = document.getElementById('todayEvents');
            if (events.length === 0) { section.style.display = 'none'; return; }
            section.style.display = 'block';
            container.innerHTML = events.map(event => `
                <div class="glass-card p-4 border-l-4" style="border-color: ${getImpactColor(event.impact)}">
                    <div class="flex items-center gap-3 mb-2">
                        <span class="text-3xl">${event.icon}</span>
                        <div><div class="font-bold text-white">${event.name}</div><div class="text-sm text-gray-400">${event.name_fa || ''}</div></div>
                    </div>
                    <div class="text-xs text-gray-500 mb-2">${event.description_fa || event.description}</div>
                    <div class="flex gap-2 flex-wrap">${event.markets.map(m => `<span class="text-xs px-2 py-1 rounded bg-white/10">${m.toUpperCase()}</span>`).join('')}</div>
                    <div class="mt-2 text-xs font-bold" style="color: ${getImpactColor(event.impact)}">Impact: ${event.impact.toUpperCase()}</div>
                </div>`).join('');
        }

        function renderUpcomingEvents(events) {
            const container = document.getElementById('upcomingEventsList');
            if (events.length === 0) { container.innerHTML = '<div class="text-gray-500 col-span-3 text-center py-8">No upcoming events</div>'; return; }
            container.innerHTML = events.map(event => `
                <div class="glass-card p-4 hover:scale-105 transition-transform" style="border-top: 3px solid ${getImpactColor(event.impact)}">
                    <div class="flex items-center justify-between mb-3">
                        <span class="text-4xl">${event.icon}</span>
                        <div class="text-right"><div class="text-xs text-gray-400">In</div><div class="text-lg font-bold text-cyan-400">${event.days_until} days</div></div>
                    </div>
                    <div class="font-bold text-white mb-1">${event.name}</div>
                    <div class="text-sm text-gray-400 mb-2">${event.name_fa || ''}</div>
                    <div class="text-xs text-gray-500 mb-3">${event.description_fa || event.description}</div>
                    <div class="flex gap-1 flex-wrap mb-2">${event.markets.map(m => `<span class="text-xs px-2 py-1 rounded bg-white/10">${m.toUpperCase()}</span>`).join('')}</div>
                    <div class="text-xs font-bold" style="color: ${getImpactColor(event.impact)}">${event.impact.toUpperCase()} IMPACT</div>
                </div>`).join('');
        }

        function getImpactColor(impact) {
            const colors = {'low': '#00ff88', 'medium': '#ffff00', 'high': '#ff8800', 'extreme': '#ff0000'};
            return colors[impact] || '#ffffff';
        }

        async function loadNews(lang) {
            document.getElementById('btn-en').classList.toggle('active', lang === 'en');
            document.getElementById('btn-fa').classList.toggle('active', lang === 'fa');
            try {
                const response = await fetch(`/api/news?lang=${lang}`);
                const data = await response.json();
                if (data.status === 'success') renderNews(data.news);
            } catch (error) { console.error("Failed to load news:", error); }
        }

        function renderNews(news) {
            document.getElementById('newsFeed').innerHTML = news.map(item => `
                <div class="news-item" style="border-color: ${getImpactColor(item.impact)}">
                    <div class="flex items-center gap-3 mb-2">
                        <span class="text-2xl">${item.icon}</span>
                        <div><div class="font-bold text-white">${item.source}</div><div class="text-xs text-gray-500">${item.time}</div></div>
                    </div>
                    <div class="text-sm text-gray-300 mb-2">${item.title}</div>
                    <div class="flex gap-2 flex-wrap">${item.markets.map(m => `<span class="text-xs px-2 py-1 rounded bg-white/10">${m.toUpperCase()}</span>`).join('')}</div>
                </div>`).join('');
        }

        function toggleChatbot() {
            document.getElementById('chatbotWindow').classList.toggle('active');
        }

        async function sendMessage() {
            const input = document.getElementById('chatInput');
            const message = input.value.trim();
            if (!message) return;
            
            const messagesContainer = document.getElementById('chatMessages');
            messagesContainer.innerHTML += `<div class="chat-message user">${message}</div>`;
            input.value = '';
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: message})
                });
                const data = await response.json();
                messagesContainer.innerHTML += `<div class="chat-message bot">${data.response}</div>`;
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            } catch (error) {
                messagesContainer.innerHTML += `<div class="chat-message bot">Connection error. Try again! 🤖</div>`;
            }
        }
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTML_CONTENT


@app.get("/api/assets")
async def get_all_assets():
    try:
        return {"status": "success", "assets": data_fetcher.get_all_assets()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/data/{symbol}")
async def get_asset_data(symbol: str, days: int = 30):
    try:
        df = data_fetcher.fetch_historical_data(symbol, days=max(1, days))
        if df.empty:
            raise HTTPException(status_code=404, detail="No data available")
        
        current_data = data_fetcher.get_current_price(symbol)
        predictions = predictor.predict_next(df, days=7)
        signal = predictor.get_signal(df)
        
        last_timestamp = int(df.iloc[-1]['date'].timestamp())
        prediction_data = [{"time": last_timestamp + (i + 1) * 86400, "value": round(pred, 2)} for i, pred in enumerate(predictions)]
        chart_data = [{"time": int(row['date'].timestamp()), "price": round(row['price'], 2)} for _, row in df.iterrows()]
        
        return {
            "status": "success", "symbol": symbol.upper(),
            "current_price": current_data.get("price", 0),
            "high_24h": df['price'].max(), "low_24h": df['price'].min(),
            "predicted_price": predictions[-1],
            "chart_data": chart_data, "predictions": prediction_data,
            "signal": signal
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/price/{symbol}")
async def get_live_price(symbol: str):
    try:
        current_data = data_fetcher.get_current_price(symbol)
        return {"status": "success", "price": current_data.get("price", 0)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/calendar")
async def get_calendar():
    try:
        return {
            "status": "success",
            "upcoming_events": calendar_engine.get_upcoming_events(30),
            "today_events": calendar_engine.get_today_events(),
            "gregorian_calendar": calendar_engine.get_gregorian_calendar_month(),
            "persian_calendar": calendar_engine.get_persian_calendar_month()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/news")
async def get_news(lang: str = "en"):
    try:
        return news_engine.get_latest_news(lang)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        response = chatbot.get_response(request.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def open_browser():
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:8000")


if __name__ == "__main__":
    threading.Thread(target=open_browser).start()
    uvicorn.run(app, host="127.0.0.1", port=8000)
