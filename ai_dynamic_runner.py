from utils.browser import BrowserManager
from utils.gemini_helper import generate_test_steps
from utils.action_engine import ActionEngine

from pages.login_page import LoginPage

from config.settings import (
    BASE_URL,
    USERNAME,
    PASSWORD
)


scenario = input(
    "Enter testcase scenario: "
)

browser = BrowserManager()

page = browser.start()

login_page = LoginPage(page)

login_page.open(BASE_URL)

login_page.login(USERNAME, PASSWORD)

steps = generate_test_steps(scenario)

print("\nGenerated Steps From AI:\n")
print(steps)

engine = ActionEngine(page)

engine.execute(steps)

browser.close()