class LocatorRanker:

    def __init__(self, page):

        self.page = page

    def rank(
            self,
            locators
    ):

        scored = []

        generic_patterns = [

            'page.locator("input")',
            'page.locator("button")',
            'page.locator("div")',
            'page.locator("span")',
            'page.locator("*")'
        ]

        for locator in locators:

            try:

                print(
                    f"\nEvaluating Locator: "
                    f"{locator}"
                )

                # =====================================
                # CREATE PLAYWRIGHT OBJECT
                # =====================================

                obj = eval(
                    locator,
                    {"page": self.page}
                )

                # =====================================
                # ELEMENT COUNT
                # =====================================

                count = obj.count()

                # =====================================
                # IGNORE INVALID LOCATORS
                # =====================================

                if count == 0:

                    print(
                        "Skipping locator "
                        "(0 elements found)"
                    )

                    continue

                # =====================================
                # VISIBILITY CHECK
                # =====================================

                visible = False

                try:

                    obj.first.wait_for(
                        state="visible",
                        timeout=3000
                    )

                    visible = True

                except Exception:

                    visible = False

                # =====================================
                # BASE SCORE
                # =====================================

                score = 0

                # =====================================
                # UNIQUE MATCH BONUS
                # =====================================

                if count == 1:

                    score += 50

                elif count <= 3:

                    score += 20

                # =====================================
                # VISIBILITY BONUS
                # =====================================

                if visible:

                    score += 50

                # =====================================
                # SMART LOCATOR BONUS
                # =====================================

                if "get_by_role" in locator:

                    score += 40

                elif "get_by_label" in locator:

                    score += 35

                elif "get_by_placeholder" in locator:

                    score += 30

                elif "get_by_text" in locator:

                    score += 25

                elif "locator(" in locator:

                    score += 5

                # =====================================
                # GENERIC LOCATOR PENALTY
                # =====================================

                if locator.strip() in generic_patterns:

                    score -= 60

                # =====================================
                # EXTRA PENALTY IF TOO MANY MATCHES
                # =====================================

                if count > 5:

                    score -= 20

                # =====================================
                # LOCATOR TYPE
                # =====================================

                locator_type = "SMART"

                if locator.strip() in generic_patterns:

                    locator_type = "GENERIC"


                # =====================================
                # REJECT INPUT LOCATOR FOR VERIFY STEPS
                # =====================================
                if locator == 'page.locator("input")':
                    score -= 100

                # =====================================
                # LOG SCORE
                # =====================================
                print(
                    f"[{locator_type}] "
                    f"Count={count}, "
                    f"Visible={visible}, "
                    f"Score={score}"
                )

                scored.append(
                    (
                        score,
                        locator
                    )
                )

            except Exception as e:

                print(
                    f"Ranking Failed: "
                    f"{str(e)}"
                )

        # =====================================
        # SORT LOCATORS
        # =====================================

        scored.sort(
            reverse=True,
            key=lambda x: x[0]
        )

        print(
            "\n=========== "
            "LOCATOR RANKING "
            "==========="
        )

        for score, locator in scored:

            print(
                f"Score={score} | "
                f"Locator={locator}"
            )

        # =====================================
        # RETURN BEST LOCATOR
        # =====================================

        if scored:

            best_locator = scored[0][1]

            print(
                f"\nBest Ranked Locator: "
                f"{best_locator}"
            )

            return best_locator

        print(
            "\nNo valid locator found"
        )

        return None