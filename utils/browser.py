import os

from playwright.sync_api import sync_playwright

class BrowserManager:

    def __init__(self):

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=os.getenv(
                "HEADLESS",
                "true"
            ).lower() == "true",
            args=["--lang=en-US"]
        )

        self.page = self.browser.new_page()

    def start(self):
        return self.page

    def close(self):
        self.browser.close()
        self.playwright.stop()
