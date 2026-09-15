import json
import os
from playwright.sync_api import expect
from .common_page import CommonPage

def load_locator(filename):
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    locator_path = os.path.join(base_dir, "locators", "web", filename)
    with open(locator_path) as f:
        return json.load(f)

class SearchPage(CommonPage):
    flow_name = "search_page"
    
    def __init__(self, page, scenario):
        """Initialize the SearchPage with page and scenario objects.
        
        Args:
            page: Playwright page object for browser interactions.
            scenario: Scenario object for test context and reporting.
        """
        super().__init__(page, scenario)
        self.locators = load_locator("search_page.json")
    
    def click_search_box(self):
        """Click the search box element to activate the input field.
        
        Waits for the search box to be clickable before clicking it.
        """
        search_box = self.page.locator(self.locators["search_box"])
        search_box.wait_for(state="visible")
        search_box.click()
    
    def input_product_name(self, product_name):
        """Input a product name into the search box input field.
        
        Args:
            product_name (str): The name of the product to search for.
        
        Waits for the search input field to be visible, clears any existing text,
        and fills it with the provided product name.
        """
        search_input = self.page.locator(self.locators["search_box_input"])
        search_input.wait_for(state="visible")
        search_input.clear()
        search_input.fill(product_name)
    
    def click_search_button(self):
        """Click the search button to execute the search.
        
        Waits for the search button to be clickable before clicking it.
        """
        search_button = self.page.locator(self.locators["search_button"])
        search_button.wait_for(state="visible")
        search_button.click()
    
    def verify_product_displayed(self, product_name):
        """Verify that a specific product is displayed in the search results.
        
        Args:
            product_name (str): The name of the product to verify.
        
        Returns:
            bool: True if the product is found in search results, False otherwise.
        
        Waits for search results to load and iterates through result items
        to find a match with the provided product name.
        """
        results_list = self.page.locator(self.locators["search_results_list"])
        results_list.wait_for(state="visible")
        
        result_items = self.page.locator(self.locators["search_result_item"])
        result_items.first.wait_for(state="visible")
        
        count = result_items.count()
        for i in range(count):
            item_text = result_items.nth(i).text_content()
            if product_name in item_text:
                return True
        
        return False