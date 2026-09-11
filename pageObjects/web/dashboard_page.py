import json
import os
from playwright.sync_api import expect
from .common_page import CommonPage

def load_locator(filename):
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    locator_path = os.path.join(base_dir, "locators", "web", filename)
    with open(locator_path) as f:
        return json.load(f)

class DashboardPage(CommonPage):
    def __init__(self, page, scenario):
        super().__init__(page, scenario)
        self.locators = load_locator("dashboard_locators.json")

    def search_product_add_cart(self, product_name):
        product = self.page.locator(self.locators["products"], has_text=product_name).first
        product.wait_for(state="visible")
        add_cart_button = product.locator("button", has_text=" Add To Cart")
        expect(add_cart_button).to_be_visible()
        if add_cart_button.is_visible():
            add_cart_button.click()

    def navigate_to_orders(self):
        self.page.locator(self.locators["orders"]).click()
        self.page.wait_for_load_state("networkidle")

    def navigate_to_cart(self):
        self.page.locator(self.locators["cart"]).click()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_load_state("domcontentloaded")

    def search_product_and_add_to_cart(self, product_name):
        """Search for a product by name and add it to the cart.
        
        This method performs a complete search workflow: waits for the search input to be visible,
        clears any existing text, enters the product name, triggers the search, waits for results,
        locates the specific product, clicks its 'Add to Cart' button, and waits for confirmation.
        
        Args:
            product_name (str): The name of the product to search for and add to cart.
        
        Returns:
            None
        """
        self.page.locator(self.locators["search_input"]).wait_for(state="visible")
        self.page.locator(self.locators["search_input"]).clear()
        self.page.locator(self.locators["search_input"]).fill(product_name)
        self.page.locator(self.locators["search_button"]).click()
        self.page.locator(self.locators["search_results"]).wait_for(state="visible")
        product = self.page.locator(self.locators["products"], has_text=product_name).first
        product.wait_for(state="visible")
        add_cart_button = product.locator("button", has_text=" Add To Cart")
        expect(add_cart_button).to_be_visible()
        add_cart_button.click()
        self.page.locator(self.locators["cart_confirmation_message"]).wait_for(state="visible", timeout=5000)
