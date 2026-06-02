from pages.login_page import LoginPage
from utils.browser import BrowserManager
from config.settings import (
    BASE_URL,
    USERNAME,
    PASSWORD
)


def test_ai_locator_login():

    browser = BrowserManager()

    page = browser.start()

    login_page = LoginPage(page)

    login_page.open(BASE_URL)

    login_page.login(
        USERNAME,
        PASSWORD
    )

    assert "dashboard" in page.url.lower()

    browser.close()