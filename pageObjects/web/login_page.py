import json
import os
from .common_page import CommonPage

def load_locator(filename):
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    locator_path = os.path.join(base_dir, "locators", "web", filename)
    with open(locator_path) as f:
        return json.load(f)

def load_test_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    with open(os.path.join(base_dir, "testData", "web", "test_data.json")) as f:
        return json.load(f)

class LoginPage(CommonPage):
    def __init__(self, page, scenario):
        super().__init__(page, scenario)
        self.locators = load_locator("login_page_locators.json")
        self.test_data = load_test_data()

    def go_to(self):
        """Navigate to the login page and verify key elements are visible.
        
        This method navigates to the login page URL from test data, waits for the page
        to load completely, performs accessibility analysis, and verifies that the username
        field, password field, and sign-in button are visible.
        """
        self.page.goto(self.test_data["qa"])
        self.page.wait_for_load_state("domcontentloaded")
        self.scenario.a11y_analysis()
        self.page.locator(self.locators["userName"]).wait_for(state="visible")
        self.page.locator(self.locators["password"]).wait_for(state="visible")
        self.page.locator(self.locators["signInbutton"]).wait_for(state="visible")

    def valid_login(self, username, password):
        """Perform a valid login with the provided username and password.
        
        Args:
            username (str): The username to enter in the username field.
            password (str): The password to enter in the password field.
        
        This method waits for the username and password fields to be visible, fills them
        with the provided credentials, clicks the sign-in button, and waits for the page
        to reach a network idle state.
        """
        self.page.locator(self.locators["userName"]).wait_for(state="visible")
        self.page.locator(self.locators["userName"]).fill(username)
        self.page.locator(self.locators["password"]).wait_for(state="visible")
        self.page.locator(self.locators["password"]).fill(password)
        self.page.locator(self.locators["signInbutton"]).wait_for(state="visible")
        self.page.locator(self.locators["signInbutton"]).click()
        self.page.wait_for_load_state("networkidle")
