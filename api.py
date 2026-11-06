from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn
import webbrowser
import threading
import time
import requests
import numpy as np
import pandas as pd

from src.data_fetcher import DataFetcher
from src.predictor import CryptoPredictor
from src.calendar_engine import CalendarEngine
from src.news_engine import NewsEngine
from src.chatbot import ChatBot

app = FastAPI(title="Universal Market Oracle - Empire Edition v9.0")

# Initialize engines
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
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Universal Market Oracle - Empire Edition v9.0</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lightweight-charts@4.1.0/dist/lightweight-charts.standalone.production.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
        
        :root {
            --bg-primary: #0a0e27;
            --bg-secondary: #1a1f3a;
            --text-primary: #ffffff;
            --text-secondary: #9ca3af;
            --glass-bg: rgba(255, 255, 255, 0.03);
            --glass-border: rgba(255, 255, 255, 0.08);
            --accent-cyan: #00ffff;
            --accent-green: #00ff88;
            --accent-red: #ff4757;
            --accent-purple: #a855f7;
            --accent-orange: #ff8800;
            --accent-yellow: #ffd700;
        }
        
        body.light-mode {
            --bg-primary: #f0f4f8;
            --bg-secondary: #ffffff;
            --text-primary: #1a202c;
            --text-secondary: #4a5568;
            --glass-bg: rgba(255, 255, 255, 0.7);
            --glass-border: rgba(0, 0, 0, 0.1);
            --accent-cyan: #0891b2;
            --accent-green: #059669;
            --accent-red: #dc2626;
            --accent-purple: #7c3aed;
            --accent-orange: #ea580c;
            --accent-yellow: #ca8a04;
        }
        
        * {
            font-family: 'Inter', sans-serif;
            box-sizing: border-box;
            transition: background-color 0.3s, color 0.3s;
        }
        
        body {
            background: var(--bg-primary);
            min-height: 100vh;
            color: var(--text-primary);
            overflow-x: hidden;
            margin: 0;
            padding: 24px;
        }
        
        body.light-mode {
            background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 100%);
        }
        
        .animated-bg {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            z-index: -1;
            background: linear-gradient(-45deg, var(--bg-primary), var(--bg-secondary), #0f1629, #1a1a2e);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
        }
        
        body.light-mode .animated-bg {
            background: linear-gradient(-45deg, #f0f4f8, #e2e8f0, #cbd5e1, #94a3b8);
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .particle {
            position: fixed;
            border-radius: 50%;
            background: rgba(0, 255, 255, 0.3);
            pointer-events: none;
            animation: float 20s infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { transform: translateY(-100vh) rotate(720deg); opacity: 0; }
        }
        
        .glass-card {
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5), 
                        inset 0 0 20px rgba(255, 255, 255, 0.05);
            transition: all 0.3s ease;
            border-radius: 16px;
        }
        
        body.light-mode .glass-card {
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1), 
                        inset 0 0 20px rgba(255, 255, 255, 0.5);
        }
        
        .glass-card:hover {
            box-shadow: 0 12px 40px 0 rgba(0, 255, 255, 0.2), 
                        inset 0 0 30px rgba(255, 255, 255, 0.1);
            border-color: rgba(0, 255, 255, 0.3);
            transform: translateY(-2px);
        }
        
        .glow-text {
            text-shadow: 0 0 20px rgba(0, 255, 255, 0.5),
                         0 0 40px rgba(0, 255, 255, 0.3);
        }
        
        body.light-mode .glow-text { text-shadow: none; }
        
        .search-container { position: relative; z-index: 1000; }
        
        .search-input {
            width: 100%;
            padding: 16px 24px;
            background: rgba(0, 0, 0, 0.4);
            border: 2px solid rgba(0, 255, 255, 0.3);
            border-radius: 12px;
            color: var(--text-primary);
            font-size: 18px;
            outline: none;
            transition: all 0.3s;
        }
        
        body.light-mode .search-input {
            background: rgba(255, 255, 255, 0.8);
            border-color: rgba(8, 145, 178, 0.3);
            color: var(--text-primary);
        }
        
        .search-input:focus {
            border-color: var(--accent-cyan);
            box-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
        }
        
        .search-dropdown {
            position: absolute;
            top: calc(100% + 8px);
            left: 0; right: 0;
            background: rgba(10, 14, 39, 0.98);
            border: 2px solid rgba(0, 255, 255, 0.5);
            border-radius: 12px;
            max-height: 400px;
            overflow-y: auto;
            z-index: 99999;
            display: none;
            box-shadow: 0 10px 50px rgba(0, 0, 0, 0.9);
        }
        
        body.light-mode .search-dropdown {
            background: rgba(255, 255, 255, 0.98);
            border-color: rgba(8, 145, 178, 0.5);
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
        
        .search-item:hover {
            background: rgba(0, 255, 255, 0.15);
            padding-left: 20px;
        }
        
        .search-item-icon { font-size: 24px; }
        .search-item-name { font-weight: 600; color: var(--text-primary); }
        .search-item-symbol { color: var(--text-secondary); font-size: 12px; }
        .search-item-type {
            margin-left: auto;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 10px;
            text-transform: uppercase;
        }
        .type-crypto { background: rgba(247, 147, 26, 0.2); color: #f7931a; }
        .type-forex { background: rgba(0, 255, 255, 0.2); color: var(--accent-cyan); }
        .type-gold { background: rgba(255, 215, 0, 0.2); color: #ffd700; }
        
        .live-indicator {
            display: inline-block;
            width: 10px; height: 10px;
            background: var(--accent-green);
            border-radius: 50%;
            animation: pulse 2s infinite;
            margin-right: 10px;
            box-shadow: 0 0 10px var(--accent-green);
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(0.8); }
        }
        
        .timeframe-btn {
            padding: 8px 16px;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 600;
            color: var(--text-primary);
        }
        
        body.light-mode .timeframe-btn {
            background: rgba(0, 0, 0, 0.05);
            border-color: rgba(0, 0, 0, 0.1);
        }
        
        .timeframe-btn:hover, .timeframe-btn.active {
            background: linear-gradient(135deg, rgba(0, 255, 255, 0.3), rgba(0, 255, 255, 0.1));
            border-color: var(--accent-cyan);
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.4);
            transform: scale(1.05);
        }
        
        #chart-container { 
            height: 600px; 
            width: 100%;
            border-radius: 12px;
            overflow: hidden;
        }
        
        #rsi-container { 
            height: 200px; 
            width: 100%;
            border-radius: 12px;
            overflow: hidden;
        }
        
        .stat-card {
            position: relative;
            overflow: hidden;
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            top: -50%; left: -50%;
            width: 200%; height: 200%;
            background: radial-gradient(circle, rgba(0, 255, 255, 0.1) 0%, transparent 70%);
            opacity: 0;
            transition: opacity 0.3s;
        }
        
        .stat-card:hover::before { opacity: 1; }
        
        .signal-buy { color: var(--accent-green); text-shadow: 0 0 20px rgba(0, 255, 136, 0.5); }
        .signal-sell { color: var(--accent-red); text-shadow: 0 0 20px rgba(255, 71, 87, 0.5); }
        .signal-hold { color: var(--accent-yellow); text-shadow: 0 0 20px rgba(255, 215, 0, 0.5); }
        
        body.light-mode .signal-buy,
        body.light-mode .signal-sell,
        body.light-mode .signal-hold { text-shadow: none; }
        
        .price-up { color: var(--accent-green); }
        .price-down { color: var(--accent-red); }
        
        .news-ticker {
            overflow: hidden;
            white-space: nowrap;
            background: rgba(0, 255, 255, 0.05);
            border: 1px solid rgba(0, 255, 255, 0.2);
            border-radius: 8px;
            padding: 8px 0;
            margin-bottom: 20px;
        }
        
        .news-ticker-content {
            display: inline-block;
            animation: ticker 60s linear infinite;
        }
        
        @keyframes ticker {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }
        
        .news-ticker-item {
            display: inline-block;
            padding: 0 30px;
            color: var(--text-primary);
            font-size: 14px;
        }
        
        .theme-toggle {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 99998;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--accent-cyan), #0088ff);
            border: none;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            box-shadow: 0 4px 20px rgba(0, 255, 255, 0.5);
            transition: all 0.3s;
        }
        
        .theme-toggle:hover {
            transform: scale(1.1) rotate(180deg);
        }
        
        .alert-item {
            padding: 12px;
            background: rgba(0, 255, 255, 0.05);
            border: 1px solid rgba(0, 255, 255, 0.2);
            border-radius: 8px;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .alert-item.triggered {
            background: rgba(0, 255, 136, 0.2);
            border-color: var(--accent-green);
            animation: alertPulse 2s infinite;
        }
        
        @keyframes alertPulse {
            0%, 100% { box-shadow: 0 0 0 0 rgba(0, 255, 136, 0.7); }
            50% { box-shadow: 0 0 0 10px rgba(0, 255, 136, 0); }
        }
        
        .portfolio-table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .portfolio-table th {
            padding: 12px;
            text-align: left;
            border-bottom: 2px solid var(--glass-border);
            color: var(--text-secondary);
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .portfolio-table td {
            padding: 12px;
            border-bottom: 1px solid var(--glass-border);
            color: var(--text-primary);
        }
        
        .portfolio-table tr:hover {
            background: rgba(0, 255, 255, 0.05);
        }
        
        .profit { color: var(--accent-green); font-weight: bold; }
        .loss { color: var(--accent-red); font-weight: bold; }
        
        .calc-input {
            width: 100%;
            padding: 12px;
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid var(--glass-border);
            border-radius: 8px;
            color: var(--text-primary);
            font-size: 14px;
            outline: none;
        }
        
        body.light-mode .calc-input {
            background: rgba(255, 255, 255, 0.8);
        }
        
        .calc-input:focus {
            border-color: var(--accent-cyan);
        }
        
        .calc-result {
            padding: 16px;
            background: rgba(0, 255, 255, 0.05);
            border: 1px solid rgba(0, 255, 255, 0.2);
            border-radius: 8px;
            margin-top: 12px;
        }
        
        .calc-result-label {
            font-size: 12px;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .calc-result-value {
            font-size: 24px;
            font-weight: bold;
            margin-top: 4px;
        }
        
        .tab-btn {
            padding: 10px 20px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--glass-border);
            border-radius: 8px 8px 0 0;
            cursor: pointer;
            color: var(--text-secondary);
            font-weight: 600;
            transition: all 0.3s;
        }
        
        .tab-btn.active {
            background: var(--glass-bg);
            color: var(--accent-cyan);
            border-bottom-color: transparent;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .news-item {
            padding: 12px;
            border-left: 3px solid;
            background: rgba(255, 255, 255, 0.02);
            border-radius: 8px;
            margin-bottom: 8px;
            transition: all 0.2s;
        }
        .news-item:hover { background: rgba(255, 255, 255, 0.05); }
        
        .calendar-day {
            padding: 8px;
            text-align: center;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .calendar-day:hover { background: rgba(0, 255, 255, 0.1); }
        .calendar-day.today { background: rgba(0, 255, 255, 0.3); border: 2px solid var(--accent-cyan); }
        .calendar-day.weekend { color: var(--accent-red); }
        
        .chatbot-container {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 99999;
        }
        .chatbot-button {
            width: 60px; height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--accent-cyan), #0088ff);
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
        body.light-mode .chatbot-window {
            background: rgba(255, 255, 255, 0.98);
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
            border-radius: 8px; color: var(--text-primary); outline: none;
        }
        body.light-mode .chatbot-input {
            background: rgba(0, 0, 0, 0.05);
            border-color: rgba(0, 0, 0, 0.1);
        }
        .chatbot-send {
            padding: 10px 16px;
            background: linear-gradient(135deg, var(--accent-cyan), #0088ff);
            border: none; border-radius: 8px;
            color: white; cursor: pointer; font-weight: 600;
        }
        
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: rgba(0, 0, 0, 0.2); }
        ::-webkit-scrollbar-thumb { background: rgba(0, 255, 255, 0.3); border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(0, 255, 255, 0.5); }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .fade-in { animation: fadeIn 0.5s ease-out; }
        
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }
        .bounce { animation: bounce 2s infinite; }
        
        .modal-overlay {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.7);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 999999;
        }
        
        .modal-overlay.active {
            display: flex;
        }
        
        .modal-content {
            background: var(--bg-secondary);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
            padding: 24px;
            max-width: 500px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
        }
        
        .ai-panel {
            background: linear-gradient(135deg, rgba(168, 85, 247, 0.1), rgba(0, 255, 255, 0.1));
            border: 1px solid rgba(168, 85, 247, 0.3);
            border-radius: 12px;
            padding: 20px;
            margin-top: 16px;
        }
        
        .ai-panel-title {
            font-size: 18px;
            font-weight: bold;
            color: var(--accent-purple);
            margin-bottom: 12px;
        }
        
        .indicator-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            margin: 4px;
        }
        
        .indicator-bullish {
            background: rgba(0, 255, 136, 0.2);
            color: var(--accent-green);
        }
        
        .indicator-bearish {
            background: rgba(255, 71, 87, 0.2);
            color: var(--accent-red);
        }
        
        .indicator-neutral {
            background: rgba(255, 215, 0, 0.2);
            color: var(--accent-yellow);
        }
        
        .lang-toggle {
            padding: 6px 12px;
            border-radius: 6px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--glass-border);
            cursor: pointer;
            font-weight: 600;
            color: var(--text-secondary);
            transition: all 0.3s;
        }
        
        .lang-toggle.active {
            background: rgba(0, 255, 255, 0.2);
            color: var(--accent-cyan);
            border-color: var(--accent-cyan);
        }
    </style>
