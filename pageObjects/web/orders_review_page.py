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
        self.locators = load_locator("orders_review_page_locators.json")

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

    def select_payment_method(self, payment_method):
        """Select a payment method from available options.
        
        Args:
            payment_method (str): The payment method to select (e.g., 'Credit Card', 'PayPal', 'COD').
        """
        self.page.locator(self.locators["paymentMethodSection"]).wait_for()
        payment_method_map = {
            "Credit Card": "paymentMethodCreditCard",
            "PayPal": "paymentMethodPayPal",
            "COD": "paymentMethodCOD",
            "Cash on Delivery": "paymentMethodCOD"
        }
        payment_method_key = payment_method_map.get(payment_method, "paymentMethodRadioButton")
        self.page.locator(self.locators[payment_method_key]).wait_for()
        self.page.locator(self.locators[payment_method_key]).click()
        expect(self.page.locator(self.locators[payment_method_key])).to_be_checked()

    def assert_order_confirmation_message_visible(self, order_id):
        """Assert that the order confirmation message containing the order ID is visible.
        
        Args:
            order_id (str): The order ID to verify in the confirmation message.
        
        Returns:
            bool: True if assertion passes.
        
        Raises:
            AssertionError: If the confirmation message or order ID is not visible or does not match.
        """
        self.page.locator(self.locators["orderConfirmationText"]).wait_for()
        confirmation_text = self.page.locator(self.locators["orderConfirmationText"]).text_content()
        if order_id not in confirmation_text:
            raise AssertionError(f"Order ID '{order_id}' not found in confirmation message: '{confirmation_text}'")
        expect(self.page.locator(self.locators["orderConfirmationText"])).to_be_visible()
        expect(self.page.locator(self.locators["orderId"])).to_have_text(order_id)
        return True
