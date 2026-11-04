"""
Multilingual AI Chatbot - English, Persian, and more
Works Online and Offline
"""
import re


class ChatBot:
    def __init__(self):
        self.responses = self._load_multilingual_responses()
    
    def _load_multilingual_responses(self):
        return [
            # Greetings
            {
                "patterns": ["hello", "hi", "hey", "سلام", "درود", "سلام علیکم", "صبح بخیر", "عصر بخیر", "good morning", "good evening"],
                "responses": {
                    "en": "Hello! I'm your Market Oracle Assistant. How can I help you today? 🤖",
                    "fa": "سلام! من دستیار بازار اوراکل هستم. چطور می‌تونم کمکتون کنم؟ 🤖"
                }
            },
            # Price queries
            {
                "patterns": ["price", "قیمت", "how much", "چقدر", "rate", "نرخ", "value", "ارزش", "cost", "هزینه"],
                "responses": {
                    "en": "You can check real-time prices on the dashboard. Select any asset from the search bar to see live prices updated every 3 seconds! 📊",
                    "fa": "می‌تونید قیمت‌های لحظه‌ای رو در داشبورد ببینید. هر دارایی رو از نوار جستجو انتخاب کنید تا قیمت‌های زنده هر ۳ ثانیه به‌روز شوند! 📊"
                }
            },
            # Buy/Sell
            {
                "patterns": ["buy", "sell", "خرید", "فروش", "should i buy", "should i sell", "time to buy", "time to sell", "بخرم", "بفروشم", "زمان خرید", "زمان فروش"],
                "responses": {
                    "en": "Check the 'Trading Signal' card on the dashboard. It shows BUY/SELL/HOLD signals with confidence percentage based on RSI and Moving Averages. Always do your own research! ⚠️",
                    "fa": "کارت 'سیگنال معاملاتی' رو در داشبورد بررسی کنید. سیگنال‌های خرید/فروش/صبر با درصد اطمینان بر اساس RSI و میانگین متحرک نشان داده می‌شود. همیشه تحقیق خودتان را انجام دهید! ⚠️"
                }
            },
            # Bitcoin
            {
                "patterns": ["bitcoin", "btc", "بیت کوین", "بیت‌کوین", "بیت کوین"],
                "responses": {
                    "en": "Bitcoin (BTC) is the world's first cryptocurrency, created by Satoshi Nakamoto in 2009. It has a maximum supply of 21 million coins. Select it from the search bar to see live price, predictions, and technical analysis! ₿",
                    "fa": "بیت‌کوین (BTC) اولین ارز دیجیتال جهان است که توسط ساتوشی ناکاموتو در سال ۲۰۰۹ ساخته شد. حداکثر عرضه آن ۲۱ میلیون کوین است. از نوار جستجو انتخاب کنید تا قیمت زنده، پیش‌بینی‌ها و تحلیل تکنیکال را ببینید! ₿"
                }
            },
            # Ethereum
            {
                "patterns": ["ethereum", "eth", "اتریوم"],
                "responses": {
                    "en": "Ethereum (ETH) is the second-largest cryptocurrency. It powers smart contracts, DeFi, and NFTs. The network is transitioning to proof-of-stake for better energy efficiency. Check its live price on the dashboard! Ξ",
                    "fa": "اتریوم (ETH) دومین ارز دیجیتال بزرگ است. قراردادهای هوشمند، DeFi و NFTها را پشتیبانی می‌کند. شبکه در حال انتقال به proof-of-stake برای کارایی بهتر انرژی است. قیمت زنده آن را در داشبورد ببینید! Ξ"
                }
            },
            # Gold
            {
                "patterns": ["gold", "طلا", "xau", "silver", "نقره"],
                "responses": {
                    "en": "Gold (XAU) is a safe-haven asset. Its price is influenced by inflation, geopolitical tensions, dollar strength, and central bank policies. During uncertain times, gold typically rises. Check live prices on the dashboard! 🥇",
                    "fa": "طلا (XAU) یک دارایی امن است. قیمت آن تحت تأثیر تورم، تنش‌های ژئوپلیتیک، قدرت دلار و سیاست‌های بانک مرکزی است. در زمان‌های عدم اطمینان، طلا معمولاً افزایش می‌یابد. قیمت‌های زنده را در داشبورد ببینید! 🥇"
                }
            },
            # Prediction
            {
                "patterns": ["predict", "forecast", "پیش بینی", "future price", "قیمت آینده", "where will it go", "کجا میره"],
                "responses": {
                    "en": "Our AI predicts prices using Moving Average and RSI analysis. Check the 'AI Prediction' card and the purple dashed line on the chart for 7-day forecasts. Remember: predictions are not guarantees! 🔮",
                    "fa": "AI ما قیمت‌ها را با استفاده از تحلیل میانگین متحرک و RSI پیش‌بینی می‌کند. کارت 'پیش‌بینی AI' و خط نقطه‌چین بنفش روی نمودار را برای پیش‌بینی ۷ روزه بررسی کنید. به یاد داشته باشید: پیش‌بینی‌ها تضمین نیستند! 🔮"
                }
            },
            # Calendar
            {
                "patterns": ["calendar", "تقویم", "event", "رویداد", "holiday", "تعطیل"],
                "responses": {
                    "en": "Check the Global Events Calendar section! It shows both Gregorian and Persian (Shamsi) dates with market-impacting events like FOMC meetings, elections, and holidays. 📅",
                    "fa": "بخش تقویم رویدادهای جهانی را بررسی کنید! هم تاریخ میلادی و هم شمسی را با رویدادهای تأثیرگذار بر بازار مانند جلسات FOMC، انتخابات و تعطیلات نشان می‌دهد. 📅"
                }
            },
            # News
            {
                "patterns": ["news", "اخبار", "latest", "جدید", "what's happening", "چه خبر"],
                "responses": {
                    "en": "Check the News Feed section for latest updates from Elon Musk, Donald Trump, Federal Reserve, and major market events in both English and Persian! 📰",
                    "fa": "بخش اخبار را برای آخرین به‌روزرسانی‌ها از ایلان ماسک، دونالد ترامپ، فدرال رزرو و رویدادهای بزرگ بازار به هر دو زبان انگلیسی و فارسی بررسی کنید! 📰"
                }
            },
            # Help
            {
                "patterns": ["help", "کمک", "how to use", "راهنما", "guide", "راهنمایی"],
                "responses": {
                    "en": "Here's how to use the platform:\n1️⃣ Search any asset in the search bar\n2️⃣ Select timeframe (1m, 5m, 1D, 1W, 1M)\n3️⃣ Check live price (updates every 3s)\n4️⃣ View AI predictions and signals\n5️⃣ Read news and calendar events\n6️⃣ Ask me anything! 🤖",
                    "fa": "اینطور از پلتفرم استفاده کنید:\n1️⃣ هر دارایی را در نوار جستجو سرچ کنید\n2️⃣ تایم‌فریم را انتخاب کنید (1m, 5m, 1D, 1W, 1M)\n3️⃣ قیمت لحظه‌ای را بررسی کنید (هر 3 ثانیه به‌روز)\n4️⃣ پیش‌بینی‌ها و سیگنال‌های AI را ببینید\n5️⃣ اخبار و رویدادهای تقویم را بخوانید\n6️⃣ هر سوالی دارید از من بپرسید! 🤖"
                }
            },
            # Thanks
            {
                "patterns": ["thanks", "thank you", "ممنون", "مرسی", "تشکر", "سپاس", "متشکرم"],
                "responses": {
                    "en": "You're welcome! Happy trading! May your profits be endless! 🚀💰",
                    "fa": "خواهش می‌کنم! معامله موفق! امیدوارم سودهای بی‌پایان داشته باشید! 🚀💰"
                }
            },
            # Trump
            {
                "patterns": ["trump", "ترامپ"],
                "responses": {
                    "en": "Donald Trump's policies significantly impact markets. His tariff announcements, trade wars, and political statements can cause major volatility in forex, gold, and crypto markets. Check the News Feed for his latest statements! 🇺🇸",
                    "fa": "سیاست‌های دونالد ترامپ تأثیر قابل توجهی بر بازارها دارد. اعلام تعرفه‌ها، جنگ‌های تجاری و بیانیه‌های سیاسی او می‌تواند نوسان شدیدی در بازارهای فارکس، طلا و کریپتو ایجاد کند. آخرین بیانیه‌های او را در بخش اخبار ببینید! 🇺🇸"
                }
            },
            # Elon Musk
            {
                "patterns": ["elon", "musk", "ایلان", "ماسک"],
                "responses": {
                    "en": "Elon Musk's tweets can move crypto markets! He has influenced Bitcoin, Dogecoin, and Tesla stock prices with his social media posts. His support for crypto has been both praised and criticized. Check the News Feed for his latest posts! 🚀",
                    "fa": "توییت‌های ایلان ماسک می‌تواند بازارهای کریپتو را جابجا کند! او قیمت‌های بیت‌کوین، دوج‌کوین و سهام تسلا را با پست‌های شبکه اجتماعی خود تحت تأثیر قرار داده است. حمایت او از کریپتو هم ستایش و هم انتقاد شده است. آخرین پست‌های او را در اخبار ببینید! 🚀"
                }
            },
            # RSI
            {
                "patterns": ["rsi", "شاخص قدرت", "relative strength"],
                "responses": {
                    "en": "RSI (Relative Strength Index) is a momentum oscillator that measures the speed and magnitude of price changes. RSI above 70 indicates overbought (sell signal), below 30 indicates oversold (buy signal). It's shown on your dashboard! 📊",
                    "fa": "RSI (شاخص قدرت نسبی) یک نوسان‌نمای مومنتوم است که سرعت و بزرگی تغییرات قیمت را اندازه‌گیری می‌کند. RSI بالای ۷۰ نشان‌دهنده اشباع خرید (سیگنال فروش) و زیر ۳۰ نشان‌دهنده اشباع فروش (سیگنال خرید) است. در داشبورد شما نشان داده می‌شود! 📊"
                }
            },
            # Moving Average
            {
                "patterns": ["moving average", "ma", "میانگین متحرک"],
                "responses": {
                    "en": "Moving Averages (MA7, MA25) smooth out price data to identify trends. When MA7 crosses above MA25, it's a bullish signal (buy). When MA7 crosses below MA25, it's bearish (sell). These are calculated for your selected asset! 📈",
                    "fa": "میانگین‌های متحرک (MA7, MA25) داده‌های قیمت را هموار می‌کنند تا روندها شناسایی شوند. وقتی MA7 از بالای MA25 عبور کند، سیگنال صعودی (خرید) است. وقتی MA7 از زیر MA25 عبور کند، نزولی (فروش) است. اینها برای دارایی انتخابی شما محاسبه می‌شوند! 📈"
                }
            },
            # What is crypto
            {
                "patterns": ["what is crypto", "cryptocurrency", "ارز دیجیتال", "کریپتو"],
                "responses": {
                    "en": "Cryptocurrency is a digital or virtual currency secured by cryptography. Bitcoin was the first, created in 2009. Today there are thousands of cryptocurrencies. They operate on blockchain technology, which is decentralized and transparent. 🌐",
                    "fa": "ارز دیجیتال یک ارز دیجیتال یا مجازی است که با رمزنگاری امن شده است. بیت‌کوین اولین بود که در سال ۲۰۰۹ ساخته شد. امروزه هزاران ارز دیجیتال وجود دارد. آنها بر فناوری بلاکچین کار می‌کنند که غیرمتمرکز و شفاف است. 🌐"
                }
            },
            # What is forex
            {
                "patterns": ["forex", "فارکس", "currency exchange", "تبادل ارز"],
                "responses": {
                    "en": "Forex (Foreign Exchange) is the global marketplace for trading national currencies. It's the largest financial market in the world, with over $6 trillion traded daily. Major pairs include EUR/USD, GBP/USD, USD/JPY. 💱",
                    "fa": "فارکس (Foreign Exchange) بازار جهانی معامله ارزهای ملی است. این بزرگترین بازار مالی جهان است با بیش از ۶ تریلیون دلار معامله روزانه. جفت‌ارزهای اصلی شامل EUR/USD، GBP/USD، USD/JPY هستند. 💱"
                }
            },
            # Inflation
            {
                "patterns": ["inflation", "تورم"],
                "responses": {
                    "en": "Inflation erodes purchasing power over time. Gold and cryptocurrencies like Bitcoin are often considered hedges against inflation. When inflation rises, central banks may raise interest rates, which can strengthen the currency but hurt stocks. 📊",
                    "fa": "تورم قدرت خرید را در طول زمان کاهش می‌دهد. طلا و ارزهای دیجیتالی مانند بیت‌کوین اغلب به عنوان پوشش در برابر تورم در نظر گرفته می‌شوند. وقتی تورم افزایش می‌یابد، بانک‌های مرکزی ممکن است نرخ بهره را افزایش دهند که می‌تواند ارز را تقویت کند اما به سهام آسیب برساند. 📊"
                }
            },
            # Default
            {
                "patterns": [],
                "responses": {
                    "en": "I'm not sure about that. Try asking about:\n• Prices (bitcoin, ethereum, gold)\n• Buy/Sell signals\n• Predictions\n• Calendar events\n• News\n• Or type 'help' for more options! 🤖",
                    "fa": "مطمئن نیستم. این موارد را امتحان کنید:\n• قیمت‌ها (بیت‌کوین، اتریوم، طلا)\n• سیگنال‌های خرید/فروش\n• پیش‌بینی‌ها\n• رویدادهای تقویم\n• اخبار\n• یا 'help' را تایپ کنید! 🤖"
                }
            }
        ]
    
    def detect_language(self, message: str) -> str:
        """Detect if message is Persian or English."""
        persian_chars = re.findall(r'[\u0600-\u06FF]', message)
        if len(persian_chars) > len(message) * 0.3:
            return "fa"
        return "en"
    
    def get_response(self, message: str) -> str:
        """Get response based on user message - multilingual."""
        message_lower = message.lower().strip()
        lang = self.detect_language(message)
        
        if not message_lower:
            return "Please type a message! 💬" if lang == "en" else "لطفاً پیامی تایپ کنید! 💬"
        
        # Check each category
        for category in self.responses:
            for pattern in category["patterns"]:
                if pattern and pattern in message_lower:
                    return category["responses"].get(lang, category["responses"]["en"])
        
        # Default response
        default = self.responses[-1]
        return default["responses"].get(lang, default["responses"]["en"])
