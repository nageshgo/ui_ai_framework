from agents.locator_agent import LocatorAgent


class LoginPage:

    def __init__(self, page):

        self.page = page

        self.ai = LocatorAgent(self.page)

    def open(self, url):

        self.page.goto(url)

    def login(
            self,
            username,
            password
    ):
        username_locator = self.ai.get_locator(
            "username input field in orangehrm login page"
        )

        password_locator = self.ai.get_locator(
            "password input field in orangehrm login page"
        )

        login_button_locator = self.ai.get_locator(
            "login button in orangehrm login page"
        )

        print(
            f"\nAI Username Locator: "
            f"{username_locator}"
        )

        print(
            f"AI Password Locator: "
            f"{password_locator}"
        )

        print(
            f"AI Login Button Locator: "
            f"{login_button_locator}"
        )

        username_element = eval(
            username_locator,
            {"page": self.page}
        )

        password_element = eval(
            password_locator,
            {"page": self.page}
        )

        login_button_element = eval(
            login_button_locator,
            {"page": self.page}
        )

        username_element.fill(username)

        password_element.fill(password)

        login_button_element.click()
