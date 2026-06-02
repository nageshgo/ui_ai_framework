class HealingEngine:

    def generate_fallbacks(
        self,
        element_name
    ):

        # =====================================
        # NORMALIZE INPUT
        # =====================================

        original = (
            element_name
            .strip()
            .lower()
        )

        # =====================================
        # REMOVE COMMON WORDS
        # =====================================

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

        clean = original

        for word in remove_words:

            clean = clean.replace(
                word,
                ""
            )

        clean = clean.strip()

        clean_title = clean.title()

        # =====================================
        # SAFE XPATH
        # =====================================

        xpath_locator = (
            'page.locator('
            f'"//label[contains(normalize-space(), '
            f"\'{clean_title}\')]"
            '/ancestor::div[contains('
            "@class,'oxd-input-group')]"
            '//input"'
            ')'
        )

        # =====================================
        # LOCATOR LIST
        # =====================================

        locators = [

            # ROLE LOCATORS

            (
                'page.get_by_role('
                f'"button", '
                f'name="{clean_title}"'
                ')'
            ),

            (
                'page.get_by_role('
                f'"link", '
                f'name="{clean_title}"'
                ')'
            ),

            (
                'page.get_by_role('
                f'"textbox", '
                f'name="{clean_title}"'
                ')'
            ),

            # TEXT LOCATORS

            (
                f'page.get_by_text('
                f'"{clean_title}"'
                ')'
            ),

            (
                f'page.get_by_placeholder('
                f'"{clean_title}"'
                ')'
            ),

            (
                f'page.get_by_label('
                f'"{clean_title}"'
                ')'
            ),

            # CSS TEXT

            (
                f'page.locator('
                f'"text={clean_title}"'
                ')'
            ),

            # XPATH

            xpath_locator,

            # GENERIC INPUT

            'page.locator("input")'
        ]

        # =====================================
        # REMOVE DUPLICATES
        # =====================================

        locators = list(
            dict.fromkeys(locators)
        )

        # =====================================
        # DEBUG LOG
        # =====================================

        print(
            "\nGenerated Healing Candidates:"
        )

        for locator in locators:

            print(locator)

        return locators