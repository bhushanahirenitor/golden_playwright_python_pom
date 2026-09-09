import json
import os
from playwright.sync_api import expect
from .common_page import CommonPage

def load_locator(filename):
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    locator_path = os.path.join(base_dir, "locators", "web", filename)
    with open(locator_path) as f:
        return json.load(f)

class OrdersReviewPage(CommonPage):
    def __init__(self, page, scenario):
        super().__init__(page, scenario)
        self.locators = load_locator("orders_review_page.json")

    def search_country_and_select(self, country_code, country_name):
        self.page.locator(self.locators["country"]).press_sequentially(country_code, delay=100)
        self.page.locator(self.locators["dropdown"]).wait_for()
        options_count = self.page.locator(self.locators["dropdown"]).locator("button").count()
        for i in range(options_count):
            text = self.page.locator(self.locators["dropdown"]).locator("button").nth(i).text_content()
            if text and text.strip() == country_name:
                self.page.locator(self.locators["dropdown"]).locator("button").nth(i).click()
                break

    def verify_email_id(self, username):
        expect(self.page.locator(self.locators["emailId"])).to_have_text(username)

    def submit_and_get_order_id(self):
        self.page.locator(self.locators["submit"]).click()
        expect(self.page.locator(self.locators["orderConfirmationText"])).to_have_text(" Thankyou for the order. ")
        order_id = self.page.locator(self.locators["orderId"]).text_content()
        self.set_value("orderId", order_id)
