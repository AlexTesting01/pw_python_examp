import pytest_asyncio
import pytest
from playwright.async_api import expect
from global_config import GLOBAL_CONFIG




    

@pytest_asyncio.fixture(scope="function")
async def logged_in_page(page):

    await page.locator('[data-test="username"]').fill(GLOBAL_CONFIG["user"])
    await page.locator('[data-test="password"]').fill(GLOBAL_CONFIG["password"])
    await page.locator('[data-test="login-button"]').click()
    
    # Assert that login was successful before yielding the page
    await expect(page).to_have_url(GLOBAL_CONFIG["url"] + "inventory.html")
    
    yield page

