"""
Advanced Multilingual Chatbot with Memory
"""
import re
from datetime import datetime


class ChatBot:
    def __init__(self):
        self.name = "Market Oracle AI"
        self.creator = "Amirhossein Ahmadvand (امیرحسین احمدوند)"
        self.version = "4.0.0 Empire Edition"
        self.conversation_history = []
        
        # Knowledge bases
        self.capitals = {
            "iran": "Tehran (تهران)", "tehran": "Tehran (تهران) - Capital of Iran",
            "usa": "Washington D.C.", "united states": "Washington D.C.", "america": "Washington D.C.",
            "uk": "London", "england": "London", "france": "Paris", "germany": "Berlin",
            "italy": "Rome", "spain": "Madrid", "russia": "Moscow", "china": "Beijing",
            "japan": "Tokyo", "india": "New Delhi", "brazil": "Brasilia", "canada": "Ottawa",
            "australia": "Canberra", "egypt": "Cairo", "turkey": "Ankara", "saudi arabia": "Riyadh",
            "uae": "Abu Dhabi", "iraq": "Baghdad", "afghanistan": "Kabul", "pakistan": "Islamabad",
            "india": "New Delhi", "russia": "Moscow", "ukraine": "Kyiv", "poland": "Warsaw",
            "sweden": "Stockholm", "norway": "Oslo", "denmark": "Copenhagen", "finland": "Helsinki",
            "greece": "Athens", "portugal": "Lisbon", "netherlands": "Amsterdam", "belgium": "Brussels",
            "switzerland": "Bern", "austria": "Vienna", "czech republic": "Prague", "hungary": "Budapest",
            "romania": "Bucharest", "bulgaria": "Sofia", "serbia": "Belgrade", "croatia": "Zagreb",
            "south korea": "Seoul", "north korea": "Pyongyang", "vietnam": "Hanoi", "thailand": "Bangkok",
            "indonesia": "Jakarta", "malaysia": "Kuala Lumpur", "singapore": "Singapore",
            "philippines": "Manila", "mexico": "Mexico City", "argentina": "Buenos Aires",
            "chile": "Santiago", "colombia": "Bogota", "peru": "Lima", "venezuela": "Caracas",
            "south africa": "Pretoria", "nigeria": "Abuja", "kenya": "Nairobi", "morocco": "Rabat",
            "israel": "Jerusalem", "lebanon": "Beirut", "syria": "Damascus", "jordan": "Amman",
            "kuwait": "Kuwait City", "qatar": "Doha", "bahrain": "Manama", "oman": "Muscat",
            "yemen": "Sana'a", "libya": "Tripoli", "tunisia": "Tunis", "algeria": "Algiers",
            "sudan": "Khartoum", "ethiopia": "Addis Ababa", "ghana": "Accra", "senegal": "Dakar",
            "kazakhstan": "Astana", "uzbekistan": "Tashkent", "turkmenistan": "Ashgabat",
            "kyrgyzstan": "Bishkek", "tajikistan": "Dushanbe", "mongolia": "Ulaanbaatar",
            "nepal": "Kathmandu", "bhutan": "Thimphu", "sri lanka": "Sri Jayawardenepura Kotte",
            "bangladesh": "Dhaka", "myanmar": "Naypyidaw", "cambodia": "Phnom Penh",
            "laos": "Vientiane", "brunei": "Bandar Seri Begawan", "maldives": "Male",
            "fiji": "Suva", "new zealand": "Wellington", "papua new guinea": "Port Moresby",
            "cuba": "Havana", "jamaica": "Kingston", "haiti": "Port-au-Prince",
            "dominican republic": "Santo Domingo", "puerto rico": "San Juan",
            "costa rica": "San Jose", "panama": "Panama City", "guatemala": "Guatemala City",
            "honduras": "Tegucigalpa", "nicaragua": "Managua", "el salvador": "San Salvador",
            "belize": "Belmopan", "bahamas": "Nassau", "barbados": "Bridgetown",
            "trinidad and tobago": "Port of Spain", "guyana": "Georgetown", "suriname": "Paramaribo",
            "uruguay": "Montevideo", "paraguay": "Asuncion", "bolivia": "Sucre",
            "ecuador": "Quito", "peru": "Lima", "bolivia": "Sucre",
            "iran_fa": "تهران (Tehran)", "آمریکا": "Washington D.C.", "انگلیس": "London",
            "فرانسه": "Paris", "آلمان": "Berlin", "ایتالیا": "Rome", "اسپانیا": "Madrid",
            "روسیه": "Moscow", "چین": "Beijing", "ژاپن": "Tokyo", "هند": "New Delhi",
            "ترکیه": "Ankara", "عربستان": "Riyadh", "امارات": "Abu Dhabi", "عراق": "Baghdad",
            "افغانستان": "Kabul", "پاکستان": "Islamabad", "مصر": "Cairo", "سوریه": "Damascus",
            "لبنان": "Beirut", "اردن": "Amman", "کویت": "Kuwait City", "قطر": "Doha",
            "بحرین": "Manama", "عمان": "Muscat", "یمن": "Sana'a", "لیبی": "Tripoli",
            "تونس": "Tunis", "الجزایر": "Algiers", "مراکش": "Rabat", "سودان": "Khartoum",
            "اتیوپی": "Addis Ababa", "نیجریه": "Abuja", "کنیا": "Nairobi",
            "کره جنوبی": "Seoul", "کره شمالی": "Pyongyang", "ویتنام": "Hanoi",
            "تایلند": "Bangkok", "اندونزی": "Jakarta", "مالزی": "Kuala Lumpur",
            "سنگاپور": "Singapore", "فیلیپین": "Manila", "مکزیک": "Mexico City",
            "آرژانتین": "Buenos Aires", "شیلی": "Santiago", "کلمبیا": "Bogota",
            "برزیل": "Brasilia", "کانادا": "Ottawa", "استرالیا": "Canberra",
            "نیوزیلند": "Wellington", "آفریقای جنوبی": "Pretoria",
            "اوکراین": "Kyiv", "لهستان": "Warsaw", "سوئد": "Stockholm",
            "نروژ": "Oslo", "دانمارک": "Copenhagen", "فنلاند": "Helsinki",
            "یونان": "Athens", "پرتغال": "Lisbon", "هلند": "Amsterdam",
            "بلژیک": "Brussels", "سوئیس": "Bern", "اتریش": "Vienna",
            "چک": "Prague", "مجارستان": "Budapest", "رومانی": "Bucharest",
            "بلغارستان": "Sofia", "صربستان": "Belgrade", "کرواسی": "Zagreb",
            "قزاقستان": "Astana", "ازبکستان": "Tashkent", "ترکمنستان": "Ashgabat",
            "قرقیزستان": "Bishkek", "تاجیکستان": "Dushanbe", "مغولستان": "Ulaanbaatar",
            "نپال": "Kathmandu", "بوتان": "Thimphu", "سری لانکا": "Sri Jayawardenepura Kotte",
            "بنگلادش": "Dhaka", "میانمار": "Naypyidaw", "کامبوج": "Phnom Penh",
            "لائوس": "Vientiane", "برونئی": "Bandar Seri Begawan", "مالدیو": "Male",
            "فیجی": "Suva", "کوبا": "Havana", "جامائیکا": "Kingston", "هائیتی": "Port-au-Prince",
            "دومینیکن": "Santo Domingo", "پورتوریکو": "San Juan", "کاستاریکا": "San Jose",
            "پاناما": "Panama City", "گواتمالا": "Guatemala City", "هندوراس": "Tegucigalpa",
            "نیکاراگوئه": "Managua", "السالوادور": "San Salvador", "بلیز": "Belmopan",
            "باهاما": "Nassau", "باربادوس": "Bridgetown", "ترینیداد": "Port of Spain",
            "گویان": "Georgetown", "سورینام": "Paramaribo", "اروگوئه": "Montevideo",
            "پاراگوئه": "Asuncion", "بولیوی": "Sucre", "اکوادور": "Quito", "پرو": "Lima",
        }
        
        self.famous_people = {
            "napoleon": "Napoleon Bonaparte (1769-1821) - French military leader and emperor who conquered much of Europe. Famous for the Napoleonic Wars and his exile to Saint Helena.",
            "napoleon bonaparte": "Napoleon Bonaparte - French emperor and military genius. Born in Corsica, rose to power during the French Revolution. Defeated at Waterloo in 1815.",
            "ناپلئون": "ناپلئون بناپارت (۱۷۶۹-۱۸۲۱) - رهبر نظامی و امپراتور فرانسه که بخش بزرگی از اروپا را فتح کرد. در واترلو شکست خورد و به سنت هلن تبعید شد.",
            "marco rubio": "Marco Rubio - American politician, U.S. Senator from Florida. Known for foreign policy expertise and conservative views. Born 1971 in Miami.",
            "مارکو روبیو": "مارکو روبیو - سیاستمدار آمریکایی، سناتور ایالات متحده از فلوریدا. متخصص سیاست خارجی و دیدگاه‌های محافظه‌کارانه. متولد ۱۹۷۱ در میامی.",
            "elon musk": "Elon Musk - CEO of Tesla, SpaceX, and owner of X (Twitter). Born 1971 in South Africa. Known for electric vehicles, space exploration, and cryptocurrency influence.",
            "ایلان ماسک": "ایلان ماسک - مدیرعامل تسلا، اسپیس‌اکس و مالک X (توییتر). متولد ۱۹۷۱ در آفریقای جنوبی. معروف به خودروهای الکتریکی، اکتشافات فضایی و تأثیر بر کریپتوکارنسی.",
            "donald trump": "Donald Trump - 45th and 47th President of the United States. Businessman and politician. Known for 'America First' policy and impact on global markets.",
            "دونالد ترامپ": "دونالد ترامپ - چهل و پنجمین و چهل و هفتمین رئیس‌جمهور ایالات متحده. تاجر و سیاستمدار. معروف به سیاست 'آمریکا اول' و تأثیر بر بازارهای جهانی.",
            "joe biden": "Joe Biden - 46th President of the United States. Former Vice President under Obama. Known for infrastructure bills and foreign policy.",
            "جو بایدن": "جو بایدن - چهل و ششمین رئیس‌جمهور ایالات متحده. معاون سابق اوباما. معروف به قوانین زیرساخت و سیاست خارجی.",
            "vladimir putin": "Vladimir Putin - President of Russia since 2000. Former KGB officer. Known for strong leadership and impact on global geopolitics.",
            "ولادیمیر پوتین": "ولادیمیر پوتین - رئیس‌جمهور روسیه از سال ۲۰۰۰. افسر سابق KGB. معروف به رهبری قوی و تأثیر بر ژئوپلیتیک جهانی.",
            "xi jinping": "Xi Jinping - President of China since 2013. General Secretary of the Communist Party. Known for Belt and Road Initiative.",
            "شی جین پینگ": "شی جین پینگ - رئیس‌جمهور چین از سال ۲۰۱۳. دبیرکل حزب کمونیست. معروف به ابتکار کمربند و جاده.",
            "emmanuel macron": "Emmanuel Macron - President of France since 2017. Former investment banker. Known for pro-EU stance and economic reforms.",
            "امانوئل ماکرون": "امانوئل ماکرون - رئیس‌جمهور فرانسه از سال ۲۰۱۷. بانکدار سابق سرمایه‌گذاری. معروف به موضع طرفدار اتحادیه اروپا و اصلاحات اقتصادی.",
            "boris johnson": "Boris Johnson - Former UK Prime Minister (2019-2022). Led Brexit process. Known for charismatic leadership style.",
            "باریس جانسون": "باریس جانسون - نخست‌وزیر سابق بریتانیا (۲۰۱۹-۲۰۲۲). فرآیند برگزیت را رهبری کرد. معروف به سبک رهبری کاریزماتیک.",
            "angela merkel": "Angela Merkel - Former Chancellor of Germany (2005-2021). Known as 'leader of the free world' and steady leadership during crises.",
            "آنگلا مرکل": "آنگلا مرکل - صدراعظم سابق آلمان (۲۰۰۵-۲۰۲۱). معروف به 'رهبر جهان آزاد' و رهبری ثابت در بحران‌ها.",
            "satoshi nakamoto": "Satoshi Nakamoto - Pseudonymous creator of Bitcoin (2009). Identity unknown. Estimated to own ~1 million BTC.",
            "ساتوشی ناکاموتو": "ساتوشی ناکاموتو - خالق ناشناس بیت‌کوین (۲۰۰۹). هویت واقعی ناشناخته. تخمین زده می‌شود حدود ۱ میلیون BTC داشته باشد.",
            "vitalik buterin": "Vitalik Buterin - Co-founder of Ethereum (2015). Born 1994 in Russia. Known for smart contracts and blockchain innovation.",
            "ویتالیک بوترین": "ویتالیک بوترین - هم‌بنیانگذار اتریوم (۲۰۱۵). متولد ۱۹۹۴ در روسیه. معروف به قراردادهای هوشمند و نوآوری بلاکچین.",
            "jeff bezos": "Jeff Bezos - Founder of Amazon (1994). One of the world's richest people. Also owns Blue Origin space company and The Washington Post.",
            "جف بزوس": "جف بزوس - بنیانگذار آمازون (۱۹۹۴). یکی از ثروتمندترین افراد جهان. همچنین مالک شرکت فضایی Blue Origin و روزنامه Washington Post.",
            "bill gates": "Bill Gates - Co-founder of Microsoft (1975). Philanthropist through Bill & Melinda Gates Foundation. Focus on global health and education.",
            "بیل گیتس": "بیل گیتس - هم‌بنیانگذار مایکروسافت (۱۹۷۵). خیر از طریق بنیاد بیل و ملیندا گیتس. تمرکز بر سلامت جهانی و آموزش.",
            "steve jobs": "Steve Jobs (1955-2011) - Co-founder of Apple. Revolutionized personal computing, music, and mobile phones. Known for iPhone and iPad.",
            "استیو جابز": "استیو جابز (۱۹۵۵-۲۰۱۱) - هم‌بنیانگذار اپل. انقلاب در رایانش شخصی، موسیقی و تلفن‌های همراه. معروف به آیفون و آیپد.",
            "mark zuckerberg": "Mark Zuckerberg - Founder and CEO of Meta (Facebook). Born 1984. Known for social media and metaverse vision.",
            "مارک زاکربرگ": "مارک زاکربرگ - بنیانگذار و مدیرعامل متا (فیسبوک). متولد ۱۹۸۴. معروف به شبکه‌های اجتماعی و چشم‌انداز متاورس.",
            "tim cook": "Tim Cook - CEO of Apple since 2011. Succeeded Steve Jobs. Known for supply chain expertise and Apple's continued innovation.",
            "تیم کوک": "تیم کوک - مدیرعامل اپل از ۲۰۱۱. جانشین استیو جابز. معروف به تخصص زنجیره تأمین و نوآوری مستمر اپل.",
            "warren buffett": "Warren Buffett - 'Oracle of Omaha'. One of the most successful investors ever. CEO of Berkshire Hathaway. Known for value investing.",
            "وارن بافت": "وارن بافت - 'پیشگوی اوماها'. یکی از موفق‌ترین سرمایه‌گذاران تاریخ. مدیرعامل برکشایر هاتاوی. معروف به سرمایه‌گذاری ارزشی.",
            "jerome powell": "Jerome Powell - Chair of the Federal Reserve since 2018. Controls US monetary policy and interest rates. Major impact on global markets.",
            "جروم پاول": "جروم پاول - رئیس فدرال رزرو از ۲۰۱۸. کنترل سیاست پولی و نرخ بهره آمریکا. تأثیر بزرگ بر بازارهای جهانی.",
        }
        
        self.crypto_knowledge = {
            "bitcoin": "Bitcoin (BTC) - First cryptocurrency, created 2009 by Satoshi Nakamoto. Max supply: 21 million. Store of value, digital gold.",
            "ethereum": "Ethereum (ETH) - Smart contract platform, created 2015 by Vitalik Buterin. Powers DeFi, NFTs, dApps.",
            "dogecoin": "Dogecoin (DOGE) - Meme coin created 2013 as a joke. Gained popularity through Elon Musk's support.",
            "solana": "Solana (SOL) - High-speed blockchain, 65,000 TPS. Known for low fees and fast transactions.",
            "cardano": "Cardano (ADA) - Research-driven blockchain, founded by Charles Hoskinson. Focus on sustainability.",
            "ripple": "XRP - Digital payment protocol by Ripple Labs. Fast cross-border transactions.",
            "polkadot": "Polkadot (DOT) - Multi-chain protocol by Gavin Wood. Enables blockchain interoperability.",
            "litecoin": "Litecoin (LTC) - Created 2011 by Charlie Lee. 'Silver to Bitcoin's gold'. Faster transactions.",
            "bnb": "BNB - Binance's native token. Used for trading fee discounts and BSC ecosystem.",
            "avalanche": "Avalanche (AVAX) - High-throughput smart contract platform. Sub-second finality.",
            "chainlink": "Chainlink (LINK) - Decentralized oracle network. Connects smart contracts to real-world data.",
        }
        
        self.responses = self._load_responses()
    
    def _load_responses(self):
        return [
            {"patterns": ["hello", "hi", "hey", "سلام", "درود", "صبح بخیر", "عصر بخیر", "good morning", "good evening", "how are you", "چطوری", "حالت چطوره"],
             "responses": {"en": "Hello! I'm Market Oracle AI, your intelligent assistant. How can I help you today? 🤖",
                          "fa": "سلام! من Market Oracle AI هستم، دستیار هوشمند شما. چطور می‌تونم کمکتون کنم؟ 🤖"}},
            
            {"patterns": ["your name", "who are you", "what are you", "اسمت چیه", "کی هستی", "چی هستی", "نام تو", "نام شما"],
             "responses": {"en": f"I'm {self.name} v{self.version}, an AI-powered market analysis assistant created by {self.creator}. I help with crypto, forex, gold prices, predictions, and much more! 🤖",
                          "fa": f"من {self.name} نسخه {self.version} هستم، یک دستیار تحلیل بازار مبتنی بر AI که توسط {self.creator} ساخته شده‌ام. در کریپتو، فارکس، طلا، پیش‌بینی‌ها و خیلی چیزهای دیگر کمک می‌کنم! 🤖"}},
            
            {"patterns": ["creator", "who made you", "who created you", "your developer", "سازنده تو", "کی تو رو ساخته", "توسعه دهنده تو", "سازنده ات"],
             "responses": {"en": f"I was created by {self.creator}, a talented developer and AI engineer. He built me to be the most powerful market analysis platform in the world! 🚀",
                          "fa": f"من توسط {self.creator} ساخته شدم، یک توسعه‌دهنده و مهندس AI با استعداد. او من را ساخت تا قوی‌ترین پلتفرم تحلیل بازار در جهان باشم! 🚀"}},
            
            {"patterns": ["capital", "پایتخت", "capital of", "paytakht"],
             "responses": {"en": "I know all world capitals! Ask me about any country. For example: 'What is the capital of Iran?' or 'Capital of France?' 🌍",
                          "fa": "من همه پایتخت‌های جهان را می‌دانم! درباره هر کشوری بپرسید. مثلاً: 'پایتخت ایران چیست؟' یا 'پایتخت فرانسه؟' 🌍"}},
            
            {"patterns": ["who is", "who was", "tell me about", "معرفی کن", "کی بود", "کیه", "درباره"],
             "responses": {"en": "I know many famous people! Ask about politicians, entrepreneurs, historical figures, or crypto founders. Try: 'Who is Napoleon?' or 'Tell me about Elon Musk' 👤",
                          "fa": "من افراد مشهور زیادی را می‌شناسم! درباره سیاستمداران، کارآفرینان، شخصیت‌های تاریخی یا بنیانگذاران کریپتو بپرسید. امتحان کنید: 'ناپلئون کی بود؟' یا 'درباره ایلان ماسک' 👤"}},
            
            {"patterns": ["price", "قیمت", "how much", "چقدر", "rate", "نرخ"],
             "responses": {"en": "Check real-time prices on the dashboard! Select any asset from the search bar. Prices update every 3 seconds from Binance API! 📊",
                          "fa": "قیمت‌های لحظه‌ای را در داشبورد ببینید! هر دارایی را از نوار جستجو انتخاب کنید. قیمت‌ها هر ۳ ثانیه از API بایننس به‌روز می‌شوند! 📊"}},
            
            {"patterns": ["buy", "sell", "خرید", "فروش", "should i buy", "بخرم", "بفروشم"],
             "responses": {"en": "Check the 'Trading Signal' card! It shows BUY/SELL/HOLD based on RSI and Moving Averages with confidence percentage. Always do your own research! ⚠️",
                          "fa": "کارت 'سیگنال معاملاتی' را بررسی کنید! بر اساس RSI و میانگین متحرک با درصد اطمینان BUY/SELL/HOLD نشان می‌دهد. همیشه تحقیق خودتان را انجام دهید! ⚠️"}},
            
            {"patterns": ["bitcoin", "btc", "بیت کوین", "بیت‌کوین"],
             "responses": {"en": self.crypto_knowledge["bitcoin"], "fa": "بیت‌کوین (BTC) - اولین ارز دیجیتال، ساخته ۲۰۰۹ توسط ساتوشی ناکاموتو. حداکثر عرضه: ۲۱ میلیون. ذخیره ارزش، طلای دیجیتال."}},
            
            {"patterns": ["ethereum", "eth", "اتریوم"],
             "responses": {"en": self.crypto_knowledge["ethereum"], "fa": "اتریوم (ETH) - پلتفرم قرارداد هوشمند، ساخته ۲۰۱۵ توسط ویتالیک بوترین. پشتیبان DeFi، NFTها، dAppها."}},
            
            {"patterns": ["gold", "طلا"],
             "responses": {"en": "Gold (XAU) - Safe-haven asset. Price influenced by inflation, geopolitics, dollar strength. Check live price on dashboard! 🥇",
                          "fa": "طلا (XAU) - دارایی امن. قیمت تحت تأثیر تورم، ژئوپلیتیک، قدرت دلار. قیمت زنده در داشبورد! 🥇"}},
            
            {"patterns": ["help", "کمک", "راهنما", "guide"],
             "responses": {"en": "I can help with:\n📊 Market prices & predictions\n🌍 World capitals & geography\n👤 Famous people & history\n💰 Crypto & forex info\n📅 Calendar events\n📰 Global news\nJust ask! 🤖",
                          "fa": "می‌تونم کمک کنم با:\n📊 قیمت‌ها و پیش‌بینی‌های بازار\n🌍 پایتخت‌ها و جغرافیا\n👤 افراد مشهور و تاریخ\n💰 اطلاعات کریپتو و فارکس\n📅 رویدادهای تقویم\n📰 اخبار جهانی\nفقط بپرسید! 🤖"}},
            
            {"patterns": ["thanks", "thank you", "ممنون", "مرسی", "تشکر", "سپاس"],
             "responses": {"en": "You're welcome! Happy trading! May your profits be endless! 🚀💰",
                          "fa": "خواهش می‌کنم! معامله موفق! امیدوارم سودهای بی‌پایان داشته باشید! 🚀💰"}},
            
            {"patterns": ["trump", "ترامپ"],
             "responses": {"en": self.famous_people["donald trump"], "fa": self.famous_people["دونالد ترامپ"]}},
            
            {"patterns": ["elon", "musk", "ایلان", "ماسک"],
             "responses": {"en": self.famous_people["elon musk"], "fa": self.famous_people["ایلان ماسک"]}},
            
            {"patterns": ["napoleon", "ناپلئون"],
             "responses": {"en": self.famous_people["napoleon"], "fa": self.famous_people["ناپلئون"]}},
            
            {"patterns": ["marco rubio", "مارکو روبیو"],
             "responses": {"en": self.famous_people["marco rubio"], "fa": self.famous_people["مارکو روبیو"]}},
            
            {"patterns": ["putin", "پوتین"],
             "responses": {"en": self.famous_people["vladimir putin"], "fa": self.famous_people["ولادیمیر پوتین"]}},
            
            {"patterns": ["biden", "بایدن"],
             "responses": {"en": self.famous_people["joe biden"], "fa": self.famous_people["جو بایدن"]}},
            
            {"patterns": ["satoshi", "ساتوشی"],
             "responses": {"en": self.famous_people["satoshi nakamoto"], "fa": self.famous_people["ساتوشی ناکاموتو"]}},
            
            {"patterns": ["vitalik", "ویتالیک"],
             "responses": {"en": self.famous_people["vitalik buterin"], "fa": self.famous_people["ویتالیک بوترین"]}},
            
            {"patterns": ["bezos", "بزوس"],
             "responses": {"en": self.famous_people["jeff bezos"], "fa": self.famous_people["جف بزوس"]}},
            
            {"patterns": ["gates", "گیتس"],
             "responses": {"en": self.famous_people["bill gates"], "fa": self.famous_people["بیل گیتس"]}},
            
            {"patterns": ["jobs", "جابز"],
             "responses": {"en": self.famous_people["steve jobs"], "fa": self.famous_people["استیو جابز"]}},
            
            {"patterns": ["zuckerberg", "زاکربرگ"],
             "responses": {"en": self.famous_people["mark zuckerberg"], "fa": self.famous_people["مارک زاکربرگ"]}},
            
            {"patterns": ["buffett", "بافت"],
             "responses": {"en": self.famous_people["warren buffett"], "fa": self.famous_people["وارن بافت"]}},
            
            {"patterns": ["powell", "پاول"],
             "responses": {"en": self.famous_people["jerome powell"], "fa": self.famous_people["جروم پاول"]}},
            
            {"patterns": ["macron", "ماکرون"],
             "responses": {"en": self.famous_people["emmanuel macron"], "fa": self.famous_people["امانوئل ماکرون"]}},
            
            {"patterns": ["merkel", "مرکل"],
             "responses": {"en": self.famous_people["angela merkel"], "fa": self.famous_people["آنگلا مرکل"]}},
            
            {"patterns": ["calendar", "تقویم", "event", "رویداد"],
             "responses": {"en": "Check the Global Events Calendar! Shows Gregorian & Persian dates with market-impacting events. 📅",
                          "fa": "تقویم رویدادهای جهانی را بررسی کنید! تاریخ میلادی و شمسی با رویدادهای تأثیرگذار بر بازار. 📅"}},
            
            {"patterns": ["news", "اخبار"],
             "responses": {"en": "Check the News Feed for latest updates from Trump, Musk, Federal Reserve in English & Persian! 📰",
                          "fa": "بخش اخبار را برای آخرین به‌روزرسانی‌ها از ترامپ، ماسک، فدرال رزرو به انگلیسی و فارسی ببینید! 📰"}},
            
            {"patterns": ["predict", "forecast", "پیش بینی", "future"],
             "responses": {"en": "AI predicts using Moving Average & RSI. Check 'AI Prediction' card and purple dashed line for 7-day forecast! 🔮",
                          "fa": "AI با میانگین متحرک و RSI پیش‌بینی می‌کند. کارت 'پیش‌بینی AI' و خط نقطه‌چین بنفش برای پیش‌بینی ۷ روزه! 🔮"}},
            
            {"patterns": ["rsi", "شاخص قدرت"],
             "responses": {"en": "RSI (Relative Strength Index) - Above 70: overbought (sell), Below 30: oversold (buy). Shown on dashboard! 📊",
                          "fa": "RSI (شاخص قدرت نسبی) - بالای ۷۰: اشباع خرید (فروش)، زیر ۳۰: اشباع فروش (خرید). در داشبورد! 📊"}},
            
            {"patterns": ["inflation", "تورم"],
             "responses": {"en": "Inflation erodes purchasing power. Gold & Bitcoin are inflation hedges. When inflation rises, central banks raise rates. 📊",
                          "fa": "تورم قدرت خرید را کاهش می‌دهد. طلا و بیت‌کوین پوشش تورم هستند. وقتی تورم بالا می‌رود، بانک‌های مرکزی نرخ را افزایش می‌دهند. 📊"}},
            
            {"patterns": ["forex", "فارکس"],
             "responses": {"en": "Forex - Global currency market, $6 trillion daily volume. Major pairs: EUR/USD, GBP/USD, USD/JPY. 💱",
                          "fa": "فارکس - بازار ارز جهانی، ۶ تریلیون دلار حجم روزانه. جفت‌ارزهای اصلی: EUR/USD, GBP/USD, USD/JPY. 💱"}},
        ]
    
    def detect_language(self, message: str) -> str:
        persian_chars = re.findall(r'[\u0600-\u06FF]', message)
        return "fa" if len(persian_chars) > len(message) * 0.3 else "en"
    
    def get_response(self, message: str) -> str:
        message_lower = message.lower().strip()
        lang = self.detect_language(message)
        
        # Save to history
        self.conversation_history.append({"role": "user", "message": message, "time": datetime.now().isoformat()})
        
        if not message_lower:
            return "Please type a message! 💬" if lang == "en" else "لطفاً پیامی تایپ کنید! 💬"
        
        # Check for capital city queries
        for country, capital in self.capitals.items():
            if country in message_lower:
                response = f"The capital of {country.title()} is {capital}! 🌍" if lang == "en" else f"پایتخت {country} {capital} است! 🌍"
                self.conversation_history.append({"role": "bot", "message": response, "time": datetime.now().isoformat()})
                return response
        
        # Check for famous people
        for person, info in self.famous_people.items():
            if person in message_lower:
                self.conversation_history.append({"role": "bot", "message": info, "time": datetime.now().isoformat()})
                return info
        
        # Check for crypto knowledge
        for crypto, info in self.crypto_knowledge.items():
            if crypto in message_lower:
                self.conversation_history.append({"role": "bot", "message": info, "time": datetime.now().isoformat()})
                return info
        
        # Check pattern responses
        for category in self.responses:
            for pattern in category["patterns"]:
                if pattern and pattern in message_lower:
                    response = category["responses"].get(lang, category["responses"]["en"])
                    self.conversation_history.append({"role": "bot", "message": response, "time": datetime.now().isoformat()})
                    return response
        
        # Default
        default = "I'm not sure about that. Try: capitals, famous people, crypto info, or type 'help'! 🤖" if lang == "en" else "مطمئن نیستم. امتحان کنید: پایتخت‌ها، افراد مشهور، اطلاعات کریپتو، یا 'help' را تایپ کنید! 🤖"
        self.conversation_history.append({"role": "bot", "message": default, "time": datetime.now().isoformat()})
        return default
    
    def get_history(self):
        return self.conversation_history[-20:]  # Last 20 messages
