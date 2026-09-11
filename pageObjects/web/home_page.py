import json
import os
from playwright.sync_api import expect
from .common_page import CommonPage

def load_locator(filename):
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    locator_path = os.path.join(base_dir, "locators", "web", filename)
    with open(locator_path) as f:
        return json.load(f)

class HomePage(CommonPage):
    flow_name = "home_page"
    
    def __init__(self, page, scenario):
        super().__init__(page, scenario)
        self.locators = load_locator("home_page.json")
    
    def verify_user_on_home_page(self):
        """Verify that the user has been successfully redirected to the home page.
        
        This method checks that the current URL matches the home page URL pattern
        and verifies that key home page elements (header and navigation menu) are visible.
        
        Args:
            None
            
        Returns:
            None
        """
        current_url = self.page.url
        assert "home" in current_url or current_url.endswith("/"), f"Expected home page URL, but got: {current_url}"
        
        home_page_header = self.page.locator(self.locators["home_page_header"])
        home_page_header.wait_for(state="visible")
        expect(home_page_header).to_be_visible()
        
        navigation_menu = self.page.locator(self.locators["navigation_menu"])
        navigation_menu.wait_for(state="visible")
        expect(navigation_menu).to_be_visible()