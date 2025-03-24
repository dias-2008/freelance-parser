# Excel file path for storing job listings
EXCEL_FILE = "data/freelance_jobs.xlsx"

# Time interval between parsing runs (in seconds)
PARSING_INTERVAL = 3600  # 1 hour

# FL.ru credentials
FLRU_LOGIN = "your_email@example.com"
FLRU_PASSWORD = "your_password"

# Kwork credentials
KWORK_LOGIN = "your_email@example.com"
KWORK_PASSWORD = "your_password"

# Freelancehunt credentials
FREELANCEHUNT_TOKEN = "your_api_token"

# Keywords for job filtering (optional)
KEYWORDS = [
    "python",
    "django",
    "flask",
    "fastapi",
    "web scraping",
    "automation"
]

# Excluded keywords (optional)
EXCLUDED_KEYWORDS = [
    "wordpress",
    "php"
]

# Minimum price filter (optional, in USD)
MIN_PRICE = 50