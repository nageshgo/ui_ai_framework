from utils.browser import BrowserManager
from pages.login_page import LoginPage
from config.settings import BASE_URL, USERNAME, PASSWORD
from playwright.sync_api import expect

browser = BrowserManager()

page = browser.start()

login_page = LoginPage(page)

login_page.open(BASE_URL)

login_page.login(USERNAME, PASSWORD)

# Validate successful login first (optional, but good practice)
expect(page.locator("text=Welcome")).to_be_visible() # Assuming "Welcome" text is visible after login

# Locate and click the logout button
logout_button = page.get_by_role("button", name="Logout")
logout_button.click()

# Assertions for successful logout
# 1. Assert that the URL has returned to the base URL or a specific login path
expect(page).to_have_url(BASE_URL)

# 2. Assert that key elements of the login page are now visible
expect(login_page.username_input).to_be_visible()
expect(login_page.password_input).to_be_visible()
expect(login_page.login_button).to_be_visible()

# 3. Assert that elements visible only after login are no longer present
expect(page.locator("text=Welcome")).not_to_be_visible() # Example: Check for absence of a post-login element
expect(logout_button).not_to_be_visible()

browser.close()