</head>
<body>
    <div class="animated-bg"></div>
    <div id="particles"></div>

    <button class="theme-toggle" onclick="toggleTheme()" title="Toggle Dark/Light Mode">🌙</button>

    <div class="max-w-7xl mx-auto">
        <header class="text-center mb-10">
            <h1 class="text-7xl font-extrabold mb-4 glow-text bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600">
                Universal Market Oracle
            </h1>
            <p class="text-xl" style="color: var(--text-secondary);">Empire Edition v9.0 - Professional Charts with Accurate Data</p>
        </header>

        <!-- Live News Ticker -->
        <div class="news-ticker mb-6">
            <div class="news-ticker-content" id="newsTicker">
                <span class="news-ticker-item">🚀 Loading latest news...</span>
            </div>
        </div>

        <!-- Search Bar -->
        <div class="glass-card rounded-3xl p-8 mb-8" style="position: relative; z-index: 1000;">
            <div class="search-container max-w-3xl mx-auto">
                <input type="text" id="assetSearch" class="search-input" 
                       placeholder="🔍 Search cryptocurrency (e.g., bitcoin, ethereum, dogecoin)..."
                       oninput="searchAssets(this.value)" onblur="setTimeout(() => document.getElementById('searchDropdown').style.display='none', 200)">
                <div id="searchDropdown" class="search-dropdown"></div>
            </div>
        </div>

        <!-- Empty State -->
        <div id="emptyState" class="glass-card rounded-3xl p-20 text-center mb-8 fade-in">
            <div class="text-8xl mb-6 bounce">🔍</div>
            <h2 class="text-3xl font-bold mb-4" style="color: var(--text-primary);">Select a Cryptocurrency</h2>
            <p class="text-lg" style="color: var(--text-secondary);">Search and select a coin to view real-time price and professional analysis</p>
        </div>

        <!-- Dashboard -->
        <div id="dashboard" class="hidden fade-in" style="position: relative; z-index: 1;">
            
            <!-- Asset Info Card -->
            <div class="glass-card rounded-3xl p-8 mb-8">
                <div class="flex items-center justify-between">
                    <div>
                        <div class="text-4xl font-bold mb-2" style="color: var(--text-primary);" id="selectedAssetName">--</div>
                        <div class="text-lg" style="color: var(--text-secondary);" id="selectedAssetSymbol">--</div>
                    </div>
                    <div class="text-right">
                        <div class="flex items-center justify-end text-sm mb-2" style="color: var(--text-secondary);">
                            <span class="live-indicator"></span> Live Price
                        </div>
                        <div id="priceDisplay" class="text-5xl font-bold glow-text" style="color: var(--accent-cyan);">$--</div>
                        <div id="priceChange" class="text-lg font-semibold mt-2">--</div>
                    </div>
                </div>
            </div>

            <!-- Stats Grid -->
            <div class="grid grid-cols-1 md:grid-cols-5 gap-6 mb-8">
                <div class="glass-card rounded-2xl p-8 text-center stat-card">
                    <h3 class="text-sm uppercase tracking-wider mb-3" style="color: var(--text-secondary);">24h High</h3>
                    <p id="high24h" class="text-3xl font-bold" style="color: var(--accent-green);">--</p>
                </div>
                
                <div class="glass-card rounded-2xl p-8 text-center stat-card">
                    <h3 class="text-sm uppercase tracking-wider mb-3" style="color: var(--text-secondary);">24h Low</h3>
                    <p id="low24h" class="text-3xl font-bold" style="color: var(--accent-red);">--</p>
                </div>

                <div class="glass-card rounded-2xl p-8 text-center stat-card">
                    <h3 class="text-sm uppercase tracking-wider mb-3" style="color: var(--text-secondary);">AI Prediction (7D)</h3>
                    <p id="prediction" class="text-3xl font-bold" style="color: var(--accent-purple);">--</p>
                </div>

                <div class="glass-card rounded-2xl p-8 text-center stat-card">
                    <h3 class="text-sm uppercase tracking-wider mb-3" style="color: var(--text-secondary);">Trading Signal</h3>
                    <p id="signalBadge" class="text-3xl font-bold">--</p>
                    <p id="signalReason" class="text-sm mt-2" style="color: var(--text-secondary);">--</p>
                </div>

                <!-- Fear & Greed Index -->
                <div class="glass-card rounded-2xl p-8 text-center stat-card">
                    <h3 class="text-sm uppercase tracking-wider mb-3" style="color: var(--text-secondary);">Fear & Greed</h3>
                    <div id="fearGreedValue" class="text-3xl font-bold">--</div>
                    <div id="fearGreedLabel" class="text-sm mt-2" style="color: var(--text-secondary);">Loading...</div>
                </div>
            </div>

            <!-- Timeframe Selector -->
            <div class="glass-card rounded-2xl p-6 mb-8 flex justify-center gap-4">
                <button class="timeframe-btn" onclick="changeTimeframe('1m')">1m</button>
                <button class="timeframe-btn" onclick="changeTimeframe('5m')">5m</button>
                <button class="timeframe-btn active" onclick="changeTimeframe('1d')">1D</button>
                <button class="timeframe-btn" onclick="changeTimeframe('1w')">1W</button>
                <button class="timeframe-btn" onclick="changeTimeframe('1m_month')">1M</button>
            </div>

            <!-- Chart with Type Selector -->
            <div class="glass-card rounded-3xl p-8 mb-8">
                <div class="flex justify-between items-center mb-6">
                    <h3 class="text-2xl font-bold" style="color: var(--text-secondary);">📊 Professional Price Chart</h3>
                    <div class="flex gap-2">
                        <button class="timeframe-btn active" id="chartType-line" onclick="changeChartType('line')">📈 Line</button>
                        <button class="timeframe-btn" id="chartType-area" onclick="changeChartType('area')">🌊 Area</button>
                    </div>
                </div>
                <div id="chart-container"></div>
            </div>

            <!-- Technical Indicators Chart -->
            <div class="glass-card rounded-3xl p-8 mb-8">
                <div class="flex justify-between items-center mb-6">
                    <h3 class="text-2xl font-bold" style="color: var(--text-secondary);">📈 Technical Indicators</h3>
                    <div class="flex gap-2">
                        <button class="lang-toggle active" id="lang-en" onclick="changeIndicatorLang('en')">English</button>
                        <button class="lang-toggle" id="lang-fa" onclick="changeIndicatorLang('fa')">فارسی</button>
                    </div>
                </div>
                
                <!-- Indicator Badges -->
                <div class="flex flex-wrap gap-2 mb-6" id="indicatorBadges">
                    <span class="indicator-badge indicator-neutral">Loading...</span>
                </div>
                
                <!-- RSI Chart -->
                <div class="mb-6">
                    <h4 class="text-lg font-bold mb-3" style="color: var(--accent-purple);" id="rsiTitle">RSI (Relative Strength Index)</h4>
                    <div id="rsi-container" class="glass-card p-4">
                        <div id="rsi-chart" style="height: 200px;"></div>
                    </div>
                </div>
                
                <!-- AI Trading Assistant -->
                <div class="ai-panel">
                    <div class="ai-panel-title" id="aiTitle">🤖 AI Trading Assistant Analysis</div>
                    <div id="aiAnalysis" class="text-sm" style="color: var(--text-primary); line-height: 1.6;">
                        Select an asset to see AI analysis...
                    </div>
                </div>
            </div>

            <!-- Trading Tools Tabs -->
            <div class="glass-card rounded-3xl p-8 mb-8">
                <h3 class="text-2xl font-bold mb-6" style="color: var(--text-secondary);">🛠️ Trading Tools</h3>
                
                <!-- Tab Buttons -->
                <div class="flex gap-2 mb-6 border-b border-gray-700">
                    <button class="tab-btn active" onclick="switchTab('portfolio')">💼 Portfolio</button>
                    <button class="tab-btn" onclick="switchTab('calculator')"> Calculator</button>
                    <button class="tab-btn" onclick="switchTab('tpsl')"> TP/SL</button>
                    <button class="tab-btn" onclick="switchTab('alerts')"> Alerts</button>
                </div>

                <!-- Portfolio Tab -->
                <div id="tab-portfolio" class="tab-content active">
                    <div class="flex justify-between items-center mb-4">
                        <h4 class="text-xl font-bold" style="color: var(--text-primary);">My Portfolio</h4>
                        <button onclick="showPortfolioModal()" class="timeframe-btn active">+ Add Asset</button>
                    </div>
                    
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                        <div class="glass-card p-4 text-center">
                            <div class="text-sm" style="color: var(--text-secondary);">Total Value</div>
                            <div id="portfolioTotal" class="text-2xl font-bold" style="color: var(--accent-cyan);">$0.00</div>
                        </div>
                        <div class="glass-card p-4 text-center">
                            <div class="text-sm" style="color: var(--text-secondary);">Total Profit/Loss</div>
                            <div id="portfolioPnL" class="text-2xl font-bold">$0.00</div>
                        </div>
                        <div class="glass-card p-4 text-center">
                            <div class="text-sm" style="color: var(--text-secondary);">P&L Percentage</div>
                            <div id="portfolioPnLPercent" class="text-2xl font-bold">0.00%</div>
                        </div>
                    </div>
                    
                    <div style="overflow-x: auto;">
                        <table class="portfolio-table">
                            <thead>
                                <tr>
                                    <th>Asset</th>
                                    <th>Amount</th>
                                    <th>Avg Buy Price</th>
                                    <th>Current Price</th>
                                    <th>Value</th>
                                    <th>P&L</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody id="portfolioTableBody">
                                <tr>
                                    <td colspan="7" class="text-center py-8" style="color: var(--text-secondary);">
                                        No assets in portfolio. Click "+ Add Asset" to start!
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Calculator Tab -->
                <div id="tab-calculator" class="tab-content">
                    <h4 class="text-xl font-bold mb-4" style="color: var(--text-primary);"> Trading Calculator</h4>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label class="block text-sm mb-2" style="color: var(--text-secondary);">Investment Amount ($)</label>
                            <input type="number" id="calcInvestment" class="calc-input" placeholder="1000" oninput="calculateTrade()">
                            
                            <label class="block text-sm mb-2 mt-4" style="color: var(--text-secondary);">Entry Price ($)</label>
                            <input type="number" id="calcEntry" class="calc-input" placeholder="80000" oninput="calculateTrade()">
                            
                            <label class="block text-sm mb-2 mt-4" style="color: var(--text-secondary);">Exit Price ($)</label>
                            <input type="number" id="calcExit" class="calc-input" placeholder="85000" oninput="calculateTrade()">
                            
                            <label class="block text-sm mb-2 mt-4" style="color: var(--text-secondary);">Fee Percentage (%)</label>
                            <input type="number" id="calcFee" class="calc-input" placeholder="0.1" value="0.1" step="0.01" oninput="calculateTrade()">
                        </div>
                        <div>
                            <div class="calc-result">
                                <div class="calc-result-label">Position Size</div>
                                <div id="calcPosition" class="calc-result-value" style="color: var(--accent-cyan);">0.00000000</div>
                            </div>
                            <div class="calc-result">
                                <div class="calc-result-label">Profit / Loss</div>
                                <div id="calcPnL" class="calc-result-value">$0.00</div>
                            </div>
                            <div class="calc-result">
                                <div class="calc-result-label">P&L Percentage</div>
                                <div id="calcPnLPercent" class="calc-result-value">0.00%</div>
                            </div>
                            <div class="calc-result">
                                <div class="calc-result-label">Total Fees</div>
                                <div id="calcFees" class="calc-result-value" style="color: var(--accent-orange);">$0.00</div>
                            </div>
                            <div class="calc-result">
                                <div class="calc-result-label">Net Profit</div>
                                <div id="calcNetProfit" class="calc-result-value">$0.00</div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- TP/SL Tab -->
                <div id="tab-tpsl" class="tab-content">
                    <h4 class="text-xl font-bold mb-4" style="color: var(--text-primary);">🎯 Take Profit / Stop Loss Calculator</h4>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label class="block text-sm mb-2" style="color: var(--text-secondary);">Entry Price ($)</label>
                            <input type="number" id="tpslEntry" class="calc-input" placeholder="80000" oninput="calculateTPSL()">
                            
                            <label class="block text-sm mb-2 mt-4" style="color: var(--text-secondary);">Risk Percentage (%)</label>
                            <input type="number" id="tpslRisk" class="calc-input" placeholder="2" value="2" step="0.1" oninput="calculateTPSL()">
                            
                            <label class="block text-sm mb-2 mt-4" style="color: var(--text-secondary);">Reward:Risk Ratio</label>
                            <input type="number" id="tpslRR" class="calc-input" placeholder="2" value="2" step="0.1" oninput="calculateTPSL()">
                            
                            <label class="block text-sm mb-2 mt-4" style="color: var(--text-secondary);">Trade Direction</label>
                            <select id="tpslDirection" class="calc-input" onchange="calculateTPSL()">
                                <option value="long">Long (Buy) 📈</option>
                                <option value="short">Short (Sell) </option>
                            </select>
                        </div>
                        <div>
                            <div class="calc-result">
                                <div class="calc-result-label">Stop Loss</div>
                                <div id="tpslSL" class="calc-result-value" style="color: var(--accent-red);">$0.00</div>
                            </div>
                            <div class="calc-result">
                                <div class="calc-result-label">Take Profit</div>
                                <div id="tpslTP" class="calc-result-value" style="color: var(--accent-green);">$0.00</div>
                            </div>
                            <div class="calc-result">
                                <div class="calc-result-label">Risk Amount</div>
                                <div id="tpslRiskAmount" class="calc-result-value" style="color: var(--accent-orange);">$0.00</div>
                            </div>
                            <div class="calc-result">
                                <div class="calc-result-label">Reward Amount</div>
                                <div id="tpslRewardAmount" class="calc-result-value" style="color: var(--accent-green);">$0.00</div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Alerts Tab -->
                <div id="tab-alerts" class="tab-content">
                    <div class="flex justify-between items-center mb-4">
                        <h4 class="text-xl font-bold" style="color: var(--text-primary);">🔔 Price Alerts</h4>
                        <button onclick="showAlertForm()" class="timeframe-btn active">+ Add Alert</button>
                    </div>
                    
                    <div id="alertForm" class="hidden mb-6 p-4" style="background: rgba(0, 255, 255, 0.05); border-radius: 12px;">
                        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                            <input type="text" id="alertAsset" placeholder="Asset (e.g., bitcoin)" class="calc-input">
                            <input type="number" id="alertPrice" placeholder="Target Price" class="calc-input">
                            <select id="alertCondition" class="calc-input">
                                <option value="above">Above ↑</option>
                                <option value="below">Below ↓</option>
                            </select>
                            <div class="flex gap-2">
                                <button onclick="addAlert()" class="timeframe-btn active" style="flex: 1;">Save</button>
                                <button onclick="hideAlertForm()" class="timeframe-btn">Cancel</button>
                            </div>
                        </div>
                    </div>
                    
                    <div id="alertsList"></div>
                </div>
            </div>

            <!-- Calendar Section -->
            <div class="glass-card rounded-3xl p-8 mb-8">
                <h3 class="text-2xl font-bold mb-6" style="color: var(--text-secondary);">📅 Global Events Calendar</h3>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    <div>
                        <h4 class="text-lg font-bold mb-3" style="color: var(--accent-cyan);"> Gregorian Calendar</h4>
                        <div id="gregorianCalendar" class="glass-card p-4"></div>
                    </div>
                    <div>
                        <h4 class="text-lg font-bold mb-3" style="color: var(--accent-cyan);">🇮🇷 Persian Calendar</h4>
                        <div id="persianCalendar" class="glass-card p-4"></div>
                    </div>
                </div>
                
                <div id="todayEvents" class="mb-6">
                    <h4 class="text-lg font-bold mb-3" style="color: var(--accent-cyan);">🔴 Today's Events</h4>
                    <div id="todayEventsList" class="grid grid-cols-1 md:grid-cols-2 gap-3"></div>
                </div>
                
                <h4 class="text-lg font-bold mb-3" style="color: var(--accent-cyan);">📆 Upcoming Events</h4>
                <div id="upcomingEventsList" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"></div>
            </div>

            <!-- News Feed -->
            <div class="glass-card rounded-3xl p-8 mb-8">
                <div class="flex justify-between items-center mb-6">
                    <h3 class="text-2xl font-bold" style="color: var(--text-secondary);"> Global News Feed</h3>
                    <div class="flex gap-2">
                        <button onclick="loadNews('en')" class="timeframe-btn active" id="btn-en">English</button>
                        <button onclick="loadNews('fa')" class="timeframe-btn" id="btn-fa">فارسی</button>
                    </div>
                </div>
                <div id="newsFeed" class="space-y-3"></div>
            </div>
        </div>
    </div>

    <!-- Portfolio Modal -->
    <div class="modal-overlay" id="portfolioModal">
        <div class="modal-content">
            <div class="flex justify-between items-center mb-6">
                <h3 class="text-2xl font-bold" style="color: var(--text-primary);">Add Asset to Portfolio</h3>
                <button onclick="hidePortfolioModal()" class="text-2xl" style="color: var(--text-secondary);">✕</button>
            </div>
            <div class="space-y-4">
                <div>
                    <label class="block text-sm mb-2" style="color: var(--text-secondary);">Asset</label>
                    <input type="text" id="portfolioAsset" class="calc-input" placeholder="e.g., bitcoin">
                </div>
                <div>
                    <label class="block text-sm mb-2" style="color: var(--text-secondary);">Amount</label>
                    <input type="number" id="portfolioAmount" class="calc-input" placeholder="e.g., 0.5" step="0.00000001">
                </div>
                <div>
                    <label class="block text-sm mb-2" style="color: var(--text-secondary);">Average Buy Price ($)</label>
                    <input type="number" id="portfolioBuyPrice" class="calc-input" placeholder="e.g., 75000" step="0.01">
                </div>
                <div class="flex gap-2 pt-4">
                    <button onclick="addPortfolioAsset()" class="timeframe-btn active" style="flex: 1;">Add to Portfolio</button>
                    <button onclick="hidePortfolioModal()" class="timeframe-btn">Cancel</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Chatbot -->
    <div class="chatbot-container">
        <div class="chatbot-window" id="chatbotWindow">
            <div class="chatbot-header">
                <div class="flex items-center justify-between">
                    <div>
                        <div class="font-bold" style="color: var(--text-primary);">🤖 Market Oracle AI</div>
                        <div class="text-xs" style="color: var(--text-secondary);">Online & Offline • Multilingual</div>
                    </div>
                    <button onclick="toggleChatbot()" class="hover:text-cyan-400" style="color: var(--text-primary);">✕</button>
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
        function createParticles() {
            const container = document.getElementById('particles');
            for (let i = 0; i < 50; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.width = Math.random() * 5 + 'px';
                particle.style.height = particle.style.width;
                particle.style.left = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 20 + 's';
                particle.style.animationDuration = (Math.random() * 20 + 10) + 's';
                container.appendChild(particle);
            }
        }
        createParticles();

        let chart = null;
        let rsiChart = null;
        let lineSeries = null;
        let areaSeries = null;
        let ma7Series = null;
        let ma25Series = null;
        let bollingerUpper = null;
        let bollingerLower = null;
        let rsiSeries = null;
        let predictionSeries = null;
        let currentAsset = null;
        let currentTimeframe = '1d';
        let currentChartType = 'line';
        let currentIndicatorLang = 'en';
        let priceUpdateInterval = null;
        let allAssets = [];
        let priceAlerts = JSON.parse(localStorage.getItem('priceAlerts') || '[]');
        let portfolio = JSON.parse(localStorage.getItem('portfolio') || '[]');
        let currentTheme = localStorage.getItem('theme') || 'dark';
        let lastChartData = null;
        let lastPredictions = null;
        let lastIndicators = null;

        const indicatorTranslations = {
            en: {
                rsiTitle: 'RSI (Relative Strength Index)',
                aiTitle: ' AI Trading Assistant Analysis',
                rsiOverbought: '⚠️ RSI ({rsi}) indicates OVERBOUGHT conditions. Consider taking profits or waiting for pullback.',
                rsiOversold: '✅ RSI ({rsi}) indicates OVERSOLD conditions. Potential buying opportunity.',
                rsiNeutral: '➡️ RSI ({rsi}) is in neutral zone. No extreme conditions.',
                maBullish: '📈 MA7 (${ma7}) is above MA25 (${ma25}), indicating an UPTREND.',
                maBearish: '📉 MA7 (${ma7}) is below MA25 (${ma25}), indicating a DOWNTREND.',
                prediction: '🔮 7-Day Prediction: ${price}',
                warning: '️ Risk Warning: Always do your own research. Past performance doesn\'t guarantee future results.',
                loading: 'Select an asset to see AI analysis...',
                noData: 'No indicators'
            },
            fa: {
                rsiTitle: 'RSI (شاخص قدرت نسبی)',
                aiTitle: '🤖 تحلیل دستیار هوشمند معاملات',
                rsiOverbought: '⚠️ RSI ({rsi}) نشان‌دهنده شرایط اشباع خرید است. در نظر بگیرید سود بگیرید یا منتظر اصلاح بمانید.',
                rsiOversold: '✅ RSI ({rsi}) نشان‌دهنده شرایط اشباع فروش است. فرصت خرید احتمالی.',
                rsiNeutral: '➡️ RSI ({rsi}) در منطقه خنثی است. شرایط افراطی وجود ندارد.',
                maBullish: '📈 MA7 (${ma7}) بالاتر از MA25 (${ma25}) است که نشان‌دهنده روند صعودی است.',
                maBearish: '📉 MA7 (${ma7}) پایین‌تر از MA25 (${ma25}) است که نشان‌دهنده روند نزولی است.',
                prediction: '🔮 پیش‌بینی ۷ روزه: ${price} دلار',
                warning: '️ هشدار ریسک: همیشه تحقیقات خودتان را انجام دهید. عملکرد گذشته تضمین‌کننده نتایج آینده نیست.',
                loading: 'یک دارایی انتخاب کنید تا تحلیل AI را ببینید...',
                noData: 'بدون اندیکاتور'
            }
        };

        if (currentTheme === 'light') {
            document.body.classList.add('light-mode');
            document.querySelector('.theme-toggle').innerText = '☀️';
        }

        window.onload = async () => {
            await loadAssets();
            loadCalendar();
            loadNews('en');
            loadFearGreedIndex();
            loadNewsTicker();
            renderAlerts();
            renderPortfolio();
            startAlertChecker();
            updatePortfolioPrices();
        };

        function toggleTheme() {
            document.body.classList.toggle('light-mode');
            const isLight = document.body.classList.contains('light-mode');
            currentTheme = isLight ? 'light' : 'dark';
            localStorage.setItem('theme', currentTheme);
            document.querySelector('.theme-toggle').innerText = isLight ? '☀️' : '';
            if (chart) updateChart(lastChartData || [], lastPredictions || [], lastIndicators || {});
        }

        function changeIndicatorLang(lang) {
            currentIndicatorLang = lang;
            document.getElementById('lang-en').classList.toggle('active', lang === 'en');
            document.getElementById('lang-fa').classList.toggle('active', lang === 'fa');
            
            const t = indicatorTranslations[lang];
            document.getElementById('rsiTitle').innerText = t.rsiTitle;
            document.getElementById('aiTitle').innerText = t.aiTitle;
            
            if (lastIndicators) {
                updateAIAnalysis({ signal: lastSignal || {}, indicators: lastIndicators, symbol: currentAsset || 'BTC' });
            }
        }

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
            
            document.getElementById('emptyState').classList.add('hidden');
            document.getElementById('dashboard').classList.remove('hidden');
            
            const asset = allAssets[assetId];
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
                    signalEl.className = `text-3xl font-bold signal-${data.signal.signal.toLowerCase()}`;
                    
                    lastChartData = data.chart_data;
                    lastPredictions = data.predictions;
                    lastIndicators = data.indicators || {};
                    lastSignal = data.signal;
                    
                    updateChart(data.chart_data, data.predictions, data.indicators || {});
                    updateRSIChart(data.indicators?.rsi || []);
                    updateIndicatorBadges(data.indicators || {});
                    updateAIAnalysis(data);
                }
            } catch (error) { console.error("Failed to load data:", error); }
        }

        function getTimeframeDays(timeframe) {
            const map = { '1m': 1, '5m': 1, '1d': 30, '1w': 90, '1m_month': 365 };
            return map[timeframe] || 30;
        }

        function changeChartType(type) {
            currentChartType = type;
            document.querySelectorAll('[id^="chartType-"]').forEach(btn => btn.classList.remove('active'));
            document.getElementById(`chartType-${type}`).classList.add('active');
            if (lastChartData) updateChart(lastChartData, lastPredictions || [], lastIndicators || {});
        }

        function updateChart(chartData, predictions, indicators) {
            const container = document.getElementById('chart-container');
            container.innerHTML = '';
            
            const isLight = document.body.classList.contains('light-mode');
            const gridColor = isLight ? 'rgba(0, 0, 0, 0.05)' : 'rgba(0, 255, 255, 0.1)';
            const textColor = isLight ? '#4a5568' : '#d1d4dc';
            
            chart = LightweightCharts.createChart(container, {
                width: container.clientWidth,
                height: 600,
                layout: { background: { color: 'transparent' }, textColor: textColor, fontSize: 12 },
                grid: { vertLines: { color: gridColor, style: 2 }, horzLines: { color: gridColor, style: 2 } },
                crosshair: { 
                    mode: LightweightCharts.CrosshairMode.Normal,
                    vertLine: { width: 1, color: 'rgba(0, 255, 255, 0.5)', style: 3, labelBackgroundColor: '#00ffff', labelVisible: true },
                    horzLine: { width: 1, color: 'rgba(0, 255, 255, 0.5)', style: 3, labelBackgroundColor: '#00ffff', labelVisible: true },
                },
                rightPriceScale: { borderColor: 'rgba(0, 255, 255, 0.3)', scaleMargins: { top: 0.1, bottom: 0.1 }, alignLabels: true },
                timeScale: { borderColor: 'rgba(0, 255, 255, 0.3)', timeVisible: true, secondsVisible: false, fixLeftEdge: true, fixRightEdge: true },
                handleScroll: { vertTouchDrag: false, mouseWheel: true, pressedMouseMove: true },
                handleScale: { axisPressedMouseMove: true, mouseWheel: true, pinch: true },
            });
            
            if (currentChartType === 'line') {
                lineSeries = chart.addLineSeries({ 
                    color: '#00ffff', lineWidth: 2,
                    priceLineVisible: true, lastValueVisible: true,
                    crosshairMarkerVisible: true, crosshairMarkerRadius: 6,
                    priceFormat: { type: 'price', precision: 2, minMove: 0.01 },
                });
                lineSeries.setData(chartData.map(d => ({ time: d.time, value: d.price })));
            } else if (currentChartType === 'area') {
                areaSeries = chart.addAreaSeries({
                    topColor: 'rgba(0, 255, 255, 0.4)',
                    bottomColor: 'rgba(0, 255, 255, 0.0)',
                    lineColor: '#00ffff', lineWidth: 2,
                    priceLineVisible: true, lastValueVisible: true,
                    crosshairMarkerVisible: true, crosshairMarkerRadius: 6,
                    priceFormat: { type: 'price', precision: 2, minMove: 0.01 },
                });
                areaSeries.setData(chartData.map(d => ({ time: d.time, value: d.price })));
            }
            
            // MA7
            if (indicators.ma7 && indicators.ma7.length > 0) {
                ma7Series = chart.addLineSeries({ 
                    color: '#ffa500', lineWidth: 1, title: 'MA7',
                    priceLineVisible: false, lastValueVisible: false,
                });
                ma7Series.setData(indicators.ma7);
            }
            
            // MA25
            if (indicators.ma25 && indicators.ma25.length > 0) {
                ma25Series = chart.addLineSeries({ 
                    color: '#ff00ff', lineWidth: 1, title: 'MA25',
                    priceLineVisible: false, lastValueVisible: false,
                });
                ma25Series.setData(indicators.ma25);
            }
            
            // Bollinger Bands
            if (indicators.bollinger_upper && indicators.bollinger_upper.length > 0) {
                bollingerUpper = chart.addLineSeries({ 
                    color: 'rgba(168, 85, 247, 0.5)', lineWidth: 1, lineStyle: 2,
                    priceLineVisible: false, lastValueVisible: false,
                });
                bollingerUpper.setData(indicators.bollinger_upper);
                
                bollingerLower = chart.addLineSeries({ 
                    color: 'rgba(168, 85, 247, 0.5)', lineWidth: 1, lineStyle: 2,
                    priceLineVisible: false, lastValueVisible: false,
                });
                bollingerLower.setData(indicators.bollinger_lower);
            }
            
            // Prediction
            if (predictions && predictions.length > 0) {
                predictionSeries = chart.addLineSeries({ 
                    color: '#ff00ff', lineWidth: 2, lineStyle: 2,
                    priceLineVisible: false, lastValueVisible: true,
                    priceFormat: { type: 'price', precision: 2, minMove: 0.01 },
                });
                predictionSeries.setData(predictions);
            }
            
            chart.timeScale().fitContent();
            
            window.addEventListener('resize', () => {
                if (chart) chart.applyOptions({ width: container.clientWidth });
            });
        }

        function updateRSIChart(rsiData) {
            const container = document.getElementById('rsi-chart');
            container.innerHTML = '';
            
            if (!rsiData || rsiData.length === 0) {
                container.innerHTML = '<div class="text-center py-8" style="color: var(--text-secondary);">No RSI data available</div>';
                return;
            }
            
            const isLight = document.body.classList.contains('light-mode');
            const gridColor = isLight ? 'rgba(0, 0, 0, 0.05)' : 'rgba(0, 255, 255, 0.1)';
            const textColor = isLight ? '#4a5568' : '#d1d4dc';
            
            rsiChart = LightweightCharts.createChart(container, {
                width: container.clientWidth,
                height: 200,
                layout: { background: { color: 'transparent' }, textColor: textColor, fontSize: 11 },
                grid: { vertLines: { color: gridColor }, horzLines: { color: gridColor } },
                rightPriceScale: { borderColor: 'rgba(168, 85, 247, 0.3)' },
                timeScale: { visible: false },
            });
            
            rsiSeries = rsiChart.addLineSeries({ 
                color: '#a855f7', lineWidth: 2,
                priceLineVisible: false, lastValueVisible: true,
                priceFormat: { type: 'price', precision: 2, minMove: 0.01 },
            });
            rsiSeries.setData(rsiData);
            
            // Overbought line (70)
            const overbought = rsiChart.addLineSeries({ 
                color: 'rgba(255, 71, 87, 0.5)', lineWidth: 1, lineStyle: 2,
                priceLineVisible: false, lastValueVisible: false,
            });
            overbought.setData(rsiData.map(d => ({ time: d.time, value: 70 })));
            
            // Oversold line (30)
            const oversold = rsiChart.addLineSeries({ 
                color: 'rgba(0, 255, 136, 0.5)', lineWidth: 1, lineStyle: 2,
                priceLineVisible: false, lastValueVisible: false,
            });
            oversold.setData(rsiData.map(d => ({ time: d.time, value: 30 })));
            
            rsiChart.timeScale().fitContent();
        }

        function updateIndicatorBadges(indicators) {
            const container = document.getElementById('indicatorBadges');
            const badges = [];
            
            if (indicators.rsi_current !== undefined) {
                const rsi = indicators.rsi_current;
                let status = 'neutral';
                if (rsi > 70) status = 'bearish';
                else if (rsi < 30) status = 'bullish';
                badges.push(`<span class="indicator-badge indicator-${status}">RSI: ${rsi.toFixed(1)}</span>`);
            }
            
            if (indicators.ma7_current !== undefined && indicators.ma25_current !== undefined) {
                const ma7 = indicators.ma7_current;
                const ma25 = indicators.ma25_current;
                const status = ma7 > ma25 ? 'bullish' : 'bearish';
                badges.push(`<span class="indicator-badge indicator-${status}">MA7 > MA25: ${status.toUpperCase()}</span>`);
            }
            
            if (indicators.bollinger_position) {
                const pos = indicators.bollinger_position;
                badges.push(`<span class="indicator-badge indicator-neutral">BB: ${pos}</span>`);
            }
            
            const t = indicatorTranslations[currentIndicatorLang];
            container.innerHTML = badges.length > 0 ? badges.join('') : `<span class="indicator-badge indicator-neutral">${t.noData}</span>`;
        }

        function updateAIAnalysis(data) {
            const container = document.getElementById('aiAnalysis');
            const signal = data.signal;
            const indicators = data.indicators || {};
            const t = indicatorTranslations[currentIndicatorLang];
            
            let analysis = `<strong>${data.symbol}:</strong><br><br>`;
            
            analysis += `<strong>🎯 Trading Signal:</strong> ${signal.signal} (Confidence: ${signal.confidence}%)<br>`;
            analysis += `<strong>💡 Reason:</strong> ${signal.reason_en}<br><br>`;
            
            if (indicators.rsi_current !== undefined) {
                const rsi = indicators.rsi_current;
                if (rsi > 70) analysis += t.rsiOverbought.replace('{rsi}', rsi.toFixed(1)) + '<br>';
                else if (rsi < 30) analysis += t.rsiOversold.replace('{rsi}', rsi.toFixed(1)) + '<br>';
                else analysis += t.rsiNeutral.replace('{rsi}', rsi.toFixed(1)) + '<br>';
            }
            
            if (indicators.ma7_current && indicators.ma25_current) {
                const ma7 = indicators.ma7_current;
                const ma25 = indicators.ma25_current;
                if (ma7 > ma25) analysis += t.maBullish.replace('${ma7}', ma7.toFixed(2)).replace('${ma25}', ma25.toFixed(2)) + '<br>';
                else analysis += t.maBearish.replace('${ma7}', ma7.toFixed(2)).replace('${ma25}', ma25.toFixed(2)) + '<br>';
            }
            
            analysis += `<br>${t.prediction.replace('${price}', data.predicted_price.toLocaleString())}<br>`;
            analysis += `<br>${t.warning}`;
            
            container.innerHTML = analysis;
        }

        function changeTimeframe(timeframe) {
            currentTimeframe = timeframe;
            document.querySelectorAll('.timeframe-btn').forEach(btn => {
                if (!btn.id.startsWith('chartType-')) btn.classList.remove('active');
            });
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
                            changeEl.className = 'text-lg font-semibold mt-2 price-up';
                        } else if (change < 0) {
                            changeEl.innerText = `▼ ${change}%`;
                            changeEl.className = 'text-lg font-semibold mt-2 price-down';
                        }
                        
                        checkAlerts(assetId, newPrice);
                        updatePortfolioPrices();
                    }
                } catch (error) { console.error("Failed to update price:", error); }
            }, 3000);
        }

        async function loadFearGreedIndex() {
            try {
                const response = await fetch('https://api.alternative.me/fng/?limit=1');
                const data = await response.json();
                if (data.data && data.data[0]) {
                    const value = parseInt(data.data[0].value);
                    const classification = data.data[0].value_classification;
                    
                    document.getElementById('fearGreedValue').innerText = value;
                    document.getElementById('fearGreedLabel').innerText = classification;
                    
                    const valueEl = document.getElementById('fearGreedValue');
                    if (value <= 25) valueEl.style.color = '#ff4757';
                    else if (value <= 45) valueEl.style.color = '#ff8800';
                    else if (value <= 55) valueEl.style.color = '#ffff00';
                    else if (value <= 75) valueEl.style.color = '#00ff88';
                    else valueEl.style.color = '#00ff88';
                }
            } catch (error) {
                console.error("Failed to load Fear & Greed:", error);
                document.getElementById('fearGreedValue').innerText = '--';
                document.getElementById('fearGreedLabel').innerText = 'Unavailable';
            }
        }

        async function loadNewsTicker() {
            try {
                const response = await fetch('/api/news?lang=en');
                const data = await response.json();
                if (data.status === 'success') {
                    const ticker = document.getElementById('newsTicker');
                    ticker.innerHTML = data.news.map(item => 
                        `<span class="news-ticker-item">${item.icon} <strong>${item.source}:</strong> ${item.title} | ${item.time}</span>`
                    ).join('');
                }
            } catch (error) { console.error("Failed to load news ticker:", error); }
        }

        function switchTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById(`tab-${tabName}`).classList.add('active');
            event.target.classList.add('active');
        }

        function showPortfolioModal() {
            document.getElementById('portfolioModal').classList.add('active');
            if (currentAsset) document.getElementById('portfolioAsset').value = currentAsset;
        }

        function hidePortfolioModal() {
            document.getElementById('portfolioModal').classList.remove('active');
        }

        function addPortfolioAsset() {
            const asset = document.getElementById('portfolioAsset').value.trim().toLowerCase();
            const amount = parseFloat(document.getElementById('portfolioAmount').value);
            const buyPrice = parseFloat(document.getElementById('portfolioBuyPrice').value);
            
            if (!asset || !amount || !buyPrice) { alert('Please fill in all fields!'); return; }
            
            const existingIndex = portfolio.findIndex(p => p.asset === asset);
            if (existingIndex >= 0) {
                const existing = portfolio[existingIndex];
                const totalAmount = existing.amount + amount;
                existing.avgBuyPrice = ((existing.avgBuyPrice * existing.amount) + (buyPrice * amount)) / totalAmount;
                existing.amount = totalAmount;
            } else {
                portfolio.push({ asset: asset, amount: amount, avgBuyPrice: buyPrice, addedAt: new Date().toISOString() });
            }
            
            localStorage.setItem('portfolio', JSON.stringify(portfolio));
            hidePortfolioModal();
            renderPortfolio();
            updatePortfolioPrices();
            
            document.getElementById('portfolioAsset').value = '';
            document.getElementById('portfolioAmount').value = '';
            document.getElementById('portfolioBuyPrice').value = '';
        }

        function removePortfolioAsset(index) {
            if (confirm('Remove this asset from portfolio?')) {
                portfolio.splice(index, 1);
                localStorage.setItem('portfolio', JSON.stringify(portfolio));
                renderPortfolio();
            }
        }

        function renderPortfolio() {
            const tbody = document.getElementById('portfolioTableBody');
            if (portfolio.length === 0) {
                tbody.innerHTML = '<tr><td colspan="7" class="text-center py-8" style="color: var(--text-secondary);">No assets in portfolio. Click "+ Add Asset" to start!</td></tr>';
                document.getElementById('portfolioTotal').innerText = '$0.00';
                document.getElementById('portfolioPnL').innerText = '$0.00';
                document.getElementById('portfolioPnLPercent').innerText = '0.00%';
                return;
            }
            
            tbody.innerHTML = portfolio.map((item, index) => `
                <tr>
                    <td><strong>${item.asset.toUpperCase()}</strong></td>
                    <td>${item.amount}</td>
                    <td>$${item.avgBuyPrice.toLocaleString()}</td>
                    <td id="currentPrice-${index}">Loading...</td>
                    <td id="value-${index}">--</td>
                    <td id="pnl-${index}">--</td>
                    <td><button onclick="removePortfolioAsset(${index})" class="timeframe-btn" style="padding: 4px 8px; font-size: 12px;">✕</button></td>
                </tr>
            `).join('');
        }

        async function updatePortfolioPrices() {
            let totalValue = 0;
            let totalCost = 0;
            
            for (let i = 0; i < portfolio.length; i++) {
                const item = portfolio[i];
                try {
                    const response = await fetch(`/api/price/${item.asset}`);
                    const data = await response.json();
                    if (data.status === 'success') {
                        const currentPrice = data.price;
                        const value = currentPrice * item.amount;
                        const cost = item.avgBuyPrice * item.amount;
                        const pnl = value - cost;
                        const pnlPercent = (pnl / cost) * 100;
                        
                        totalValue += value;
                        totalCost += cost;
                        
                        const priceCell = document.getElementById(`currentPrice-${i}`);
                        const valueCell = document.getElementById(`value-${i}`);
                        const pnlCell = document.getElementById(`pnl-${i}`);
                        
                        if (priceCell) priceCell.innerText = `$${currentPrice.toLocaleString()}`;
                        if (valueCell) valueCell.innerText = `$${value.toLocaleString(undefined, {maximumFractionDigits: 2})}`;
                        if (pnlCell) {
                            pnlCell.innerHTML = `<span class="${pnl >= 0 ? 'profit' : 'loss'}">${pnl >= 0 ? '+' : ''}$${pnl.toFixed(2)} (${pnlPercent.toFixed(2)}%)</span>`;
                        }
                    }
                } catch (error) { console.error(`Failed to update price for ${item.asset}:`, error); }
            }
            
            const totalPnL = totalValue - totalCost;
            const totalPnLPercent = totalCost > 0 ? (totalPnL / totalCost) * 100 : 0;
            
            document.getElementById('portfolioTotal').innerText = `$${totalValue.toLocaleString(undefined, {maximumFractionDigits: 2})}`;
            
            const pnlEl = document.getElementById('portfolioPnL');
            pnlEl.innerText = `${totalPnL >= 0 ? '+' : ''}$${totalPnL.toFixed(2)}`;
            pnlEl.className = `text-2xl font-bold ${totalPnL >= 0 ? 'profit' : 'loss'}`;
            
            const pnlPercentEl = document.getElementById('portfolioPnLPercent');
            pnlPercentEl.innerText = `${totalPnLPercent >= 0 ? '+' : ''}${totalPnLPercent.toFixed(2)}%`;
            pnlPercentEl.className = `text-2xl font-bold ${totalPnLPercent >= 0 ? 'profit' : 'loss'}`;
        }

        function calculateTrade() {
            const investment = parseFloat(document.getElementById('calcInvestment').value) || 0;
            const entry = parseFloat(document.getElementById('calcEntry').value) || 0;
            const exit = parseFloat(document.getElementById('calcExit').value) || 0;
            const feePercent = parseFloat(document.getElementById('calcFee').value) || 0;
            
            if (entry === 0) { document.getElementById('calcPosition').innerText = '0.00000000'; return; }
            
            const positionSize = investment / entry;
            const grossPnL = (exit - entry) * positionSize;
            const fees = (investment * feePercent / 100) * 2;
            const netPnL = grossPnL - fees;
            const pnlPercent = investment > 0 ? (netPnL / investment) * 100 : 0;
            
            document.getElementById('calcPosition').innerText = positionSize.toFixed(8);
            
            const pnlEl = document.getElementById('calcPnL');
            pnlEl.innerText = `${grossPnL >= 0 ? '+' : ''}$${grossPnL.toFixed(2)}`;
            pnlEl.style.color = grossPnL >= 0 ? 'var(--accent-green)' : 'var(--accent-red)';
            
            const pnlPercentEl = document.getElementById('calcPnLPercent');
            pnlPercentEl.innerText = `${pnlPercent >= 0 ? '+' : ''}${pnlPercent.toFixed(2)}%`;
            pnlPercentEl.style.color = pnlPercent >= 0 ? 'var(--accent-green)' : 'var(--accent-red)';
            
            document.getElementById('calcFees').innerText = `$${fees.toFixed(2)}`;
            
            const netEl = document.getElementById('calcNetProfit');
            netEl.innerText = `${netPnL >= 0 ? '+' : ''}$${netPnL.toFixed(2)}`;
            netEl.style.color = netPnL >= 0 ? 'var(--accent-green)' : 'var(--accent-red)';
        }

        function calculateTPSL() {
            const entry = parseFloat(document.getElementById('tpslEntry').value) || 0;
            const riskPercent = parseFloat(document.getElementById('tpslRisk').value) || 0;
            const rrRatio = parseFloat(document.getElementById('tpslRR').value) || 0;
            const direction = document.getElementById('tpslDirection').value;
            
            if (entry === 0) return;
            
            const riskAmount = entry * (riskPercent / 100);
            const rewardAmount = riskAmount * rrRatio;
            
            let sl, tp;
            if (direction === 'long') { sl = entry - riskAmount; tp = entry + rewardAmount; }
            else { sl = entry + riskAmount; tp = entry - rewardAmount; }
            
            document.getElementById('tpslSL').innerText = `$${sl.toFixed(2)}`;
            document.getElementById('tpslTP').innerText = `$${tp.toFixed(2)}`;
            document.getElementById('tpslRiskAmount').innerText = `$${riskAmount.toFixed(2)}`;
            document.getElementById('tpslRewardAmount').innerText = `$${rewardAmount.toFixed(2)}`;
        }

        function showAlertForm() {
            document.getElementById('alertForm').classList.remove('hidden');
            if (currentAsset) document.getElementById('alertAsset').value = currentAsset;
        }

        function hideAlertForm() {
            document.getElementById('alertForm').classList.add('hidden');
        }

        function addAlert() {
            const asset = document.getElementById('alertAsset').value.trim().toLowerCase();
            const price = parseFloat(document.getElementById('alertPrice').value);
            const condition = document.getElementById('alertCondition').value;
            
            if (!asset || !price) { alert('Please fill in all fields!'); return; }
            
            const alert = { id: Date.now(), asset: asset, price: price, condition: condition, triggered: false, createdAt: new Date().toISOString() };
            priceAlerts.push(alert);
            localStorage.setItem('priceAlerts', JSON.stringify(priceAlerts));
            hideAlertForm();
            renderAlerts();
            
            if ('Notification' in window && Notification.permission === 'default') Notification.requestPermission();
        }

        function removeAlert(id) {
            priceAlerts = priceAlerts.filter(a => a.id !== id);
            localStorage.setItem('priceAlerts', JSON.stringify(priceAlerts));
            renderAlerts();
        }

        function renderAlerts() {
            const container = document.getElementById('alertsList');
            if (priceAlerts.length === 0) {
                container.innerHTML = '<div class="text-center py-8" style="color: var(--text-secondary);">No alerts yet. Click "+ Add Alert" to create one!</div>';
                return;
            }
            
            container.innerHTML = priceAlerts.map(alert => `
                <div class="alert-item ${alert.triggered ? 'triggered' : ''}">
                    <div>
                        <div class="font-bold" style="color: var(--text-primary);">${alert.asset.toUpperCase()}</div>
                        <div class="text-sm" style="color: var(--text-secondary);">${alert.condition === 'above' ? '↑ Above' : '↓ Below'} $${alert.price.toLocaleString()}</div>
                        ${alert.triggered ? '<div class="text-xs" style="color: var(--accent-green);">✅ Triggered!</div>' : ''}
                    </div>
                    <button onclick="removeAlert(${alert.id})" class="timeframe-btn" style="padding: 6px 12px; font-size: 12px;">✕</button>
                </div>
            `).join('');
        }

        async function checkAlerts(assetId, currentPrice) {
            let changed = false;
            priceAlerts.forEach(alert => {
                if (alert.triggered) return;
                if (alert.asset.toLowerCase() !== assetId.toLowerCase()) return;
                
                const triggered = alert.condition === 'above' ? currentPrice >= alert.price : currentPrice <= alert.price;
                
                if (triggered) {
                    alert.triggered = true;
                    changed = true;
                    
                    if ('Notification' in window && Notification.permission === 'granted') {
                        new Notification(`🔔 Price Alert: ${alert.asset.toUpperCase()}`, {
                            body: `Price is now ${alert.condition} $${alert.price}!\nCurrent: $${currentPrice}`, icon: '🔔'
                        });
                    }
                    
                    alert(`🔔 Price Alert Triggered!\n\n${alert.asset.toUpperCase()} is now ${alert.condition} $${alert.price}\nCurrent price: $${currentPrice}`);
                }
            });
            
            if (changed) {
                localStorage.setItem('priceAlerts', JSON.stringify(priceAlerts));
                renderAlerts();
            }
        }

        function startAlertChecker() {
            setInterval(async () => {
                if (!currentAsset) return;
                try {
                    const response = await fetch(`/api/price/${currentAsset}`);
                    const data = await response.json();
                    if (data.status === 'success') checkAlerts(currentAsset, data.price);
                } catch (error) {}
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
                <div class="text-center mb-4"><div class="text-xl font-bold" style="color: var(--accent-cyan);">${cal.month_name} ${cal.year}</div></div>
                <div class="grid grid-cols-7 gap-1">
                    ${['S','M','T','W','T','F','S'].map(d => `<div class="text-xs text-center" style="color: var(--text-secondary);">${d}</div>`).join('')}
                    ${cal.days.map(d => `<div class="calendar-day ${d.is_today ? 'today' : ''} ${d.is_weekend ? 'weekend' : ''}">${d.day}</div>`).join('')}
                </div>`;
        }

        function renderPersianCalendar(cal) {
            const container = document.getElementById('persianCalendar');
            container.innerHTML = `
                <div class="text-center mb-4"><div class="text-xl font-bold" style="color: var(--accent-cyan);">${cal.month_name} ${cal.year}</div></div>
                <div class="grid grid-cols-7 gap-1">
                    ${['ش','ی','د','س','چ','پ','ج'].map(d => `<div class="text-xs text-center" style="color: var(--text-secondary);">${d}</div>`).join('')}
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
                        <div><div class="font-bold" style="color: var(--text-primary);">${event.name}</div><div class="text-sm" style="color: var(--text-secondary);">${event.name_fa || ''}</div></div>
                    </div>
                    <div class="text-xs mb-2" style="color: var(--text-secondary);">${event.description_fa || event.description}</div>
                    <div class="flex gap-2 flex-wrap">${event.markets.map(m => `<span class="text-xs px-2 py-1 rounded" style="background: rgba(255,255,255,0.1);">${m.toUpperCase()}</span>`).join('')}</div>
                    <div class="mt-2 text-xs font-bold" style="color: ${getImpactColor(event.impact)}">Impact: ${event.impact.toUpperCase()}</div>
                </div>`).join('');
        }

        function renderUpcomingEvents(events) {
            const container = document.getElementById('upcomingEventsList');
            if (events.length === 0) { container.innerHTML = '<div class="text-center py-8 col-span-3" style="color: var(--text-secondary);">No upcoming events</div>'; return; }
            container.innerHTML = events.map(event => `
                <div class="glass-card p-4 hover:scale-105 transition-transform" style="border-top: 3px solid ${getImpactColor(event.impact)}">
                    <div class="flex items-center justify-between mb-3">
                        <span class="text-4xl">${event.icon}</span>
                        <div class="text-right"><div class="text-xs" style="color: var(--text-secondary);">In</div><div class="text-lg font-bold" style="color: var(--accent-cyan);">${event.days_until} days</div></div>
                    </div>
                    <div class="font-bold mb-1" style="color: var(--text-primary);">${event.name}</div>
                    <div class="text-sm mb-2" style="color: var(--text-secondary);">${event.name_fa || ''}</div>
                    <div class="text-xs mb-3" style="color: var(--text-secondary);">${event.description_fa || event.description}</div>
                    <div class="flex gap-1 flex-wrap mb-2">${event.markets.map(m => `<span class="text-xs px-2 py-1 rounded" style="background: rgba(255,255,255,0.1);">${m.toUpperCase()}</span>`).join('')}</div>
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
                        <div><div class="font-bold" style="color: var(--text-primary);">${item.source}</div><div class="text-xs" style="color: var(--text-secondary);">${item.time}</div></div>
                    </div>
                    <div class="text-sm mb-2" style="color: var(--text-secondary);">${item.title}</div>
                    <div class="flex gap-2 flex-wrap">${item.markets.map(m => `<span class="text-xs px-2 py-1 rounded" style="background: rgba(255,255,255,0.1);">${m.toUpperCase()}</span>`).join('')}</div>
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
                messagesContainer.innerHTML += `<div class="chat-message bot">Connection error. Try again! </div>`;
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
        
        # Calculate technical indicators with accurate data
        prices = df['price'].values
        timestamps = [int(df.iloc[i]['date'].timestamp()) for i in range(len(df))]
        
        # MA7 - 7-period Moving Average
        ma7_data = []
        for i in range(6, len(prices)):
            ma7 = np.mean(prices[i-6:i+1])
            ma7_data.append({"time": timestamps[i], "value": round(ma7, 2)})
        
        # MA25 - 25-period Moving Average
        ma25_data = []
        for i in range(24, len(prices)):
            ma25 = np.mean(prices[i-24:i+1])
            ma25_data.append({"time": timestamps[i], "value": round(ma25, 2)})
        
        # RSI - 14-period Relative Strength Index
        rsi_data = []
        if len(prices) >= 15:
            for i in range(14, len(prices)):
                gains = []
                losses = []
                for j in range(1, 15):
                    change = prices[i-j+1] - prices[i-j]
                    if change > 0:
                        gains.append(change)
                    else:
                        losses.append(abs(change))
                
                avg_gain = np.mean(gains) if gains else 0
                avg_loss = np.mean(losses) if losses else 0.001
                rs = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + rs))
                rsi_data.append({"time": timestamps[i], "value": round(rsi, 2)})
        
        # Bollinger Bands - 20-period, 2 standard deviations
        bb_upper = []
        bb_lower = []
        if len(prices) >= 20:
            for i in range(19, len(prices)):
                window = prices[i-19:i+1]
                mean = np.mean(window)
                std = np.std(window)
                bb_upper.append({"time": timestamps[i], "value": round(mean + 2*std, 2)})
                bb_lower.append({"time": timestamps[i], "value": round(mean - 2*std, 2)})
        
        indicators = {
            "ma7": ma7_data,
            "ma25": ma25_data,
            "rsi": rsi_data,
            "bollinger_upper": bb_upper,
            "bollinger_lower": bb_lower,
            "rsi_current": rsi_data[-1]["value"] if rsi_data else None,
            "ma7_current": ma7_data[-1]["value"] if ma7_data else None,
            "ma25_current": ma25_data[-1]["value"] if ma25_data else None,
            "bollinger_position": "Middle" if bb_upper and bb_lower else None
        }
        
        # Determine Bollinger position
        if bb_upper and bb_lower and len(prices) > 0:
            current_price = prices[-1]
            upper = bb_upper[-1]["value"]
            lower = bb_lower[-1]["value"]
            if current_price > upper:
                indicators["bollinger_position"] = "Above Upper Band"
            elif current_price < lower:
                indicators["bollinger_position"] = "Below Lower Band"
            else:
                indicators["bollinger_position"] = "Between Bands"
        
        last_timestamp = int(df.iloc[-1]['date'].timestamp())
        prediction_data = [{"time": last_timestamp + (i + 1) * 86400, "value": round(pred, 2)} for i, pred in enumerate(predictions)]
        chart_data = [{"time": int(row['date'].timestamp()), "price": round(row['price'], 2)} for _, row in df.iterrows()]
        
        return {
            "status": "success", "symbol": symbol.upper(),
            "current_price": current_data.get("price", 0),
            "high_24h": float(df['price'].max()), "low_24h": float(df['price'].min()),
            "predicted_price": float(predictions[-1]),
            "chart_data": chart_data, "predictions": prediction_data,
            "signal": signal,
            "indicators": indicators
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
