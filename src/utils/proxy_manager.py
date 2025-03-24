import aiohttp
import random
from typing import Dict

class ProxyManager:
    def __init__(self):
        self.proxies = [
            'http://proxy1.example.com:8080',
            'http://proxy2.example.com:8080',
        ]
        self.current_proxy = None

    def get_proxy(self) -> Dict[str, str]:
        self.current_proxy = random.choice(self.proxies)
        return {'http': self.current_proxy, 'https': self.current_proxy}

    async def check_proxy(self, proxy: str) -> bool:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.ipify.org', proxy=proxy, timeout=10) as response:
                    return response.status == 200
        except:
            return False