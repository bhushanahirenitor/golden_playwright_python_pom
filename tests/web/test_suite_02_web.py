import pytest
from playwright.sync_api import Page
from pageObjects.web.LoginPage import LoginPage
from pageObjects.web.SearchPage import SearchPage


class TestSuite02Web:
    """Test suite for web application search functionality"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup fixture to initialize page objects"""
        self.loginPage = LoginPage(page)
        self.searchPage = SearchPage(page)
        yield

    def test_search_product(self, page: Page):
        """Test case to search for a product"""
        # Navigate to the application
        self.loginPage.go_to()
        
        # Click Search box
        self.searchPage.click_search_box()
        
        # Input product name
        self.searchPage.input_product_name()
        
        # Click Search button
        self.searchPage.click_search_button()
        
        # Verify product is displayed
        self.searchPage.verify_product_displayed()