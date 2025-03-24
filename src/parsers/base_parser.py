from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import KEYWORDS
from utils.proxy_manager import ProxyManager  # Changed from relative to absolute import
from utils.captcha_solver import ManualCaptchaSolver  # Changed from relative to absolute import
import aiohttp

@dataclass
class JobPost:
    title: str
    description: str
    price: str
    client_name: Optional[str]
    url: str
    published_date: datetime
    platform: str

class BaseParser(ABC):
    def __init__(self, session):
        self.session = session
        self.platform_name = self.__class__.__name__.replace('Parser', '')
        self.proxy_manager = ProxyManager()
        self.captcha_solver = ManualCaptchaSolver()

    async def get_session(self) -> aiohttp.ClientSession:
        proxy = self.proxy_manager.get_proxy()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        return aiohttp.ClientSession(headers=headers, proxy=proxy.get('http'))

    async def handle_captcha(self, session: aiohttp.ClientSession, captcha_url: str) -> Optional[str]:
        async with session.get(captcha_url) as response:
            if response.status == 200:
                image_data = await response.read()
                return await self.captcha_solver.solve_captcha(image_data)
        return None

    @abstractmethod
    async def parse(self) -> List[JobPost]:
        """Parse job posts from the platform"""
        pass

    def filter_job(self, title: str, description: str) -> bool:
        """Check if job matches our criteria"""
        text = f"{title} {description}".lower()
        
        # Check if any keyword is present
        has_keyword = any(keyword.lower() in text for keyword in KEYWORDS)
        
        # Exclude unwanted jobs (you can add more exclusion criteria)
        exclusions = ['админ бот', 'модератор']
        has_exclusion = any(excl.lower() in text for excl in exclusions)
        
        return has_keyword and not has_exclusion