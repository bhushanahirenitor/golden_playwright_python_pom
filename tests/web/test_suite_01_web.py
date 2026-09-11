import pytest
from playwright.sync_api import Page
from pageObjects.web.LoginPage import LoginPage
from pageObjects.web.HomePage import HomePage


class TestSuite01Web:
    """Test suite for web automation tests"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup fixture that runs before each test"""
        self.loginPage = LoginPage(page)
        self.homePage = HomePage(page)
        yield

    def test_valid_login(self, page: Page):
        """Test case for valid login functionality"""
        # Navigate to the login page
        self.loginPage.go_to()
        
        # Perform valid login with username and password
        self.loginPage.valid_login()
        
        # Assert user is redirected to the home page
        self.homePage.verify_user_on_home_page()