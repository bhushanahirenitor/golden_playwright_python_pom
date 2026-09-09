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
        self.locators = load_locator("cart_page.json")

    def verify_product_is_displayed(self, product_name):
        selected_product = self.page.get_by_role("heading", name=product_name)
        selected_product.wait_for(state="visible")
        expect(selected_product).to_be_visible()

    def click_checkout(self):
        self.page.get_by_role("button", name="Checkout❯").click()
        self.take_screenshot("checkout")
