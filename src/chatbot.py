"""
Advanced Multilingual Chatbot with Memory & Extensive Knowledge
Works Online and Offline - Empire Edition
"""
import re
from datetime import datetime
import json
from pathlib import Path


class ChatBot:
    def __init__(self):
        self.name = "Market Oracle AI"
        self.version = "5.0 Empire Edition"
        self.creator = "Amirhossein Ahmadvand (امیرحسین احمدوند)"
        self.created_date = "2026"
        self.conversation_history = []
        self.memory_file = Path("data/chat_memory.json")
        self._load_memory()
        
        self.capitals = self._load_capitals()
        self.famous_people = self._load_famous_people()
        self.crypto_info = self._load_crypto_info()
        self.forex_info = self._load_forex_info()
        self.general_knowledge = self._load_general_knowledge()
        self.responses = self._load_responses()
    
    def _load_memory(self):
        """Load conversation history from file."""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                    self.conversation_history = data.get('history', [])
            except:
                self.conversation_history = []
        else:
            self.memory_file.parent.mkdir(exist_ok=True)
    
    def _save_memory(self):
        """Save conversation history to file."""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump({'history': self.conversation_history[-100:]}, f)
        except:
            pass
    
    def _load_capitals(self):
        """Load all world capitals."""
        return {
            # Middle East
            "iran": {"capital": "Tehran (تهران)", "country": "Iran", "region": "Middle East", "population": "9 million"},
            "tehran": {"capital": "Tehran", "country": "Iran", "region": "Middle East", "population": "9 million"},
            "iraq": {"capital": "Baghdad (بغداد)", "country": "Iraq", "region": "Middle East", "population": "7 million"},
            "baghdad": {"capital": "Baghdad", "country": "Iraq", "region": "Middle East"},
            "syria": {"capital": "Damascus (دمشق)", "country": "Syria", "region": "Middle East"},
            "damascus": {"capital": "Damascus", "country": "Syria", "region": "Middle East"},
            "lebanon": {"capital": "Beirut (بیروت)", "country": "Lebanon", "region": "Middle East"},
            "beirut": {"capital": "Beirut", "country": "Lebanon", "region": "Middle East"},
            "jordan": {"capital": "Amman (امان)", "country": "Jordan", "region": "Middle East"},
            "amman": {"capital": "Amman", "country": "Jordan", "region": "Middle East"},
            "saudi arabia": {"capital": "Riyadh (ریاض)", "country": "Saudi Arabia", "region": "Middle East"},
            "riyadh": {"capital": "Riyadh", "country": "Saudi Arabia", "region": "Middle East"},
            "uae": {"capital": "Abu Dhabi (ابوظبی)", "country": "UAE", "region": "Middle East"},
            "abu dhabi": {"capital": "Abu Dhabi", "country": "UAE", "region": "Middle East"},
            "qatar": {"capital": "Doha (دوحه)", "country": "Qatar", "region": "Middle East"},
            "doha": {"capital": "Doha", "country": "Qatar", "region": "Middle East"},
            "kuwait": {"capital": "Kuwait City (کویت)", "country": "Kuwait", "region": "Middle East"},
            "kuwait city": {"capital": "Kuwait City", "country": "Kuwait", "region": "Middle East"},
            "bahrain": {"capital": "Manama (منامه)", "country": "Bahrain", "region": "Middle East"},
            "manama": {"capital": "Manama", "country": "Bahrain", "region": "Middle East"},
            "oman": {"capital": "Muscat (مسقط)", "country": "Oman", "region": "Middle East"},
            "muscat": {"capital": "Muscat", "country": "Oman", "region": "Middle East"},
            "yemen": {"capital": "Sana'a (صنعا)", "country": "Yemen", "region": "Middle East"},
            "egypt": {"capital": "Cairo (قاهره)", "country": "Egypt", "region": "Middle East/Africa"},
            "cairo": {"capital": "Cairo", "country": "Egypt", "region": "Middle East/Africa"},
            "israel": {"capital": "Jerusalem (اورشلیم)", "country": "Israel", "region": "Middle East"},
            "jerusalem": {"capital": "Jerusalem", "country": "Israel", "region": "Middle East"},
            "palestine": {"capital": "Ramallah (رام‌الله)", "country": "Palestine", "region": "Middle East"},
            "turkey": {"capital": "Ankara (آنکارا)", "country": "Turkey", "region": "Middle East/Europe"},
            "ankara": {"capital": "Ankara", "country": "Turkey", "region": "Middle East/Europe"},
            
            # Europe
            "uk": {"capital": "London (لندن)", "country": "United Kingdom", "region": "Europe"},
            "united kingdom": {"capital": "London", "country": "United Kingdom", "region": "Europe"},
            "england": {"capital": "London", "country": "England", "region": "Europe"},
            "london": {"capital": "London", "country": "UK", "region": "Europe"},
            "france": {"capital": "Paris (پاریس)", "country": "France", "region": "Europe"},
            "paris": {"capital": "Paris", "country": "France", "region": "Europe"},
            "germany": {"capital": "Berlin (برلین)", "country": "Germany", "region": "Europe"},
            "berlin": {"capital": "Berlin", "country": "Germany", "region": "Europe"},
            "italy": {"capital": "Rome (رم)", "country": "Italy", "region": "Europe"},
            "rome": {"capital": "Rome", "country": "Italy", "region": "Europe"},
            "spain": {"capital": "Madrid (مادرید)", "country": "Spain", "region": "Europe"},
            "madrid": {"capital": "Madrid", "country": "Spain", "region": "Europe"},
            "russia": {"capital": "Moscow (مسکو)", "country": "Russia", "region": "Europe/Asia"},
            "moscow": {"capital": "Moscow", "country": "Russia", "region": "Europe/Asia"},
            "ukraine": {"capital": "Kyiv (کی‌یف)", "country": "Ukraine", "region": "Europe"},
            "kyiv": {"capital": "Kyiv", "country": "Ukraine", "region": "Europe"},
            "poland": {"capital": "Warsaw (ورشو)", "country": "Poland", "region": "Europe"},
            "warsaw": {"capital": "Warsaw", "country": "Poland", "region": "Europe"},
            "greece": {"capital": "Athens (آتن)", "country": "Greece", "region": "Europe"},
            "athens": {"capital": "Athens", "country": "Greece", "region": "Europe"},
            "portugal": {"capital": "Lisbon (لیسبون)", "country": "Portugal", "region": "Europe"},
            "lisbon": {"capital": "Lisbon", "country": "Portugal", "region": "Europe"},
            "netherlands": {"capital": "Amsterdam (آمستردام)", "country": "Netherlands", "region": "Europe"},
            "amsterdam": {"capital": "Amsterdam", "country": "Netherlands", "region": "Europe"},
            "belgium": {"capital": "Brussels (بروکسل)", "country": "Belgium", "region": "Europe"},
            "brussels": {"capital": "Brussels", "country": "Belgium", "region": "Europe"},
            "switzerland": {"capital": "Bern (برن)", "country": "Switzerland", "region": "Europe"},
            "bern": {"capital": "Bern", "country": "Switzerland", "region": "Europe"},
            "austria": {"capital": "Vienna (وین)", "country": "Austria", "region": "Europe"},
            "vienna": {"capital": "Vienna", "country": "Austria", "region": "Europe"},
            "sweden": {"capital": "Stockholm (استکهلم)", "country": "Sweden", "region": "Europe"},
            "stockholm": {"capital": "Stockholm", "country": "Sweden", "region": "Europe"},
            "norway": {"capital": "Oslo (اسلو)", "country": "Norway", "region": "Europe"},
            "oslo": {"capital": "Oslo", "country": "Norway", "region": "Europe"},
            "denmark": {"capital": "Copenhagen (کپنهاگ)", "country": "Denmark", "region": "Europe"},
            "copenhagen": {"capital": "Copenhagen", "country": "Denmark", "region": "Europe"},
            "finland": {"capital": "Helsinki (هلسینکی)", "country": "Finland", "region": "Europe"},
            "helsinki": {"capital": "Helsinki", "country": "Finland", "region": "Europe"},
            "czech republic": {"capital": "Prague (پراگ)", "country": "Czech Republic", "region": "Europe"},
            "prague": {"capital": "Prague", "country": "Czech Republic", "region": "Europe"},
            "hungary": {"capital": "Budapest (بوداپست)", "country": "Hungary", "region": "Europe"},
            "budapest": {"capital": "Budapest", "country": "Hungary", "region": "Europe"},
            "romania": {"capital": "Bucharest (بخارست)", "country": "Romania", "region": "Europe"},
            "bucharest": {"capital": "Bucharest", "country": "Romania", "region": "Europe"},
            "bulgaria": {"capital": "Sofia (صوفیه)", "country": "Bulgaria", "region": "Europe"},
            "sofia": {"capital": "Sofia", "country": "Bulgaria", "region": "Europe"},
            
            # Asia
            "china": {"capital": "Beijing (پکن)", "country": "China", "region": "Asia"},
            "beijing": {"capital": "Beijing", "country": "China", "region": "Asia"},
            "japan": {"capital": "Tokyo (توکیو)", "country": "Japan", "region": "Asia"},
            "tokyo": {"capital": "Tokyo", "country": "Japan", "region": "Asia"},
            "india": {"capital": "New Delhi (دهلی نو)", "country": "India", "region": "Asia"},
            "new delhi": {"capital": "New Delhi", "country": "India", "region": "Asia"},
            "delhi": {"capital": "New Delhi", "country": "India", "region": "Asia"},
            "south korea": {"capital": "Seoul (سئول)", "country": "South Korea", "region": "Asia"},
            "seoul": {"capital": "Seoul", "country": "South Korea", "region": "Asia"},
            "north korea": {"capital": "Pyongyang (پیونگ‌یانگ)", "country": "North Korea", "region": "Asia"},
            "pyongyang": {"capital": "Pyongyang", "country": "North Korea", "region": "Asia"},
            "vietnam": {"capital": "Hanoi (هانوی)", "country": "Vietnam", "region": "Asia"},
            "hanoi": {"capital": "Hanoi", "country": "Vietnam", "region": "Asia"},
            "thailand": {"capital": "Bangkok (بانکوک)", "country": "Thailand", "region": "Asia"},
            "bangkok": {"capital": "Bangkok", "country": "Thailand", "region": "Asia"},
            "indonesia": {"capital": "Jakarta (جاکارتا)", "country": "Indonesia", "region": "Asia"},
            "jakarta": {"capital": "Jakarta", "country": "Indonesia", "region": "Asia"},
            "malaysia": {"capital": "Kuala Lumpur (کوالالامپور)", "country": "Malaysia", "region": "Asia"},
            "kuala lumpur": {"capital": "Kuala Lumpur", "country": "Malaysia", "region": "Asia"},
            "singapore": {"capital": "Singapore (سنگاپور)", "country": "Singapore", "region": "Asia"},
            "philippines": {"capital": "Manila (مانیل)", "country": "Philippines", "region": "Asia"},
            "manila": {"capital": "Manila", "country": "Philippines", "region": "Asia"},
            "pakistan": {"capital": "Islamabad (اسلام‌آباد)", "country": "Pakistan", "region": "Asia"},
            "islamabad": {"capital": "Islamabad", "country": "Pakistan", "region": "Asia"},
            "bangladesh": {"capital": "Dhaka (داکا)", "country": "Bangladesh", "region": "Asia"},
            "dhaka": {"capital": "Dhaka", "country": "Bangladesh", "region": "Asia"},
            "sri lanka": {"capital": "Colombo (کلمبو)", "country": "Sri Lanka", "region": "Asia"},
            "colombo": {"capital": "Colombo", "country": "Sri Lanka", "region": "Asia"},
            "nepal": {"capital": "Kathmandu (کاتماندو)", "country": "Nepal", "region": "Asia"},
            "kathmandu": {"capital": "Kathmandu", "country": "Nepal", "region": "Asia"},
            "afghanistan": {"capital": "Kabul (کابل)", "country": "Afghanistan", "region": "Asia"},
            "kabul": {"capital": "Kabul", "country": "Afghanistan", "region": "Asia"},
            
            # Americas
            "usa": {"capital": "Washington D.C. (واشنگتن)", "country": "United States", "region": "North America"},
            "united states": {"capital": "Washington D.C.", "country": "United States", "region": "North America"},
            "america": {"capital": "Washington D.C.", "country": "USA", "region": "North America"},
            "washington": {"capital": "Washington D.C.", "country": "USA", "region": "North America"},
            "canada": {"capital": "Ottawa (اتاوا)", "country": "Canada", "region": "North America"},
            "ottawa": {"capital": "Ottawa", "country": "Canada", "region": "North America"},
            "mexico": {"capital": "Mexico City (مکزیکو سیتی)", "country": "Mexico", "region": "North America"},
            "mexico city": {"capital": "Mexico City", "country": "Mexico", "region": "North America"},
            "brazil": {"capital": "Brasilia (برازیلیا)", "country": "Brazil", "region": "South America"},
            "brasilia": {"capital": "Brasilia", "country": "Brazil", "region": "South America"},
            "argentina": {"capital": "Buenos Aires (بوئنوس آیرس)", "country": "Argentina", "region": "South America"},
            "buenos aires": {"capital": "Buenos Aires", "country": "Argentina", "region": "South America"},
            "chile": {"capital": "Santiago (سانتیاگو)", "country": "Chile", "region": "South America"},
            "santiago": {"capital": "Santiago", "country": "Chile", "region": "South America"},
            "colombia": {"capital": "Bogota (بوگوتا)", "country": "Colombia", "region": "South America"},
            "bogota": {"capital": "Bogota", "country": "Colombia", "region": "South America"},
            "peru": {"capital": "Lima (لیما)", "country": "Peru", "region": "South America"},
            "lima": {"capital": "Lima", "country": "Peru", "region": "South America"},
            "venezuela": {"capital": "Caracas (کاراکاس)", "country": "Venezuela", "region": "South America"},
            "caracas": {"capital": "Caracas", "country": "Venezuela", "region": "South America"},
            
            # Africa
            "south africa": {"capital": "Pretoria (پرتوریا)", "country": "South Africa", "region": "Africa"},
            "pretoria": {"capital": "Pretoria", "country": "South Africa", "region": "Africa"},
            "nigeria": {"capital": "Abuja (آبوجا)", "country": "Nigeria", "region": "Africa"},
            "abuja": {"capital": "Abuja", "country": "Nigeria", "region": "Africa"},
            "kenya": {"capital": "Nairobi (نایروبی)", "country": "Kenya", "region": "Africa"},
            "nairobi": {"capital": "Nairobi", "country": "Kenya", "region": "Africa"},
            "morocco": {"capital": "Rabat (رباط)", "country": "Morocco", "region": "Africa"},
            "rabat": {"capital": "Rabat", "country": "Morocco", "region": "Africa"},
            "egypt": {"capital": "Cairo (قاهره)", "country": "Egypt", "region": "Africa"},
            "libya": {"capital": "Tripoli (طرابلس)", "country": "Libya", "region": "Africa"},
            "tripoli": {"capital": "Tripoli", "country": "Libya", "region": "Africa"},
            "tunisia": {"capital": "Tunis (تونس)", "country": "Tunisia", "region": "Africa"},
            "tunis": {"capital": "Tunis", "country": "Tunisia", "region": "Africa"},
            "algeria": {"capital": "Algiers (الجزیره)", "country": "Algeria", "region": "Africa"},
            "algiers": {"capital": "Algiers", "country": "Algeria", "region": "Africa"},
            "sudan": {"capital": "Khartoum (خارطوم)", "country": "Sudan", "region": "Africa"},
            "khartoum": {"capital": "Khartoum", "country": "Sudan", "region": "Africa"},
            "ethiopia": {"capital": "Addis Ababa (آدیس آبابا)", "country": "Ethiopia", "region": "Africa"},
            "addis ababa": {"capital": "Addis Ababa", "country": "Ethiopia", "region": "Africa"},
            "ghana": {"capital": "Accra (آکرا)", "country": "Ghana", "region": "Africa"},
            "accra": {"capital": "Accra", "country": "Ghana", "region": "Africa"},
            
            # Oceania
            "australia": {"capital": "Canberra (کانبرا)", "country": "Australia", "region": "Oceania"},
            "canberra": {"capital": "Canberra", "country": "Australia", "region": "Oceania"},
            "new zealand": {"capital": "Wellington (ولینگتون)", "country": "New Zealand", "region": "Oceania"},
            "wellington": {"capital": "Wellington", "country": "New Zealand", "region": "Oceania"},
            
            # Persian versions
            "ایران": {"capital": "تهران (Tehran)", "country": "Iran", "region": "خاورمیانه"},
            "تهران": {"capital": "Tehran", "country": "Iran", "region": "خاورمیانه"},
            "آمریکا": {"capital": "Washington D.C.", "country": "USA", "region": "آمریکای شمالی"},
            "انگلیس": {"capital": "London", "country": "UK", "region": "اروپا"},
            "فرانسه": {"capital": "Paris", "country": "France", "region": "اروپا"},
            "آلمان": {"capital": "Berlin", "country": "Germany", "region": "اروپا"},
            "ایتالیا": {"capital": "Rome", "country": "Italy", "region": "اروپا"},
            "اسپانیا": {"capital": "Madrid", "country": "Spain", "region": "اروپا"},
            "روسیه": {"capital": "Moscow", "country": "Russia", "region": "اروپا/آسیا"},
            "چین": {"capital": "Beijing", "country": "China", "region": "آسیا"},
            "ژاپن": {"capital": "Tokyo", "country": "Japan", "region": "آسیا"},
            "هند": {"capital": "New Delhi", "country": "India", "region": "آسیا"},
            "ترکیه": {"capital": "Ankara", "country": "Turkey", "region": "خاورمیانه/اروپا"},
            "عربستان": {"capital": "Riyadh", "country": "Saudi Arabia", "region": "خاورمیانه"},
            "امارات": {"capital": "Abu Dhabi", "country": "UAE", "region": "خاورمیانه"},
            "عراق": {"capital": "Baghdad", "country": "Iraq", "region": "خاورمیانه"},
            "افغانستان": {"capital": "Kabul", "country": "Afghanistan", "region": "آسیا"},
            "پاکستان": {"capital": "Islamabad", "country": "Pakistan", "region": "آسیا"},
            "مصر": {"capital": "Cairo", "country": "Egypt", "region": "خاورمیانه/آفریقا"},
            "سوریه": {"capital": "Damascus", "country": "Syria", "region": "خاورمیانه"},
            "لبنان": {"capital": "Beirut", "country": "Lebanon", "region": "خاورمیانه"},
            "اردن": {"capital": "Amman", "country": "Jordan", "region": "خاورمیانه"},
            "کویت": {"capital": "Kuwait City", "country": "Kuwait", "region": "خاورمیانه"},
            "قطر": {"capital": "Doha", "country": "Qatar", "region": "خاورمیانه"},
            "بحرین": {"capital": "Manama", "country": "Bahrain", "region": "خاورمیانه"},
            "عمان": {"capital": "Muscat", "country": "Oman", "region": "خاورمیانه"},
            "یمن": {"capital": "Sana'a", "country": "Yemen", "region": "خاورمیانه"},
            "کره جنوبی": {"capital": "Seoul", "country": "South Korea", "region": "آسیا"},
            "کره شمالی": {"capital": "Pyongyang", "country": "North Korea", "region": "آسیا"},
            "ویتنام": {"capital": "Hanoi", "country": "Vietnam", "region": "آسیا"},
            "تایلند": {"capital": "Bangkok", "country": "Thailand", "region": "آسیا"},
            "اندونزی": {"capital": "Jakarta", "country": "Indonesia", "region": "آسیا"},
            "مالزی": {"capital": "Kuala Lumpur", "country": "Malaysia", "region": "آسیا"},
            "سنگاپور": {"capital": "Singapore", "country": "Singapore", "region": "آسیا"},
            "فیلیپین": {"capital": "Manila", "country": "Philippines", "region": "آسیا"},
            "برزیل": {"capital": "Brasilia", "country": "Brazil", "region": "آمریکای جنوبی"},
            "آرژانتین": {"capital": "Buenos Aires", "country": "Argentina", "region": "آمریکای جنوبی"},
            "شیلی": {"capital": "Santiago", "country": "Chile", "region": "آمریکای جنوبی"},
            "کلمبیا": {"capital": "Bogota", "country": "Colombia", "region": "آمریکای جنوبی"},
            "مکزیک": {"capital": "Mexico City", "country": "Mexico", "region": "آمریکای شمالی"},
            "کانادا": {"capital": "Ottawa", "country": "Canada", "region": "آمریکای شمالی"},
            "استرالیا": {"capital": "Canberra", "country": "Australia", "region": "اقیانوسیه"},
            "نیوزیلند": {"capital": "Wellington", "country": "New Zealand", "region": "اقیانوسیه"},
            "آفریقای جنوبی": {"capital": "Pretoria", "country": "South Africa", "region": "آفریقا"},
            "نیجریه": {"capital": "Abuja", "country": "Nigeria", "region": "آفریقا"},
            "کنیا": {"capital": "Nairobi", "country": "Kenya", "region": "آفریقا"},
            "مراکش": {"capital": "Rabat", "country": "Morocco", "region": "آفریقا"},
            "لیبی": {"capital": "Tripoli", "country": "Libya", "region": "آفریقا"},
            "تونس": {"capital": "Tunis", "country": "Tunisia", "region": "آفریقا"},
            "الجزایر": {"capital": "Algiers", "country": "Algeria", "region": "آفریقا"},
            "سودان": {"capital": "Khartoum", "country": "Sudan", "region": "آفریقا"},
            "اتیوپی": {"capital": "Addis Ababa", "country": "Ethiopia", "region": "آفریقا"},
            "غنا": {"capital": "Accra", "country": "Ghana", "region": "آفریقا"},
            "اوکراین": {"capital": "Kyiv", "country": "Ukraine", "region": "اروپا"},
            "لهستان": {"capital": "Warsaw", "country": "Poland", "region": "اروپا"},
            "سوئد": {"capital": "Stockholm", "country": "Sweden", "region": "اروپا"},
            "نروژ": {"capital": "Oslo", "country": "Norway", "region": "اروپا"},
            "دانمارک": {"capital": "Copenhagen", "country": "Denmark", "region": "اروپا"},
            "فنلاند": {"capital": "Helsinki", "country": "Finland", "region": "اروپا"},
            "یونان": {"capital": "Athens", "country": "Greece", "region": "اروپا"},
            "پرتغال": {"capital": "Lisbon", "country": "Portugal", "region": "اروپا"},
            "هلند": {"capital": "Amsterdam", "country": "Netherlands", "region": "اروپا"},
            "بلژیک": {"capital": "Brussels", "country": "Belgium", "region": "اروپا"},
            "سوئیس": {"capital": "Bern", "country": "Switzerland", "region": "اروپا"},
            "اتریش": {"capital": "Vienna", "country": "Austria", "region": "اروپا"},
            "چک": {"capital": "Prague", "country": "Czech Republic", "region": "اروپا"},
            "مجارستان": {"capital": "Budapest", "country": "Hungary", "region": "اروپا"},
            "رومانی": {"capital": "Bucharest", "country": "Romania", "region": "اروپا"},
            "بلغارستان": {"capital": "Sofia", "country": "Bulgaria", "region": "اروپا"},
            "صربستان": {"capital": "Belgrade", "country": "Serbia", "region": "اروپا"},
            "کرواسی": {"capital": "Zagreb", "country": "Croatia", "region": "اروپا"},
            "قزاقستان": {"capital": "Astana", "country": "Kazakhstan", "region": "آسیا"},
            "ازبکستان": {"capital": "Tashkent", "country": "Uzbekistan", "region": "آسیا"},
            "ترکمنستان": {"capital": "Ashgabat", "country": "Turkmenistan", "region": "آسیا"},
            "قرقیزستان": {"capital": "Bishkek", "country": "Kyrgyzstan", "region": "آسیا"},
            "تاجیکستان": {"capital": "Dushanbe", "country": "Tajikistan", "region": "آسیا"},
            "مغولستان": {"capital": "Ulaanbaatar", "country": "Mongolia", "region": "آسیا"},
            "نپال": {"capital": "Kathmandu", "country": "Nepal", "region": "آسیا"},
            "بوتان": {"capital": "Thimphu", "country": "Bhutan", "region": "آسیا"},
            "سری لانکا": {"capital": "Colombo", "country": "Sri Lanka", "region": "آسیا"},
            "بنگلادش": {"capital": "Dhaka", "country": "Bangladesh", "region": "آسیا"},
            "میانمار": {"capital": "Naypyidaw", "country": "Myanmar", "region": "آسیا"},
            "کامبوج": {"capital": "Phnom Penh", "country": "Cambodia", "region": "آسیا"},
            "لائوس": {"capital": "Vientiane", "country": "Laos", "region": "آسیا"},
            "برونئی": {"capital": "Bandar Seri Begawan", "country": "Brunei", "region": "آسیا"},
            "مالدیو": {"capital": "Male", "country": "Maldives", "region": "آسیا"},
            "فیجی": {"capital": "Suva", "country": "Fiji", "region": "اقیانوسیه"},
            "کوبا": {"capital": "Havana", "country": "Cuba", "region": "آمریکای مرکزی"},
            "جامائیکا": {"capital": "Kingston", "country": "Jamaica", "region": "آمریکای مرکزی"},
            "هائیتی": {"capital": "Port-au-Prince", "country": "Haiti", "region": "آمریکای مرکزی"},
            "دومینیکن": {"capital": "Santo Domingo", "country": "Dominican Republic", "region": "آمریکای مرکزی"},
            "پورتوریکو": {"capital": "San Juan", "country": "Puerto Rico", "region": "آمریکای مرکزی"},
            "کاستاریکا": {"capital": "San Jose", "country": "Costa Rica", "region": "آمریکای مرکزی"},
            "پاناما": {"capital": "Panama City", "country": "Panama", "region": "آمریکای مرکزی"},
            "گواتمالا": {"capital": "Guatemala City", "country": "Guatemala", "region": "آمریکای مرکزی"},
            "هندوراس": {"capital": "Tegucigalpa", "country": "Honduras", "region": "آمریکای مرکزی"},
            "نیکاراگوئه": {"capital": "Managua", "country": "Nicaragua", "region": "آمریکای مرکزی"},
            "السالوادور": {"capital": "San Salvador", "country": "El Salvador", "region": "آمریکای مرکزی"},
            "بلیز": {"capital": "Belmopan", "country": "Belize", "region": "آمریکای مرکزی"},
            "باهاما": {"capital": "Nassau", "country": "Bahamas", "region": "آمریکای مرکزی"},
            "باربادوس": {"capital": "Bridgetown", "country": "Barbados", "region": "آمریکای مرکزی"},
            "ترینیداد": {"capital": "Port of Spain", "country": "Trinidad and Tobago", "region": "آمریکای مرکزی"},
            "گویان": {"capital": "Georgetown", "country": "Guyana", "region": "آمریکای جنوبی"},
            "سورینام": {"capital": "Paramaribo", "country": "Suriname", "region": "آمریکای جنوبی"},
            "اروگوئه": {"capital": "Montevideo", "country": "Uruguay", "region": "آمریکای جنوبی"},
            "پاراگوئه": {"capital": "Asuncion", "country": "Paraguay", "region": "آمریکای جنوبی"},
            "بولیوی": {"capital": "Sucre", "country": "Bolivia", "region": "آمریکای جنوبی"},
            "اکوادور": {"capital": "Quito", "country": "Ecuador", "region": "آمریکای جنوبی"},
            "پرو": {"capital": "Lima", "country": "Peru", "region": "آمریکای جنوبی"},
            "ونزوئلا": {"capital": "Caracas", "country": "Venezuela", "region": "آمریکای جنوبی"},
        }
    
    def _load_famous_people(self):
        """Load information about famous people."""
        return {
            # Historical Figures
            "napoleon": "Napoleon Bonaparte (1769-1821) - French military leader and emperor who conquered much of Europe. Famous for the Napoleonic Wars, his exile to Elba and Saint Helena, and the Napoleonic Code. Died at age 51.",
            "napoleon bonaparte": "Napoleon Bonaparte - French emperor and military genius. Born in Corsica, rose to power during the French Revolution. Defeated at Waterloo in 1815. Exiled to Saint Helena where he died.",
            "ناپلئون": "ناپلئون بناپارت (۱۷۹-۱۸۲) - رهبر نظامی و امپراتور فرانسه که بخش بزرگی از اروپا را فتح کرد. در واترلو شکست خورد و به سنت هلن تبعید شد. در ۵۱ سالگی درگذشت.",
            
            "marco rubio": "Marco Rubio - American politician, U.S. Senator from Florida since 2011. Born May 28, 1971 in Miami, Florida. Known for foreign policy expertise, conservative views, and potential presidential candidate. Republican Party member.",
            "مارکو روبیو": "مارکو روبیو - سیاستمدار آمریکایی، سناتور ایالات متحده از فلوریدا از سال ۲۱۱. متولد ۲۸ مه ۱۷۱ در میامی، فلوریدا. معروف به تخصص در سیاست خارجی، دیدگاه‌های محافظه‌کارانه و نامزد احتمالی ریاست‌جمهوری. عضو حزب جمهوری‌خواه.",
            
            # Tech Leaders
            "elon musk": "Elon Musk - CEO of Tesla, SpaceX, and owner of X (Twitter). Born June 28, 1971 in Pretoria, South Africa. Known for electric vehicles, space exploration (Starship, Mars colonization), and cryptocurrency influence. Net worth: ~$250 billion.",
            "ایلان ماسک": "ایلان ماسک - مدیرعامل تسلا، اسپیس‌اکس و مالک X (توییتر). متولد ۲۸ ژوئن ۱۹۷۱ در پرتوریا، آفریقای جنوبی. معروف به خودروهای الکتریکی، اکتشافات فضایی (Starship، استعمار مریخ) و تأثیر بر کریپتوکارنسی. ثروت خالص: حدود ۲۵۰ میلیارد دلار.",
            
            "donald trump": "Donald Trump - 45th and 47th President of the United States. Born June 14, 1946 in New York. Businessman and politician. Known for 'America First' policy, impact on global markets, and trade wars. Republican Party.",
            "دونالد ترامپ": "دونالد ترامپ - چهل و پنجمین و چهل و هفتمین رئیس‌جمهور ایالات متحده. متولد ۱۴ ژوئن ۱۹۴ در نیویورک. تاجر و سیاستمدار. معروف به سیاست 'آمریکا اول'، تأثیر بر بازارهای جهانی و جنگ‌های تجاری. حزب جمهوری‌خواه.",
            
            "joe biden": "Joe Biden - 46th President of the United States. Born November 20, 1942. Former Vice President under Obama (2009-2017). Known for infrastructure bills, foreign policy, and climate change initiatives. Democratic Party.",
            "جو بایدن": "جو بایدن - چهل و ششمین رئیس‌جمهور ایالات متحده. متولد ۲۰ نوامبر ۱۹۴۲. معاون سابق اوباما (۲۰۰۹-۲۰۱۷). معروف به قوانین زیرساخت، سیاست خارجی و ابتکارات تغییرات اقلیمی. حزب دموکرات.",
            
            "vladimir putin": "Vladimir Putin - President of Russia since 2000 (and 2008-2012 as PM). Born October 7, 1952 in Leningrad. Former KGB officer. Known for strong leadership, Crimea annexation, Ukraine conflict, and impact on global geopolitics.",
            "ولادیمیر پوتین": "ولادیمیر پوتین - رئیس‌جمهور روسیه از سال ۲۰۰۰ (و ۲۰۰-۲۰۱۲ به عنوان نخست‌وزیر). متولد ۷ اکتبر ۱۹۵۲ در لنینگراد. افسر سابق KGB. معروف به رهبری قوی، الحاق کریمه، درگیری اوکراین و تأثیر بر ژئوپلیتیک جهانی.",
            
            "xi jinping": "Xi Jinping - President of China since 2013. Born June 15, 1953. General Secretary of the Communist Party. Known for Belt and Road Initiative, economic reforms, and making China a global superpower.",
            "شی جین پینگ": "شی جین پینگ - رئیس‌جمهور چین از سال ۲۰۱۳. متولد ۱۵ ژوئن ۱۹۵۳. دبیرکل حزب کمونیست. معروف به ابتکار کمربند و جاده، اصلاحات اقتصادی و تبدیل چین به ابرقدرت جهانی.",
            
            "emmanuel macron": "Emmanuel Macron - President of France since 2017. Born December 21, 1977. Former investment banker. Known for pro-EU stance, economic reforms, and climate change advocacy.",
            "امانوئل ماکرون": "امانوئل ماکرون - رئیس‌جمهور فرانسه از سال ۲۰۱۷. متولد ۲۱ دسامبر ۱۹۷۷. بانکدار سابق سرمایه‌گذاری. معروف به موضع طرفدار اتحادیه اروپا، اصلاحات اقتصادی و دفاع از تغییرات اقلیمی.",
            
            "boris johnson": "Boris Johnson - Former UK Prime Minister (2019-2022). Born June 19, 1964. Led Brexit process. Known for charismatic leadership style and controversial decisions.",
            "باریس جانسون": "باریس جانسون - نخست‌وزیر سابق بریتانیا (۲۰۱۹-۲۰۲۲). متولد ۱۹ ژوئن ۱۹۶۴. فرآیند برگزیت را رهبری کرد. معروف به سبک رهبری کاریزماتیک و تصمیمات بحث‌برانگیز.",
            
            "angela merkel": "Angela Merkel - Former Chancellor of Germany (2005-2021). Born July 17, 1954. Known as 'leader of the free world' and steady leadership during crises. Longest-serving German head of government.",
            "آنگلا مرکل": "آنگلا مرکل - صدراعظم سابق آلمان (۲۰۰۵-۲۰۲). متولد ۱۷ ژوئیه ۱۹۵۴. معروف به 'رهبر جهان آزاد' و رهبری ثابت در بحران‌ها. طولانی‌ترین دوره خدمت به عنوان رئیس دولت آلمان.",
            
            # Crypto Founders
            "satoshi nakamoto": "Satoshi Nakamoto - Pseudonymous creator of Bitcoin (2009). Identity unknown. Estimated to own ~1 million BTC (~$80 billion). Disappeared in 2011. Considered the father of cryptocurrency.",
            "ساتوشی ناکاموتو": "ساتوشی ناکاموتو - خالق ناشناس بیت‌کوین (۲۰۰۹). هویت واقعی ناشناخته. تخمین زده می‌شود حدود ۱ میلیون BTC (~۸۰ میلیارد دلار) داشته باشد. در سال ۲۱۱ ناپدید شد. پدر ارز دیجیتال محسوب می‌شود.",
            
            "vitalik buterin": "Vitalik Buterin - Co-founder of Ethereum (2015). Born January 31, 1994 in Russia. Known for smart contracts, blockchain innovation, and decentralized applications. Youngest crypto billionaire.",
            "ویتالیک بوترین": "ویتالیک بوترین - هم‌بنیانگذار اتریوم (۰۱۵). متولد ۳۱ ژانویه ۱۹۴ در روسیه. معروف به قراردادهای هوشمند، نوآوری بلاکچین و برنامه‌های غیرمتمرکز. جوان‌ترین میلیاردر کریپتو.",
            
            # Business Leaders
            "jeff bezos": "Jeff Bezos - Founder of Amazon (1994). Born January 12, 1964. One of the world's richest people (Net worth: ~$200 billion). Also owns Blue Origin space company and The Washington Post.",
            "جف بزوس": "جف بزوس - بنیانگذار آمازون (۱۹۹۴). متولد ۱۲ ژانویه ۹۶۴. یکی از ثروتمندترین افراد جهان (ثروت خالص: ~۲۰۰ میلیارد دلار). همچنین مالک شرکت فضایی Blue Origin و روزنامه Washington Post.",
            
            "bill gates": "Bill Gates - Co-founder of Microsoft (1975). Born October 28, 1955. Philanthropist through Bill & Melinda Gates Foundation. Focus on global health, education, and climate change. Net worth: ~$130 billion.",
            "بیل گیتس": "بیل گیتس - هم‌بنیانگذار مایکروسافت (۱۹۷۵). متولد ۲۸ اکتبر ۱۹۵۵. خیر از طریق بنیاد بیل و ملیندا گیتس. تمرکز بر سلامت جهانی، آموزش و تغییرات اقلیمی. ثروت خالص: ~۱۳۰ میلیارد دلار.",
            
            "steve jobs": "Steve Jobs (1955-2011) - Co-founder of Apple. Revolutionized personal computing, music (iPod), and mobile phones (iPhone). Known for innovation and design excellence. Died from pancreatic cancer.",
            "استیو جابز": "استیو جابز (۱۹۵۵-۲۰۱۱) - هم‌بنیانگذار اپل. انقلاب در رایانش شخصی، موسیقی (iPod) و تلفن‌های همراه (iPhone). معروف به نوآوری و برتری در طراحی. از سرطان لوزالمعده درگذشت.",
            
            "mark zuckerberg": "Mark Zuckerberg - Founder and CEO of Meta (Facebook). Born May 14, 1984. Known for social media, metaverse vision, and connecting billions of people. Net worth: ~$120 billion.",
            "مارک زاکربرگ": "مارک زاکربرگ - بنیانگذار و مدیرعامل متا (فیسبوک). متولد ۱۴ مه ۱۹۸۴. معروف به شبکه‌های اجتماعی، چشم‌انداز متاورس و اتصال میلیاردها نفر. ثروت خالص: ~۱۲۰ میلیارد دلار.",
            
            "tim cook": "Tim Cook - CEO of Apple since 2011. Born November 1, 1960. Succeeded Steve Jobs. Known for supply chain expertise, Apple's continued innovation, and privacy advocacy.",
            "تیم کوک": "تیم کوک - مدیرعامل اپل از ۲۰۱۱. متولد ۱ نوامبر ۱۹۶۰. جانشین استیو جابز. معروف به تخصص زنجیره تأمین، نوآوری مستمر اپل و دفاع از حریم خصوصی.",
            
            "warren buffett": "Warren Buffett - 'Oracle of Omaha'. Born August 30, 1930. One of the most successful investors ever. CEO of Berkshire Hathaway. Known for value investing and long-term strategy. Net worth: ~$120 billion.",
            "وارن بافت": "وارن بافت - 'پیشگوی اوماها'. متولد ۳۰ اوت ۹۳۰. یکی از موفق‌ترین سرمایه‌گذاران تاریخ. مدیرعامل برکشایر هاتاوی. معروف به سرمایه‌گذاری ارزشی و استراتژی بلندمدت. ثروت خالص: ~۱۲۰ میلیارد دلار.",
            
            # Central Bankers
            "jerome powell": "Jerome Powell - Chair of the Federal Reserve since 2018. Born February 4, 1953. Controls US monetary policy and interest rates. Major impact on global markets, inflation control, and economic stability.",
            "جروم پاول": "جروم پاول - رئیس فدرال رزرو از ۲۰۱۸. متولد ۴ فوریه ۱۵۳. کنترل سیاست پولی و نرخ بهره آمریکا. تأثیر بزرگ بر بازارهای جهانی، کنترل تورم و ثبات اقتصادی.",
            
            # More People
            "christine lagarde": "Christine Lagarde - President of European Central Bank (ECB) since 2019. Born January 1, 1956. Former IMF Managing Director. Known for economic expertise and leadership.",
            "کریستین لاگارد": "کریستین لاگارد - رئیس بانک مرکزی اروپا (ECB) از ۲۰۱۹. متولد ۱ ژانویه ۱۹۵۶. مدیرعامل سابق صندوق بین‌المللی پول. معروف به تخصص اقتصادی و رهبری.",
            
            "andrew bailey": "Andrew Bailey - Governor of the Bank of England since 2020. Born 1959. Controls UK monetary policy and interest rates.",
            "اندرو بیلی": "اندرو بیلی - فرماندار بانک انگلستان از ۲۰۲۰. متولد ۱۹۵۹. کنترل سیاست پولی و نرخ بهره بریتانیا.",
        }
    
    def _load_crypto_info(self):
        """Load cryptocurrency information."""
        return {
            "bitcoin": "Bitcoin (BTC) - First cryptocurrency, created 2009 by Satoshi Nakamoto. Max supply: 21 million. Store of value, digital gold. Current market cap: ~$1.5 trillion.",
            "btc": "Bitcoin (BTC) - First cryptocurrency, created 2009. Max supply: 21M. Digital gold. Market cap: ~$1.5T.",
            "ethereum": "Ethereum (ETH) - Smart contract platform, created 2015 by Vitalik Buterin. Powers DeFi, NFTs, dApps. Second-largest crypto. Market cap: ~$400 billion.",
            "eth": "Ethereum (ETH) - Smart contract platform (2015). Powers DeFi, NFTs. Market cap: ~$400B.",
            "dogecoin": "Dogecoin (DOGE) - Meme coin created 2013 by Billy Markus & Jackson Palmer as a joke. Gained popularity through Elon Musk's support. Market cap: ~$10 billion.",
            "doge": "Dogecoin (DOGE) - Meme coin (2013). Popularized by Elon Musk. Market cap: ~$10B.",
            "solana": "Solana (SOL) - High-speed blockchain, 65,000 TPS. Known for low fees and fast transactions. Created 2020. Market cap: ~$80 billion.",
            "sol": "Solana (SOL) - High-speed blockchain (65k TPS). Low fees. Market cap: ~$80B.",
            "cardano": "Cardano (ADA) - Research-driven blockchain, founded by Charles Hoskinson (2017). Focus on sustainability and peer-reviewed development. Market cap: ~$15 billion.",
            "ada": "Cardano (ADA) - Research-driven blockchain (2017). Market cap: ~$15B.",
            "ripple": "XRP - Digital payment protocol by Ripple Labs. Fast cross-border transactions. Created 2012. Market cap: ~$30 billion.",
            "xrp": "XRP - Digital payment protocol. Fast cross-border transactions. Market cap: ~$30B.",
            "polkadot": "Polkadot (DOT) - Multi-chain protocol by Gavin Wood (2020). Enables blockchain interoperability. Market cap: ~$10 billion.",
            "dot": "Polkadot (DOT) - Multi-chain protocol. Blockchain interoperability. Market cap: ~$10B.",
            "litecoin": "Litecoin (LTC) - Created 2011 by Charlie Lee. 'Silver to Bitcoin's gold'. Faster transactions than BTC. Market cap: ~$5 billion.",
            "ltc": "Litecoin (LTC) - 'Silver to Bitcoin's gold' (2011). Market cap: ~$5B.",
            "binance coin": "BNB - Binance's native token. Used for trading fee discounts and BSC ecosystem. Created 2017. Market cap: ~$90 billion.",
            "bnb": "BNB - Binance native token. Trading fee discounts. Market cap: ~$90B.",
            "avalanche": "Avalanche (AVAX) - High-throughput smart contract platform. Sub-second finality. Created 2020. Market cap: ~$15 billion.",
            "avax": "Avalanche (AVAX) - High-throughput platform. Market cap: ~$15B.",
            "chainlink": "Chainlink (LINK) - Decentralized oracle network. Connects smart contracts to real-world data. Created 2017. Market cap: ~$10 billion.",
            "link": "Chainlink (LINK) - Decentralized oracle network. Market cap: ~$10B.",
            "polygon": "Polygon (MATIC) - Ethereum scaling solution. Layer 2 network. Fast, low-cost transactions. Market cap: ~$8 billion.",
            "matic": "Polygon (MATIC) - Ethereum L2 scaling. Market cap: ~$8B.",
            "uniswap": "Uniswap (UNI) - Decentralized exchange (DEX) protocol. Automated market maker. Created 2018. Market cap: ~$5 billion.",
            "uni": "Uniswap (UNI) - DEX protocol. AMM. Market cap: ~$5B.",
            "gold": "Gold (XAU) - Precious metal, safe-haven asset. Price influenced by inflation, geopolitics, dollar strength. Current price: ~$2,000/oz.",
            "silver": "Silver (XAG) - Precious metal, industrial use. More volatile than gold. Current price: ~$25/oz.",
        }
    
    def _load_forex_info(self):
        """Load forex information."""
        return {
            "eur/usd": "EUR/USD - Euro vs US Dollar. Most traded currency pair. Represents 24% of daily forex volume. Current rate: ~1.08",
            "eur": "EUR/USD - Euro vs US Dollar. Most traded pair. 24% of forex volume. Rate: ~1.08",
            "gbp/usd": "GBP/USD - British Pound vs US Dollar. Known as 'Cable'. Major pair. Current rate: ~1.27",
            "gbp": "GBP/USD - British Pound vs USD. 'Cable'. Rate: ~1.27",
            "usd/jpy": "USD/JPY - US Dollar vs Japanese Yen. Second most traded pair. Safe-haven currency. Rate: ~150",
            "jpy": "USD/JPY - USD vs Japanese Yen. Safe-haven. Rate: ~150",
            "usd/chf": "USD/CHF - US Dollar vs Swiss Franc. Safe-haven pair. Rate: ~0.88",
            "chf": "USD/CHF - USD vs Swiss Franc. Safe-haven. Rate: ~0.88",
            "aud/usd": "AUD/USD - Australian Dollar vs US Dollar. Commodity currency. Rate: ~0.66",
            "aud": "AUD/USD - Australian Dollar vs USD. Commodity currency. Rate: ~0.66",
            "usd/cad": "USD/CAD - US Dollar vs Canadian Dollar. 'Loonie'. Commodity currency. Rate: ~1.36",
            "cad": "USD/CAD - USD vs Canadian Dollar. 'Loonie'. Rate: ~1.36",
            "nzd/usd": "NZD/USD - New Zealand Dollar vs US Dollar. 'Kiwi'. Commodity currency. Rate: ~0.61",
            "nzd": "NZD/USD - NZ Dollar vs USD. 'Kiwi'. Rate: ~0.61",
        }
    
    def _load_general_knowledge(self):
        """Load general knowledge."""
        return {
            "inflation": "Inflation is the rate at which prices rise, reducing purchasing power. Central banks control it through interest rates. Target: 2% annually. High inflation erodes savings; deflation slows economy.",
            "تورم": "تورم نرخی است که قیمت‌ها افزایش می‌یابند و قدرت خرید کاهش می‌یابد. بانک‌های مرکزی آن را از طریق نرخ بهره کنترل می‌کنند. هدف: ۲٪ سالانه. تورم بالا پس‌انداز را از بین می‌برد؛ تورم منفی اقتصاد را کند می‌کند.",
            "interest rate": "Interest rate is the cost of borrowing money. Central banks (like Federal Reserve) set rates to control inflation and economic growth. Higher rates strengthen currency but slow economy.",
            "نرخ بهره": "نرخ بهره هزینه قرض گرفتن پول است. بانک‌های مرکزی (مثل فدرال رزرو) نرخ‌ها را برای کنترل تورم و رشد اقتصادی تعیین می‌کنند. نرخ بالاتر ارز را تقویت می‌کند اما اقتصاد را کند می‌کند.",
            "gdp": "GDP (Gross Domestic Product) measures a country's economic output. Higher GDP = stronger economy. Used to compare economic performance between countries.",
            "تولید ناخالص داخلی": "GDP (تولید ناخالص داخلی) خروجی اقتصادی یک کشور را اندازه‌گیری می‌کند. GDP بالاتر = اقتصاد قوی‌تر. برای مقایسه عملکرد اقتصادی بین کشورها استفاده می‌شود.",
            "recession": "Recession is a significant decline in economic activity (GDP falls for 2+ consecutive quarters). Causes job losses, reduced spending. Central banks try to prevent through monetary policy.",
            "رکود": "رکود کاهش قابل توجه در فعالیت اقتصادی است (GDP برای ۲+ فصل متوالی کاهش می‌یابد). باعث از دست دادن شغل و کاهش هزینه می‌شود. بانک‌های مرکزی سعی می‌کنند از طریق سیاست پولی از آن جلوگیری کنند.",
            "bull market": "Bull market is when prices rise consistently (20%+ from recent low). Investor confidence is high. Characterized by optimism and economic growth.",
            "بازار گاوی": "بازار گاوی زمانی است که قیمت‌ها به طور مداوم افزایش می‌یابند (۲۰٪+ از کف اخیر). اعتماد سرمایه‌گذاران بالاست. با خوش‌بینی و رشد اقتصادی مشخص می‌شود.",
            "bear market": "Bear market is when prices fall consistently (20%+ from recent high). Investor confidence is low. Characterized by pessimism and economic slowdown.",
            "بازار خرسی": "بازار خرسی زمانی است که قیمت‌ها به طور مداوم کاهش می‌یابند (۰٪+ از سقف اخیر). اعتماد سرمایه‌گذاران پایین است. با بدبینی و کندی اقتصادی مشخص می‌شود.",
            "blockchain": "Blockchain is a decentralized digital ledger. Records transactions across many computers. Immutable, transparent, secure. Foundation of cryptocurrencies like Bitcoin and Ethereum.",
            "بلاکچین": "بلاکچین یک دفتر کل دیجیتال غیرمتمرکز است. تراکنش‌ها را در بسیاری از کامپیوترها ثبت می‌کند. تغییرناپذیر، شفاف، امن. پایه ارزهای دیجیتال مانند بیت‌کوین و اتریوم.",
            "defi": "DeFi (Decentralized Finance) - Financial services without intermediaries (banks). Built on blockchain. Includes lending, borrowing, trading. Examples: Uniswap, Aave, Compound.",
            "دیفای": "DeFi (امور مالی غیرمتمرکز) - خدمات مالی بدون واسطه (بانک‌ها). بر بلاکچین ساخته شده. شامل وام‌دهی، وام‌گیری، معامله. مثال‌ها: Uniswap، Aave، Compound.",
            "nft": "NFT (Non-Fungible Token) - Unique digital asset on blockchain. Represents ownership of digital items (art, music, videos). Cannot be replicated. Built on Ethereum mostly.",
            "ان‌اف‌تی": "NFT (توکن غیرقابل تعویض) - دارایی دیجیتال منحصر به فرد بر بلاکچین. مالکیت اقلام دیجیتال (هنر، موسیقی، ویدیو) را نشان می‌دهد. نمی‌توان تکثیر کرد. بیشتر بر اتریوم ساخته می‌شود.",
        }
    
    def _load_responses(self):
        """Load response patterns."""
        return [
            # Greetings
            {"patterns": ["hello", "hi", "hey", "سلام", "درود", "صبح بخیر", "عصر بخیر", "good morning", "good evening", "how are you", "چطوری", "حالت چطوره", "خوبی"],
             "responses": {"en": f"Hello! I'm {self.name} v{self.version}, your intelligent market assistant. How can I help you today? 🤖",
                          "fa": f"سلام! من {self.name} نسخه {self.version} هستم، دستیار هوشمند بازار شما. چطور می‌تونم کمکتون کنم؟ 🤖"}},
            
            # Identity
            {"patterns": ["your name", "who are you", "what are you", "اسمت چیه", "کی هستی", "چی هستی", "نام تو", "نام شما", "you are", "تو کی هستی"],
             "responses": {"en": f"I'm {self.name} v{self.version}, an AI-powered market analysis assistant created by {self.creator} in {self.created_date}. I help with crypto, forex, gold prices, predictions, world capitals, famous people, and much more! 🤖",
                          "fa": f"من {self.name} نسخه {self.version} هستم، یک دستیار تحلیل بازار مبتنی بر AI که توسط {self.creator} در {self.created_date} ساخته شدم. در کریپتو، فارکس، طلا، پیش‌بینی‌ها، پایتخت‌های جهان، افراد مشهور و خیلی چیزهای دیگر کمک می‌کنم! 🤖"}},
            
            # Creator
            {"patterns": ["creator", "who made you", "who created you", "your developer", "سازنده تو", "کی تو رو ساخته", "توسعه دهنده تو", "سازنده ات", "سازندت", "سازنده تو کی", "تو رو کی ساخته", "created by", "made by"],
             "responses": {"en": f"I was created by {self.creator}, a talented developer and AI engineer. He built me to be the most powerful market analysis platform in the world with advanced AI capabilities! 🚀",
                          "fa": f"من توسط {self.creator} ساخته شدم، یک توسعه‌دهنده و مهندس AI با استعداد. او من را ساخت تا قوی‌ترین پلتفرم تحلیل بازار در جهان با قابلیت‌های پیشرفته AI باشم! 🚀"}},
            
            # Capital queries
            {"patterns": ["capital", "پایتخت", "capital of", "paytakht", "پایتخت کجاست", "پایتخت چیست"],
             "responses": {"en": "I know all world capitals! Ask me about any country. For example: 'What is the capital of Iran?' or 'Capital of France?' or 'پایتخت ایران' 🌍",
                          "fa": "من همه پایتخت‌های جهان را می‌دانم! درباره هر کشوری بپرسید. مثلاً: 'پایتخت ایران چیست؟' یا 'Capital of France?' 🌍"}},
            
            # Famous people
            {"patterns": ["who is", "who was", "tell me about", "معرفی کن", "کی بود", "کیه", "درباره", "اطلاعات درباره", "information about"],
             "responses": {"en": "I know many famous people! Ask about politicians, entrepreneurs, historical figures, or crypto founders. Try: 'Who is Napoleon?' or 'Tell me about Elon Musk' or 'مارکو روبیو' 👤",
                          "fa": "من افراد مشهور زیادی را می‌شناسم! درباره سیاستمداران، کارآفرینان، شخصیت‌های تاریخی یا بنیانگذاران کریپتو بپرسید. امتحان کنید: 'ناپلئون کی بود؟' یا 'درباره ایلان ماسک' یا 'Marco Rubio' 👤"}},
            
            # Market prices
            {"patterns": ["price", "قیمت", "how much", "چقدر", "rate", "نرخ", "current price", "قیمت فعلی"],
             "responses": {"en": "Check real-time prices on the dashboard! Select any asset from the search bar. Prices update every 3 seconds from Binance API! 📊",
                          "fa": "قیمت‌های لحظه‌ای را در داشبورد ببینید! هر دارایی را از نوار جستجو انتخاب کنید. قیمت‌ها هر ۳ ثانیه از API بایننس به‌روز می‌شوند! 📊"}},
            
            # Buy/Sell signals
            {"patterns": ["buy", "sell", "خرید", "فروش", "should i buy", "بخرم", "بفروشم", "trading signal", "سیگنال"],
             "responses": {"en": "Check the 'Trading Signal' card! It shows BUY/SELL/HOLD based on RSI and Moving Averages with confidence percentage. Always do your own research! ⚠️",
                          "fa": "کارت 'سیگنال معاملاتی' را بررسی کنید! بر اساس RSI و میانگین متحرک با درصد اطمینان BUY/SELL/HOLD نشان می‌دهد. همیشه تحقیق خودتان را انجام دهید! ⚠️"}},
            
            # Crypto specific
            {"patterns": ["bitcoin", "btc", "بیت کوین", "بیت‌کوین"],
             "responses": {"en": self.crypto_info["bitcoin"], "fa": self.crypto_info.get("bitcoin", "Bitcoin - First cryptocurrency, created 2009.")}},
            {"patterns": ["ethereum", "eth", "اتریوم"],
             "responses": {"en": self.crypto_info["ethereum"], "fa": self.crypto_info.get("ethereum", "Ethereum - Smart contract platform, 2015.")}},
            {"patterns": ["dogecoin", "doge", "دوج کوین"],
             "responses": {"en": self.crypto_info["dogecoin"], "fa": self.crypto_info.get("dogecoin", "Dogecoin - Meme coin, 2013.")}},
            
            # Gold
            {"patterns": ["gold", "طلا", "xau"],
             "responses": {"en": self.crypto_info.get("gold", "Gold - Safe-haven asset, ~$2,000/oz"), 
                          "fa": "طلا (XAU) - دارایی امن، حدود ۲,۰۰۰ دلار/اونس. تحت تأثیر تورم، ژئوپلیتیک، قدرت دلار. "}},
            
            # Help
            {"patterns": ["help", "کمک", "راهنما", "guide", "what can you do", "چه کارایی داری"],
             "responses": {"en": f"I can help with:\n📊 Market prices & predictions\n🌍 World capitals & geography\n👤 Famous people (Napoleon, Marco Rubio, Elon Musk, etc.)\n Crypto & forex info\n📅 Calendar events\n📰 Global news\n General knowledge (inflation, GDP, blockchain)\nJust ask! I'm here 24/7! 🤖",
                          "fa": f"می‌تونم کمک کنم با:\n📊 قیمت‌ها و پیش‌بینی‌های بازار\n🌍 پایتخت‌ها و جغرافیا\n👤 افراد مشهور (ناپلئون، مارکو روبیو، ایلان ماسک و...)\n اطلاعات کریپتو و فارکس\n📅 رویدادهای تقویم\n📰 اخبار جهانی\n🧮 دانش عمومی (تورم، GDP، بلاکچین)\nفقط بپرسید! من ۲۴/۷ اینجا هستم! 🤖"}},
            
            # Thanks
            {"patterns": ["thanks", "thank you", "ممنون", "مرسی", "تشکر", "سپاس", "متشکرم", "لطف داری"],
             "responses": {"en": "You're welcome! Happy trading! May your profits be endless! 🚀💰",
                          "fa": "خواهش می‌کنم! معامله موفق! امیدوارم سودهای بی‌پایان داشته باشید! 🚀💰"}},
            
            # Calendar
            {"patterns": ["calendar", "تقویم", "event", "رویداد", "holiday", "تعطیل"],
             "responses": {"en": "Check the Global Events Calendar! Shows Gregorian & Persian dates with market-impacting events like FOMC meetings, elections, and holidays. 📅",
                          "fa": "تقویم رویدادهای جهانی را بررسی کنید! تاریخ میلادی و شمسی با رویدادهای تأثیرگذار بر بازار مانند جلسات FOMC، انتخابات و تعطیلات. 📅"}},
            
            # News
            {"patterns": ["news", "اخبار", "latest news", "اخبار جدید"],
             "responses": {"en": "Check the News Feed for latest updates from Trump, Musk, Federal Reserve in English & Persian! 📰",
                          "fa": "بخش اخبار را برای آخرین به‌روزرسانی‌ها از ترامپ، ماسک، فدرال رزرو به انگلیسی و فارسی ببینید! 📰"}},
            
            # Prediction
            {"patterns": ["predict", "forecast", "پیش بینی", "future price", "قیمت آینده", "where will it go"],
             "responses": {"en": "AI predicts using Moving Average & RSI. Check 'AI Prediction' card and purple dashed line for 7-day forecast! Remember: predictions are not guarantees! 🔮",
                          "fa": "AI با میانگین متحرک و RSI پیش‌بینی می‌کند. کارت 'پیش‌بینی AI' و خط نقطه‌چین بنفش برای پیش‌بینی ۷ روزه! به یاد داشته باشید: پیش‌بینی‌ها تضمین نیستند! 🔮"}},
            
            # RSI
            {"patterns": ["rsi", "شاخص قدرت", "relative strength"],
             "responses": {"en": "RSI (Relative Strength Index) - Above 70: overbought (sell signal), Below 30: oversold (buy signal). Shown on dashboard! 📊",
                          "fa": "RSI (شاخص قدرت نسبی) - بالای ۷۰: اشباع خرید (سیگنال فروش)، زیر ۳: اشباع فروش (سیگنال خرید). در داشبورد! 📊"}},
            
            # Inflation
            {"patterns": ["inflation", "تورم"],
             "responses": {"en": self.general_knowledge["inflation"], "fa": self.general_knowledge["تورم"]}},
            
            # Interest rate
            {"patterns": ["interest rate", "نرخ بهره"],
             "responses": {"en": self.general_knowledge["interest rate"], "fa": self.general_knowledge["نرخ بهره"]}},
            
            # GDP
            {"patterns": ["gdp", "تولید ناخالص", "gross domestic product"],
             "responses": {"en": self.general_knowledge["gdp"], "fa": self.general_knowledge["تولید ناخالص داخلی"]}},
            
            # Recession
            {"patterns": ["recession", "رکود"],
             "responses": {"en": self.general_knowledge["recession"], "fa": self.general_knowledge["رکود"]}},
            
            # Bull/Bear market
            {"patterns": ["bull market", "بازار گاوی", "bear market", "بازار خرسی"],
             "responses": {"en": "Bull market = prices rising (optimism). Bear market = prices falling 20%+ (pessimism). Check signals on dashboard! 📈📉",
                          "fa": "بازار گاوی = قیمت‌ها در حال افزایش (خوش‌بینی). بازار خرسی = قیمت‌ها ۲۰٪+ کاهش (بدبینی). سیگنال‌ها را در داشبورد بررسی کنید! 📈📉"}},
            
            # Blockchain
            {"patterns": ["blockchain", "بلاکچین"],
             "responses": {"en": self.general_knowledge["blockchain"], "fa": self.general_knowledge["بلاکچین"]}},
            
            # DeFi
            {"patterns": ["defi", "دیفای", "decentralized finance"],
             "responses": {"en": self.general_knowledge["defi"], "fa": self.general_knowledge["دیفای"]}},
            
            # NFT
            {"patterns": ["nft", "ان‌اف‌تی", "non-fungible token"],
             "responses": {"en": self.general_knowledge["nft"], "fa": self.general_knowledge["ان‌اف‌تی"]}},
            
            # Forex pairs
            {"patterns": ["eur/usd", "eur usd", "یورو دلار"],
             "responses": {"en": self.forex_info.get("eur/usd", "EUR/USD - Most traded pair. Rate: ~1.08"), 
                          "fa": "EUR/USD - یورو در برابر دلار. پرمعامله‌ترین جفت‌ارز. نرخ: ~۱.۰۸"}},
            {"patterns": ["gbp/usd", "gbp usd", "پوند دلار"],
             "responses": {"en": self.forex_info.get("gbp/usd", "GBP/USD - 'Cable'. Rate: ~1.27"),
                          "fa": "GBP/USD - پوند در برابر دلار. معروف به 'Cable'. نرخ: ~۱.۲۷"}},
            {"patterns": ["usd/jpy", "usd jpy", "دلار ین"],
             "responses": {"en": self.forex_info.get("usd/jpy", "USD/JPY - Second most traded. Safe-haven. Rate: ~150"),
                          "fa": "USD/JPY - دلار در برابر ین ژاپن. دومین پرمعامله‌ترین. ارز امن. نرخ: ~۱۵"}},
        ]
    
    def detect_language(self, message: str) -> str:
        """Detect if message is Persian or English."""
        persian_chars = re.findall(r'[\u0600-\u06FF]', message)
        return "fa" if len(persian_chars) > len(message) * 0.3 else "en"
    
    def get_response(self, message: str) -> str:
        """Get response based on user message - with memory."""
        message_lower = message.lower().strip()
        lang = self.detect_language(message)
        
        # Save to history
        self.conversation_history.append({
            "role": "user", 
            "message": message, 
            "time": datetime.now().isoformat(),
            "language": lang
        })
        
        if not message_lower:
            response = "Please type a message! 💬" if lang == "en" else "لطفاً پیامی تایپ کنید! 💬"
            self.conversation_history.append({"role": "bot", "message": response, "time": datetime.now().isoformat()})
            self._save_memory()
            return response
        
        # Check for capital city queries
        for country_key, capital_info in self.capitals.items():
            if country_key in message_lower:
                response = f"The capital of {capital_info['country']} is {capital_info['capital']}! 🌍" if lang == "en" else f"پایتخت {capital_info['country']} {capital_info['capital']} است! "
                self.conversation_history.append({"role": "bot", "message": response, "time": datetime.now().isoformat()})
                self._save_memory()
                return response
        
        # Check for famous people
        for person_key, person_info in self.famous_people.items():
            if person_key in message_lower:
                response = person_info
                self.conversation_history.append({"role": "bot", "message": response, "time": datetime.now().isoformat()})
                self._save_memory()
                return response
        
        # Check for crypto info
        for crypto_key, crypto_info in self.crypto_info.items():
            if crypto_key in message_lower:
                response = crypto_info
                self.conversation_history.append({"role": "bot", "message": response, "time": datetime.now().isoformat()})
                self._save_memory()
                return response
        
        # Check for forex info
        for forex_key, forex_info in self.forex_info.items():
            if forex_key in message_lower:
                response = forex_info
                self.conversation_history.append({"role": "bot", "message": response, "time": datetime.now().isoformat()})
                self._save_memory()
                return response
        
        # Check for general knowledge
        for topic_key, topic_info in self.general_knowledge.items():
            if topic_key in message_lower:
                response = topic_info
                self.conversation_history.append({"role": "bot", "message": response, "time": datetime.now().isoformat()})
                self._save_memory()
                return response
        
        # Check pattern responses
        for category in self.responses:
            for pattern in category["patterns"]:
                if pattern and pattern in message_lower:
                    response = category["responses"].get(lang, category["responses"]["en"])
                    self.conversation_history.append({"role": "bot", "message": response, "time": datetime.now().isoformat()})
                    self._save_memory()
                    return response
        
        # Default response
        default_en = "I'm not sure about that. Try asking about:\n• World capitals (e.g., 'capital of Iran')\n• Famous people (e.g., 'Who is Napoleon?' or 'Marco Rubio')\n• Crypto info (Bitcoin, Ethereum, etc.)\n• Forex pairs (EUR/USD, GBP/USD)\n• Market prices & predictions\n• Or type 'help' for more options! 🤖"
        default_fa = "مطمئن نیستم. امتحان کنید:\n• پایتخت‌های جهان (مثلاً 'پایتخت ایران')\n• افراد مشهور (مثلاً 'ناپلئون کی بود؟' یا 'مارکو روبیو')\n• اطلاعات کریپتو (بیت‌کوین، اتریوم و...)\n• جفت‌ارزها (EUR/USD, GBP/USD)\n• قیمت‌ها و پیش‌بینی‌های بازار\n• یا 'help' را تایپ کنید! 🤖"
        
        default = default_fa if lang == "fa" else default_en
        self.conversation_history.append({"role": "bot", "message": default, "time": datetime.now().isoformat()})
        self._save_memory()
        return default
    
    def get_history(self):
        """Get conversation history."""
        return self.conversation_history[-20:]  
    
    def clear_memory(self):
        """Clear conversation history."""
        self.conversation_history = []
        self._save_memory()
        return "Memory cleared! 🧹"
