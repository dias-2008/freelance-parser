from typing import List
from .base_parser import BaseParser, JobPost
import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import FLRU_LOGIN, FLRU_PASSWORD

class FLRuParser(BaseParser):
    BASE_URL = "https://www.fl.ru/projects/"
    LOGIN_URL = "https://www.fl.ru/login/"

    async def parse(self) -> List[JobPost]:
        jobs = []
        async with aiohttp.ClientSession() as session:
            # Login first
            if FLRU_LOGIN and FLRU_PASSWORD:
                await self._login(session)
            
            async with session.get(self.BASE_URL) as response:
                if response.status == 200:
                    soup = BeautifulSoup(await response.text(), 'html.parser')
                    projects = soup.find_all('div', class_='b-post')
                    
                    for project in projects:
                        try:
                            title_elem = project.find('h2')
                            desc_elem = project.find('div', class_='b-post__body')
                            
                            if not title_elem or not desc_elem:
                                continue
                                
                            title = title_elem.text.strip()
                            description = desc_elem.text.strip()
                            
                            if self.filter_job(title, description):
                                price_elem = project.find('div', class_='b-post__price')
                                price = price_elem.text.strip() if price_elem else "N/A"
                                
                                url_elem = project.find('a')
                                url = f"https://www.fl.ru{url_elem['href']}" if url_elem else ""
                                
                                client_elem = project.find('div', class_='b-post__client')
                                client = client_elem.text.strip() if client_elem else "Unknown"
                                
                                published_date = datetime.now()
                                
                                jobs.append(JobPost(
                                    title=title,
                                    description=description,
                                    price=price,
                                    client_name=client,
                                    url=url,
                                    published_date=published_date,
                                    platform=self.platform_name
                                ))
                        except Exception as e:
                            logging.error(f"Error parsing FL.ru project: {str(e)}")
                            continue
        
        return jobs

    async def _login(self, session):
        data = {
            'login': FLRU_LOGIN,
            'password': FLRU_PASSWORD
        }
        await session.post(self.LOGIN_URL, data=data)