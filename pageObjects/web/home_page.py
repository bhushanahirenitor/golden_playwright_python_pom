import json
import os
from playwright.sync_api import expect
from .common_page import CommonPage

def load_locator(filename):
    """Load locators from JSON file"""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    locator_path = os.path.join(base_dir, "locators", "web", filename)
    with open(locator_path) as f:
        return json.load(f)

class HomePage(CommonPage):
    flow_name = "home_page"
    
    def __init__(self, page, scenario):
        """Initialize HomePage with Playwright page object and scenario.
        
        Args:
            page: Playwright page object for browser interactions.
            scenario: Scenario object for test context and reporting.
        """
        super().__init__(page, scenario)
        self.locators = load_locator("home_page.json")
    
    def verify_user_on_home_page(self):
        """Verify that the user has been successfully redirected to the home page.
        
        This method performs comprehensive validation of the home page by:
        - Checking the current URL matches the expected home page URL pattern
        - Waiting for and verifying the home page logo is visible
        - Waiting for and verifying the main content area is present
        - Validating the page title matches expected home page title
        
        Returns:
            None
        
        Raises:
            AssertionError: If any of the home page verification checks fail.
        """
        # Get current URL from driver
        current_url = self.page.url
        
        # Assert current URL contains expected home page URL pattern
        assert "inventory.html" in current_url or "home" in current_url.lower(), f"Expected home page URL, but got: {current_url}"
        
        # Wait for 'home_page_logo' to be visible
        home_logo = self.page.locator(self.locators["home_page_logo"])
        home_logo.wait_for(state="visible", timeout=10000)
        
        # Wait for 'home_page_main_content' to be present
        main_content = self.page.locator(self.locators["home_page_main_content"])
        main_content.wait_for(state="attached", timeout=10000)
        
        # Assert 'home_page_logo' is displayed
        expect(home_logo).to_be_visible()
        
        # Verify page title matches expected home page title
        expect(self.page).to_have_title("Swag Labs")
        
        # Wait for page to be fully loaded
        self.page.wait_for_load_state("networkidle")