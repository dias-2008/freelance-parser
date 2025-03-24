from typing import List
from .base_parser import BaseParser, JobPost
import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime
import logging
import os

class FLRuParser(BaseParser):
    BASE_URL = "https://www.fl.ru/projects/"
    LOGIN_URL = "https://www.fl.ru/login/"

    def __init__(self, session: aiohttp.ClientSession):
        super().__init__(session)  # Pass the session argument to the BaseParser
        self.session = session
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
        }

    async def login(self, email: str, password: str) -> bool:
        """Handles login to FL.ru."""
        try:
            async with self.session.get(self.LOGIN_URL, headers=self.headers) as response:
                if response.status != 200:
                    logging.error(f"Failed to load login page: {response.status}")
                    return False
                soup = BeautifulSoup(await response.text(), 'html.parser')
                csrf_token = soup.find('input', {'name': 'csrf_token'})
                if not csrf_token:
                    logging.error("CSRF token not found on login page.")
                    return False

                csrf_token = csrf_token['value']
                payload = {
                    'login': email,
                    'passwd': password,
                    'csrf_token': csrf_token
                }

                async with self.session.post(self.LOGIN_URL, headers=self.headers, data=payload) as login_response:
                    if login_response.status == 200 and "logout" in await login_response.text():
                        logging.info("Successfully logged in to FL.ru.")
                        return True
                    else:
                        logging.error("Login failed - check credentials or website changes.")
                        return False
        except Exception as e:
            logging.error(f"Error during login: {e}", exc_info=True)
            return False

    async def parse(self) -> List[JobPost]:
        """Parses job posts from FL.ru."""
        jobs = []
        try:
            async with self.session.get(self.BASE_URL, headers=self.headers) as response:
                if response.status != 200:
                    logging.error(f"Failed to load projects page: {response.status}")
                    return jobs

                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

                # Save HTML for debugging if needed
                with open("debug_fl.html", "w", encoding="utf-8") as f:
                    f.write(html)

                # Parse job posts
                project_containers = soup.find_all('div', class_='b-post')  # Update selector based on actual HTML
                logging.info(f"Found {len(project_containers)} project containers on FL.ru page.")

                if not project_containers:
                    logging.error("No project containers found on FL.ru page.")
                    return jobs

                for container in project_containers:
                    try:
                        # Debugging: Log raw container HTML
                        logging.debug(f"Raw container HTML: {container}")

                        title_element = container.find('a', class_='b-post__link')
                        if not title_element:
                            logging.warning("Title element not found in job container.")
                            continue

                        title = title_element.text.strip()
                        link = title_element['href'] if title_element.has_attr('href') else None
                        if not link:
                            logging.warning("Link not found for job container.")
                            continue

                        budget_element = container.find('div', class_='b-post__price')
                        budget = budget_element.text.strip() if budget_element else "Not specified"

                        posted_date = datetime.now()  # Adjust if actual date parsing is needed

                        jobs.append(JobPost(
                            title=title,
                            link=f"https://www.fl.ru{link}",
                            budget=budget,
                            posted_date=posted_date
                        ))
                    except Exception as e:
                        logging.warning(f"Error parsing job container: {e}", exc_info=True)

                logging.info(f"Parsed {len(jobs)} jobs from FL.ru.")
        except Exception as e:
            logging.error(f"Error during parsing: {e}", exc_info=True)

        return jobs