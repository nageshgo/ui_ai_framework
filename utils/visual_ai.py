class VisualAI:

    def __init__(self, page):

        self.page = page

    def highlight_element(
        self,
        locator
    ):

        locator.evaluate(
            """
            el => {
                el.style.border =
                '3px solid red';
            }
            """
        )

    def capture_failure(
        self,
        name
    ):

        self.page.screenshot(
            path=f"failure_{name}.png"
        )