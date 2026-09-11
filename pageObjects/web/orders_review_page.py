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

    def search_country_and_select(self, country_name):
        """Search for a country in the country selection field and select it.
        
        Args:
            country_name: The name of the country to search and select.
        """
        self.page.locator(self.locators["country"]).wait_for()
        self.page.locator(self.locators["country"]).press_sequentially(country_name, delay=100)
        self.page.locator(self.locators["dropdown"]).wait_for()
        options_count = self.page.locator(self.locators["dropdown"]).locator("button").count()
        for i in range(options_count):
            text = self.page.locator(self.locators["dropdown"]).locator("button").nth(i).text_content()
            if text and text.strip() == country_name.strip():
                self.page.locator(self.locators["dropdown"]).locator("button").nth(i).click()
                break

    def verify_email_id(self, username):
        expect(self.page.locator(self.locators["emailId"])).to_have_text(username)

    def submit_and_get_order_id(self):
        """Submit the order and retrieve the generated order ID.
        
        Returns:
            str: The order ID extracted from the confirmation page.
        """
        self.page.locator(self.locators["submit"]).wait_for()
        self.page.locator(self.locators["submit"]).click()
        expect(self.page.locator(self.locators["orderConfirmationText"])).to_be_visible()
        expect(self.page.locator(self.locators["orderConfirmationText"])).to_have_text(" Thankyou for the order. ")
        self.page.locator(self.locators["orderId"]).wait_for()
        order_id = self.page.locator(self.locators["orderId"]).text_content()
        self.set_value("orderId", order_id)
        return order_id

    def select_payment_method(self, payment_method):
        """Select a payment method from available options.
        
        Args:
            payment_method: The payment method to select (e.g., 'paymentMethodCreditCard', 'paymentMethodPayPal', 'paymentMethodCOD').
        """
        self.page.locator(self.locators["paymentMethodSection"]).wait_for()
        self.page.locator(self.locators[payment_method]).wait_for()
        self.page.locator(self.locators[payment_method]).click()
        expect(self.page.locator(self.locators[payment_method])).to_be_checked()

    def assert_order_confirmation_message_visible(self, order_id):
        """Assert that the order confirmation message containing the order ID is visible.
        
        Args:
            order_id: The order ID to verify in the confirmation message.
            
        Returns:
            bool: True if assertion passes.
            
        Raises:
            AssertionError: If the confirmation message or order ID is not visible or does not match.
        """
        self.page.locator(self.locators["orderConfirmationText"]).wait_for()
        confirmation_text = self.page.locator(self.locators["orderConfirmationText"]).text_content()
        if order_id not in confirmation_text:
            raise AssertionError(f"Order ID '{order_id}' not found in confirmation text: '{confirmation_text}'")
        expect(self.page.locator(self.locators["orderConfirmationText"])).to_be_visible()
        expect(self.page.locator(self.locators["orderId"])).to_have_text(order_id)
        return True
