from typing import List
from .base_parser import BaseParser, JobPost
import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime

class FreelancehuntParser(BaseParser):
    BASE_URL = "https://freelancehunt.com/projects"

    async def parse(self) -> List[JobPost]:
        jobs = []
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        
        async with aiohttp.ClientSession(headers=headers) as session:
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