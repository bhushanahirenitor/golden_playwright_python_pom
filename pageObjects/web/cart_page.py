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
