import json
import os
from playwright.sync_api import expect
from .common_page import CommonPage

def load_locator(filename):
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    locator_path = os.path.join(base_dir, "locators", "web", filename)
    with open(locator_path) as f:
        return json.load(f)

class OrdersHistoryPage(CommonPage):
    def __init__(self, page, scenario):
        super().__init__(page, scenario)
        self.locators = load_locator("orders_history_page.json")

    def search_order_and_select(self):
        order_found = False
        self.page.wait_for_selector("tbody")
        rows = self.page.locator(self.locators["rows"]).all()
        for row in rows:
            match_order_id = row.locator("th").text_content()
            if match_order_id and match_order_id in self.get_value("orderId"):
                row.locator(self.locators["BTN_View"]).click()
                order_found = True
                break
        
        assert order_found, "Order ID not found in history"
        self.take_screenshot("Orders page")

    def get_order_id(self):
        return self.page.locator(self.locators["orderdIdDetail"]).text_content()
