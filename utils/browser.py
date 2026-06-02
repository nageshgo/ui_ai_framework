import os

from playwright.sync_api import sync_playwright


class BrowserManager:

    def __init__(self):

        self.playwright = sync_playwright().start()

        browser_name = os.getenv(
            "BROWSER",
            "chrome"
        ).lower()

        headless_mode = (
            os.getenv(
                "HEADLESS",
                "true"
            ).lower() == "true"
        )

        print(
            f"[BROWSER] Selected Browser = {browser_name}"
        )

        print(
            f"[BROWSER] Headless = {headless_mode}"
        )

        if browser_name == "firefox":

            self.browser = (
                self.playwright.firefox.launch(
                    headless=headless_mode
                )
            )

        else:

            self.browser = (
                self.playwright.chromium.launch(
                    headless=headless_mode,
                    args=["--lang=en-US"]
                )
            )

        self.page = self.browser.new_page()

    def start(self):
        return self.page

    def close(self):

        self.browser.close()

        self.playwright.stop()