import os
import asyncio
import aiohttp
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

# Environment variables
EMAIL = os.getenv("PLP_EMAIL")
PASSWORD = os.getenv("PLP_PASSWORD")

# API Endpoints
LOGIN_URL = "https://api.lms.v2.powerlearnprojectafrica.org/gateway/api/auth/login/student"
POST_URL = "https://api.lms.v2.powerlearnprojectafrica.org/community/api/posts"

# Headers
HEADERS = {
    "Content-Type": "application/json",
    "Origin": "https://academy.powerlearnprojectafrica.org",
    "Referer": "https://academy.powerlearnprojectafrica.org/",
    "User-Agent": "Mozilla/5.0"
}

class PLPAutomation:
    def __init__(self):
        self.token = None
        self.message = "Hello everyone! Let's collaborate on this project: https://github.com/chojuninengu/open-minds-platform.git"
        self.session = None

    async def authenticate(self):
        payload = {"email": EMAIL, "password": PASSWORD}
        async with self.session.post(LOGIN_URL, json=payload, headers=HEADERS) as response:
            if response.status == 200:
                data = await response.json()
                self.token = data.get("token")
                logging.info("Authenticated successfully.")
            else:
                logging.error(f"Authentication failed: {response.status}")
                self.token = None

    async def post_message(self):
        if not self.token:
            await self.authenticate()
            if not self.token:
                return
        headers = {**HEADERS, "Authorization": f"Bearer {self.token}"}
        payload = {"TextMessage": self.message}
        async with self.session.post(POST_URL, json=payload, headers=headers) as response:
            if response.status == 201:
                logging.info("Post created successfully.")
            else:
                logging.error(f"Failed to create post: {response.status}")

    async def run(self):
        connector = aiohttp.TCPConnector(limit=0)  # No limit on connections
        timeout = aiohttp.ClientTimeout(total=None)  # No timeout
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as self.session:
            while True:
                await self.post_message()
                await asyncio.sleep(0)  # Yield control to event loop

if __name__ == "__main__":
    automation = PLPAutomation()
    asyncio.run(automation.run())
