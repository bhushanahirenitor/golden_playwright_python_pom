import pytest
from playwright.sync_api import Page
from pageObjects.web.DashboardPage import DashboardPage
from pageObjects.web.CartPage import CartPage


class TestFeedback:
    """Test suite for feedback functionality"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup method to initialize page objects"""
        self.dashboardPage = DashboardPage(page)
        self.cartPage = CartPage(page)

    def test_search_and_verify_cart(self, page: Page):
        """Test to search for product, add to cart and verify"""
        # Step 1: Search for product and add to cart
        self.dashboardPage.search_product_and_add_to_cart()
        
        # Step 2: Navigate to cart
        self.dashboardPage.navigate_to_cart()
        
        # Step 3: Verify product is displayed in cart
        self.cartPage.verify_product_is_displayed()
