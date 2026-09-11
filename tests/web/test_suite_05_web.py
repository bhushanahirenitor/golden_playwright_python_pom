import pytest
from playwright.sync_api import Page
from pageObjects.web.LoginPage import LoginPage
from pageObjects.web.DashboardPage import DashboardPage
from pageObjects.web.CartPage import CartPage
from pageObjects.web.OrdersReviewPage import OrdersReviewPage


class TestSuite05Web:
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.loginPage = LoginPage(page)
        self.dashboardPage = DashboardPage(page)
        self.cartPage = CartPage(page)
        self.ordersReviewPage = OrdersReviewPage(page)
    
    def test_complete_order_flow(self, page: Page):
        """Test complete order flow from login to order confirmation"""
        
        # Navigate to the application
        self.loginPage.go_to()
        
        # Login with valid credentials
        self.loginPage.valid_login()
        
        # Search for product and add to cart
        self.dashboardPage.search_product_add_cart()
        
        # Navigate to cart
        self.dashboardPage.navigate_to_cart()
        
        # Verify product is displayed in cart
        self.cartPage.verify_product_is_displayed()
        
        # Click checkout button
        self.cartPage.click_checkout()
        
        # Search and select country
        self.ordersReviewPage.search_country_and_select()
        
        # Select payment method
        self.ordersReviewPage.select_payment_method()
        
        # Submit order and get order ID
        order_id = self.ordersReviewPage.submit_and_get_order_id()
        
        # Assert order confirmation message with order ID is visible
        self.ordersReviewPage.assert_order_confirmation_message_visible()