import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# File paths
EXCEL_FILE = Path('data/freelance_jobs.xlsx')

# Parser settings
PARSING_INTERVAL = 5  # minutes

# FL.ru credentials
FLRU_LOGIN = os.getenv('FLRU_LOGIN')
FLRU_PASSWORD = os.getenv('FLRU_PASSWORD')

# Add these lines after FL.ru credentials
KWORK_LOGIN = os.getenv('KWORK_LOGIN')
KWORK_PASSWORD = os.getenv('KWORK_PASSWORD')

# Keywords to filter jobs
KEYWORDS = [
    # Python and frameworks
    'питон', 'python', 'джанго', 'django', 'фласк', 'flask', 'fastapi',
    'селениум', 'selenium', 'скрапи', 'scrapy', 'парсер сайтов',
    'pandas', 'numpy', 'pytorch', 'tensorflow', 'асинхронный', 'asyncio',
    'beautifulsoup', 'парсинг данных', 'чат-гпт', 'openai',

    # Data and automation
    'парсинг', 'парсер', 'скрапинг', 'сбор данных', 'автоматизация',
    'бот', 'программа для сбора', 'автоматизация задач',
    'автоматизация браузера', 'сбор информации', 'анализ данных',
    'машинное обучение', 'искусственный интеллект', 'ии', 'чат бот',

    # Web
    'бэкенд', 'апи', 'rest api', 'парсинг сайта', 'база данных',
    'json апи', 'вебхук', 'разработка бота', 'разработка парсера',
    'создание парсера', 'создание бота',

    # Bots & Chatbots
    'телеграм бот', 'telegram bot', 'бот для телеграм',
    'дискорд бот', 'discord bot', 'бот для дискорд',
    'чатбот', 'создание бота', 'разработка бота телеграм'
]
