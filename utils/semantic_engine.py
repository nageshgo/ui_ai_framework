class SemanticEngine:

    def __init__(
        self,
        page
    ):

        self.page = page

    # ==========================================
    # FIND INPUT BY LABEL
    # ==========================================

    def find_input_by_label(
        self,
        label_text
    ):

        xpath = (
            f"//label[contains("
            f"normalize-space(), "
            f"'{label_text}')]"
            f"/ancestor::div[contains("
            f"@class,'oxd-input-group')]"
            f"//input"
        )

        try:

            locator = self.page.locator(
                xpath
            )

            if locator.count() > 0:

                escaped_xpath = (
                    xpath.replace(
                        '"',
                        '\\"'
                    )
                )

                locator_string = (
                    f'page.locator('
                    f'"{escaped_xpath}"'
                    f')'
                )

                print(
                    f"Semantic XPath Found: "
                    f"{locator_string}"
                )

                return locator_string

        except Exception as e:

            print(
                "Semantic Label "
                f"Search Failed: {str(e)}"
            )

        return None

    # ==========================================
    # SMART FIND
    # ==========================================

    def smart_find(
        self,
        element_name
    ):

        original = element_name

        element_name = (
            element_name
            .strip()
            .lower()
        )

        # ======================================
        # CLEANUP ORDER MATTERS
        # ======================================

        remove_words = [

            "text field",
            "input field",
            "textbox",
            "text box",
            "field",
            "input",
            "button",
            "link",
            "menu",
            "dropdown",
            "option"
        ]

        cleaned = element_name

        for word in remove_words:

            cleaned = cleaned.replace(
                word,
                ""
            )

        cleaned = cleaned.strip()

        cleaned_title = cleaned.title()

        # ======================================
        # INPUT FIELDS
        # ======================================

        if any(
            word in original.lower()
            for word in [
                "field",
                "input",
                "textbox",
                "text field"
            ]
        ):

            locator = (
                self.find_input_by_label(
                    cleaned_title
                )
            )

            if locator:

                return locator

            # ==================================
            # FALLBACK INPUT SEARCH
            # ==================================

            return (
                f'page.locator('
                f'"input[placeholder*=\''
                f'{cleaned_title}'
                f'\']"'
                f')'
            )

        # ======================================
        # BUTTONS
        # ======================================

        if "button" in original.lower():

            return (
                f'page.get_by_role('
                f'"button", '
                f'name="{cleaned_title}"'
                f')'
            )

        # ======================================
        # MENUS / LINKS
        # ======================================

        if any(
            word in original.lower()
            for word in [
                "menu",
                "link"
            ]
        ):

            return (
                f'page.get_by_role('
                f'"link", '
                f'name="{cleaned_title}"'
                f')'
            )

        # ======================================
        # TEXT SEARCH
        # ======================================

        return (
            f'page.get_by_text('
            f'"{cleaned_title}"'
            f')'
        )