import pytest
from playwright.async_api import expect
from global_config import GLOBAL_CONFIG


@pytest.mark.development  
@pytest.mark.production  
@pytest.mark.asyncio
async def test_login_correct(page):
  await expect(page.locator("[data-test='username']")).to_be_visible()
  await page.locator("[data-test='username']").fill(GLOBAL_CONFIG["user"])
  await page.locator("[data-test='password']").fill(GLOBAL_CONFIG["password"])
  await page.locator("[data-test='login-button']").click()
  
  await expect(page).to_have_url(GLOBAL_CONFIG["url"] + "inventory.html")
