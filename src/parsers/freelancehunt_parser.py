from typing import List
from .base_parser import BaseParser, JobPost
import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime

class FreelancehuntParser(BaseParser):
    BASE_URL = "https://freelancehunt.com/projects"

    def __init__(self, session: aiohttp.ClientSession):
        super().__init__(session)  # Pass the session argument to the BaseParser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
        }

    async def parse(self) -> List[JobPost]:
        jobs = []
        
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(self.BASE_URL) as response:
                if response.status == 200:
                    soup = BeautifulSoup(await response.text(), 'html.parser')
                    projects = soup.find_all('div', class_='project-item')
                    
                    for project in projects:
                        title = project.find('a', class_='project-name').text.strip()
                        description = project.find('div', class_='project-description').text.strip()
                        
                        if self.filter_job(title, description):
                            price = project.find('div', class_='price').text.strip()
                            url = f"https://freelancehunt.com{project.find('a', class_='project-name')['href']}"
                            client = project.find('a', class_='customer-name').text.strip()
                            published_date = datetime.now()  # You'll need to parse date_str properly
                            
                            jobs.append(JobPost(
                                title=title,
                                description=description,
                                price=price,
                                client_name=client,
                                url=url,
                                published_date=published_date,
                                platform=self.platform_name
                            ))
        
        return jobs