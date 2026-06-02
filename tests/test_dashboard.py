import re

from playwright.sync_api import expect
from utils.browser import BrowserManager
from pages.login_page import LoginPage
from config.settings import BASE_URL, USERNAME, PASSWORD


def test_dashboard_loaded():

    browser = BrowserManager()

    page = browser.start()

    login_page = LoginPage(page)

    login_page.open(BASE_URL)

    login_page.login(USERNAME, PASSWORD)

    # wait after login
    page.wait_for_load_state("networkidle")

    # validate dashboard page
    expect(
        page.get_by_role("link", name="Dashboard")
    ).to_be_visible(timeout=10000)

    browser.close()
# # from playwright.sync_api import expect
# # from utils.browser import BrowserManager
# # from pages.login_page import LoginPage
# # from config.settings import BASE_URL, USERNAME, PASSWORD
#
#
def test_left_menu_items():

    browser = BrowserManager()

    page = browser.start()

    login_page = LoginPage(page)

    login_page.open(BASE_URL)

    login_page.login(USERNAME, PASSWORD)

    menu_items = [
        "Admin",
        "PIM",
        "Leave",
        "Time",
        "Recruitment"
    ]

    for item in menu_items:

        expect(
            page.locator("ul.oxd-main-menu")
        ).to_contain_text(item)

    browser.close()
#
# # from playwright.sync_api import expect
# # from utils.browser import BrowserManager
# # from pages.login_page import LoginPage
# # from config.settings import BASE_URL, USERNAME, PASSWORD
#
#
def test_search_employee():

    browser = BrowserManager()

    page = browser.start()

    login_page = LoginPage(page)

    login_page.open(BASE_URL)

    login_page.login(USERNAME, PASSWORD)

    page.locator("span:has-text('PIM')").click()

    page.locator(
        "input[placeholder='Type for hints...']"
    ).first.fill("Linda")

    page.locator(
        "button[type='submit']"
    ).click()

    expect(
        page.locator(".oxd-table")
    ).to_be_visible()

    browser.close()

# # from playwright.sync_api import expect
# # from utils.browser import BrowserManager
# # from pages.login_page import LoginPage
# # from config.settings import BASE_URL, USERNAME, PASSWORD
#

def test_logout():

    browser = BrowserManager()

    page = browser.start()

    login_page = LoginPage(page)

    login_page.open(BASE_URL)

    login_page.login(USERNAME, PASSWORD)

    page.locator(".oxd-userdropdown-tab").click()

    page.locator("text=Logout").click()

    expect(page).to_have_url(
        re.compile(".*login.*")
    )

    browser.close()

# # from playwright.sync_api import expect
# # from utils.browser import BrowserManager
# # from pages.login_page import LoginPage
# # from config.settings import BASE_URL, USERNAME, PASSWORD
#
#
def test_add_employee():

    browser = BrowserManager()

    page = browser.start()

    login_page = LoginPage(page)

    login_page.open(BASE_URL)

    login_page.login(USERNAME, PASSWORD)

    page.locator("span:has-text('PIM')").click()

    page.locator("a:has-text('Add Employee')").click()

    page.locator("input[name='firstName']").fill("AI")

    page.locator("input[name='lastName']").fill("Tester")

    page.get_by_role("button", name="Save").click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)
    expect(page).to_have_url(re.compile("viewPersonalDetails"))

    expect(
        page.get_by_text("AI Tester")
    ).to_be_visible(timeout=10000)

    browser.close()