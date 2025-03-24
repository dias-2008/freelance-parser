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

# Keywords to filter jobs
KEYWORDS = [
    # Python and frameworks
    'python', 'django', 'flask', 'fastapi', 'selenium', 'scrapy', 
    'pandas', 'numpy', 'pytorch', 'tensorflow', 'asyncio', 'beautifulsoup', 
    'openai', 'langchain',

    # Data and automation
    'parsing', 'scraping', 'scraper', 'crawler', 'automation', 'bot', 
    'task automation', 'browser automation', 'ETL', 'data analysis', 
    'machine learning', 'AI', 'AI bot',

    # Web
    'backend', 'api', 'rest api', 'web scraping', 'database', 'json api', 
    'webhook',

    # Bots & Chatbots
    'telegram bot', 'discord bot', 'chatbot'
]
