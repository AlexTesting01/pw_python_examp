import sys
import os
# pytest -v -n auto


# Add the root project directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import asyncio
import sys
import pytest_asyncio
from playwright.async_api import async_playwright
from playwright_config import PW_CONFIG
from global_config import GLOBAL_CONFIG

# Fix loop policy issue on macOS + Python 3.8
if sys.platform == "darwin":
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
    
    


@pytest_asyncio.fixture(scope="function")
async def playwright_instance():
    async with async_playwright() as p:
        yield p


@pytest_asyncio.fixture(scope="function")
async def browser_context(playwright_instance):
    browser_type = getattr(playwright_instance, PW_CONFIG["browser"])
    browser = await browser_type.launch(headless=PW_CONFIG["headless"])
    context = await browser.new_context()
    yield context
    await context.close()
    await browser.close()


@pytest_asyncio.fixture(scope="function")
async def page(browser_context):
    page = await browser_context.new_page()
    await page.goto(GLOBAL_CONFIG["url"])
    yield page
    await page.close()
    
