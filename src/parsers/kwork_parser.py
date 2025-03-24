from typing import List
from .base_parser import BaseParser, JobPost
import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime

class KworkParser(BaseParser):
    BASE_URL = "https://kwork.ru/projects"

    async def parse(self) -> List[JobPost]:
        jobs = []
        async with aiohttp.ClientSession() as session:
            async with session.get(self.BASE_URL) as response:
                if response.status == 200:
                    soup = BeautifulSoup(await response.text(), 'html.parser')
                    projects = soup.find_all('div', class_='card__content')
                    
                    for project in projects:
                        title = project.find('div', class_='wants-card__header-title').text.strip()
                        description = project.find('div', class_='wants-card__description-text').text.strip()
                        
                        if self.filter_job(title, description):
                            price = project.find('div', class_='wants-card__header-price').text.strip()
                            url = f"https://kwork.ru{project.find('a')['href']}"
                            published_date = datetime.now()  # Kwork doesn't show exact time, using current time
                            
                            jobs.append(JobPost(
                                title=title,
                                description=description,
                                price=price,
                                client_name=None,
                                url=url,
                                published_date=published_date,
                                platform=self.platform_name
                            ))
        
        return jobs