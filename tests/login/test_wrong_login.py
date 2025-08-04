import pytest
from playwright.async_api import expect
from global_config import GLOBAL_CONFIG



@pytest.mark.asyncio
async def test_login_wrong(page):
  await page.locator("[data-test='username']").click()
  await page.locator("[data-test='username']").fill(GLOBAL_CONFIG["locked_user"])
  await page.locator("[data-test='password']").click()
  await page.locator("[data-test='password']").fill(GLOBAL_CONFIG["password"])
  await page.locator("[data-test='login-button']").click()
  
  error_locator = page.locator('[data-test="error"]')
    
  # Assert that the error element is displayed on the page
  await expect(error_locator).to_be_visible()
  full_error_text = await error_locator.text_content()
  assert "Sorry, this user has been locked out." in full_error_text
  await expect(page).to_have_url("https://www.saucedemo.com/")
