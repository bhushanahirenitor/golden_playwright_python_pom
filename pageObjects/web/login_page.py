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
        self.locators = load_locator("login_page.json")
        self.test_data = load_test_data()

    def go_to(self):
        self.page.goto(self.test_data["qa"])
        self.page.wait_for_load_state("domcontentloaded")
        self.scenario.a11y_analysis()

    def valid_login(self, username, password):
        self.page.locator(self.locators["userName"]).fill(username)
        self.page.locator(self.locators["password"]).fill(password)
        self.page.locator(self.locators["signInbutton"]).click()
        self.page.wait_for_load_state("networkidle")
