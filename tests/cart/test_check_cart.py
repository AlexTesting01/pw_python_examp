import re
import pytest
from playwright.async_api import expect
from global_config import GLOBAL_CONFIG


@pytest.mark.asyncio
async def test_add_item_to_cart_and_verify(logged_in_page):
    """
    Verifies that adding an item from the products page correctly
    updates the cart and is visible on the cart page (async).
    """
    page = logged_in_page
    
    await expect(page.locator('[data-test="shopping-cart-badge"]')).not_to_be_visible()
    # 1. Add an item to the cart from the inventory page
    item_name = "Sauce Labs Backpack"
    item_locator = page.locator(f'[data-test="add-to-cart-sauce-labs-backpack"]')
    await item_locator.click()
    
    # 2. Assert that the cart icon count is updated
    cart_count_locator = page.locator('[data-test="shopping-cart-badge"]')
    await expect(cart_count_locator).to_have_text("1")
    
    # 3. Navigate to the cart page
    await page.locator('[data-test="shopping-cart-link"]').click()
    await expect(page).to_have_url(GLOBAL_CONFIG["url"]+"cart.html")

    # 4. Assert that the added item is visible in the cart list
    cart_item = page.locator('.cart_item', has_text=item_name)
    await expect(cart_item).to_be_visible()
    
    # 5. (Bonus) Verify the item's price and quantity
    await expect(cart_item.locator('.inventory_item_price')).to_have_text("$29.99")
    await expect(cart_item.locator('.cart_quantity')).to_have_text("1")


@pytest.mark.asyncio
async def test_remove_item_from_cart(logged_in_page):
    """
    Verifies that removing an item from the cart page correctly
    removes it from the list and updates the cart count (async).
    """
    page = logged_in_page

    # 1. Add two items to the cart
    await page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()
    await page.locator('[data-test="add-to-cart-sauce-labs-bike-light"]').click()
    await expect(page.locator('[data-test="shopping-cart-badge"]')).to_have_text("2")

    # 2. Navigate to the cart page
    await page.locator('[data-test="shopping-cart-link"]').click()
    
    # 3. Remove one of the items
    remove_button_locator = page.locator('[data-test="remove-sauce-labs-bike-light"]')
    await remove_button_locator.click()

    # 4. Assert that the item is no longer in the cart list
    item_name = "Sauce Labs Bike Light"
    removed_item_locator = page.locator('.cart_item_label', has_text=item_name)
    await expect(removed_item_locator).not_to_be_visible()

    # 5. Assert that the cart icon count is updated to "1"
    cart_count_locator = page.locator('[data-test="shopping-cart-badge"]')
    await expect(cart_count_locator).to_have_text("1")


@pytest.mark.asyncio
async def test_continue_shopping_redirects_to_products(logged_in_page):
    """
    Verifies that the "Continue Shopping" button on the cart page
    correctly redirects the user back to the inventory page (async).
    """
    page = logged_in_page

    # 1. Add an item and navigate to the cart page
    await page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()
    await page.locator('[data-test="shopping-cart-link"]').click()
    await expect(page).to_have_url(GLOBAL_CONFIG["url"] + "cart.html")

    # 2. Click the "Continue Shopping" button
    await page.locator('[data-test="continue-shopping"]').click()

    # 3. Assert that the user is on the inventory page
    await expect(page).to_have_url(GLOBAL_CONFIG["url"] + "inventory.html")
    # You can also assert the presence of the product header
    await expect(page.locator('.header_secondary_container')).to_have_text(re.compile('Products'))