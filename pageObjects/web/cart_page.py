import json
import os
from playwright.sync_api import expect
from .common_page import CommonPage

def load_locator(filename):
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    locator_path = os.path.join(base_dir, "locators", "web", filename)
    with open(locator_path) as f:
        return json.load(f)

class CartPage(CommonPage):
    def __init__(self, page, scenario):
        super().__init__(page, scenario)
        self.locators = load_locator("cart_page_locators.json")

    def verify_product_is_displayed(self, product_name):
        """Verify that a product is displayed in the cart.
        
        Waits for the cart items container to be visible, then locates and verifies
        the product heading element by name. Ensures the product is visible in the cart.
        
        Args:
            product_name (str): The name of the product to verify in the cart.
            
        Returns:
            bool: True if the product is found and visible.
            
        Raises:
            AssertionError: If the product is not found or not visible.
        """
        cart_items_container = self.page.locator(self.locators["cart_items_container"])
        cart_items_container.wait_for(state="visible")
        selected_product = self.page.get_by_role("heading", name=product_name)
        selected_product.wait_for(state="visible")
        expect(selected_product).to_be_visible()
        return True

    def click_checkout(self):
        self.page.get_by_role("button", name="Checkout⟩").click()
        self.take_screenshot("checkout")

    def locate_quantity_control(self, product_name):
        """Locate the quantity control element for a specific product in the cart.
        
        Finds the product by name and navigates to its parent container to locate
        the associated quantity control input element.
        
        Args:
            product_name (str): The name of the product whose quantity control to locate.
            
        Returns:
            Locator: The Playwright locator for the quantity control input element.
        """
        cart_items_container = self.page.locator(self.locators["cart_items_container"])
        cart_items_container.wait_for(state="visible")
        selected_product = self.page.get_by_role("heading", name=product_name)
        selected_product.wait_for(state="visible")
        product_container = selected_product.locator("xpath=ancestor::div[contains(@class, 'cart_item') or contains(@class, 'product')]")
        quantity_control = product_container.locator(self.locators["quantity_control_input"])
        quantity_control.wait_for(state="visible")
        return quantity_control

    def update_product_quantity(self, product_name, new_quantity):
        """Update the quantity of a specific product in the cart.
        
        Locates the product's quantity control, clears the current value, and enters
        the new quantity. Waits for the cart to update by monitoring the loading spinner
        and total price display.
        
        Args:
            product_name (str): The name of the product whose quantity to update.
            new_quantity (int): The new quantity value to set.
        """
        cart_items_container = self.page.locator(self.locators["cart_items_container"])
        cart_items_container.wait_for(state="visible")
        selected_product = self.page.get_by_role("heading", name=product_name)
        selected_product.wait_for(state="visible")
        product_container = selected_product.locator("xpath=ancestor::div[contains(@class, 'cart_item') or contains(@class, 'product')]")
        quantity_control = product_container.locator(self.locators["quantity_control_input"])
        quantity_control.wait_for(state="visible")
        quantity_control.clear()
        quantity_control.fill(str(new_quantity))
        if "loading_spinner" in self.locators:
            loading_spinner = self.page.locator(self.locators["loading_spinner"])
            loading_spinner.wait_for(state="hidden", timeout=10000)
        total_price_display = self.page.locator(self.locators["total_price_display"])
        total_price_display.wait_for(state="visible")
        self.take_screenshot("quantity_updated")

    def verify_total_price(self, expected_total):
        """Verify that the total price in the cart matches the expected value.
        
        Locates the total price display element, extracts the numeric value by removing
        currency symbols and formatting, and asserts that it matches the expected total.
        
        Args:
            expected_total (float or str): The expected total price value.
            
        Raises:
            AssertionError: If the actual total price does not match the expected value.
        """
        total_price_display = self.page.locator(self.locators["total_price_display"])
        total_price_display.wait_for(state="visible")
        price_text = total_price_display.inner_text()
        cleaned_price = price_text.replace("$", "").replace(",", "").strip()
        actual_total = float(cleaned_price)
        expected_total_float = float(expected_total)
        assert actual_total == expected_total_float, f"Total price mismatch: expected ${expected_total_float}, but got ${actual_total}"
        self.take_screenshot("total_price_verified")
