import logging
import aiohttp
from bs4 import BeautifulSoup
import re

_LOGGER = logging.getLogger(__name__)

URL = "https://fastlane.co.il/"

async def get_price(session: aiohttp.ClientSession) -> str:
    """Fetch the price from Fastlane website."""
    try:
        async with session.get(URL) as response:
            text = await response.text()
            
        soup = BeautifulSoup(text, 'html.parser')
        
        # Based on curl output: <span id="lblPrice" class="price">8</span>
        price_span = soup.find("span", {"id": "lblPrice"})
        
        if price_span and price_span.text.strip():
            return price_span.text.strip()
            
        _LOGGER.warning("Could not find span with id 'lblPrice'")
        return "Unknown"

    except Exception as e:
        _LOGGER.error(f"Error fetching data from {URL}: {e}")
        return "Error"

if __name__ == "__main__":
    import asyncio
    async def test():
        async with aiohttp.ClientSession() as session:
            price = await get_price(session)
            print(f"Price found: '{price}'")
    
    asyncio.run(test())
