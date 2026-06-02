import json
import os

from utils.ai_metrics import ai_metrics
from utils.semantic_engine import SemanticEngine
from utils.locator_ranker import LocatorRanker
from utils.healing_engine import HealingEngine
from utils.logger import FrameworkLogger
from utils.visual_ai import VisualAI


class LocatorAgent:

    def __init__(self, page):

        self.page = page

        self.cache_file = "locator_cache.json"

        self.locator_cache = self.load_cache()
        self.semantic = SemanticEngine(page)

        self.ranker = LocatorRanker(page)

        self.healing = HealingEngine()
        self.visual = VisualAI(page)


        self.healing_history = []

        # Locator Logger
        self.locator_logger = (
            FrameworkLogger.get_logger(
                "locator",
                "locator.log"
            )
        )
        # Healing Logger
        self.healing_logger = (
            FrameworkLogger.get_logger(
                "healing",
                "healing.log"
            )
        )
        # ==========================================
        # ENTERPRISE STATIC LOCATORS
        # ==========================================

        self.static_locators = {

            # ======================================
            # LOGIN PAGE
            # ======================================

            "username input field in orangehrm login page":
                'page.locator("input[name=\'username\']")',

            "password input field in orangehrm login page":
                'page.locator("input[name=\'password\']")',

            "login button in orangehrm login page":
                'page.get_by_role("button", name="Login")',

            # ======================================
            # MENU
            # ======================================

            "pim menu":
                'page.get_by_text("PIM")',

            "admin menu":
                'page.get_by_text("Admin")',

            "leave menu":
                'page.get_by_text("Leave")',

            "dashboard menu":
                'page.get_by_text("Dashboard")',

            # ======================================
            # USER MENU
            # ======================================

            "user dropdown":
                'page.locator(".oxd-userdropdown-tab")',

            "logout button":
                'page.get_by_text("Logout")',

            # ======================================
            # PAGE VERIFICATION
            # ======================================

            "employee list page":
                'page.get_by_text("Employee Information")',

            "login page":
                'page.locator("input[name=\'username\']")'
        }

    # ==========================================
    # CACHE LOAD
    # ==========================================

    def load_cache(self):

        if os.path.exists(self.cache_file):

            try:

                with open(
                    self.cache_file,
                    "r"
                ) as f:

                    return json.load(f)

            except Exception:

                return {}

        return {}

    # ==========================================
    # CACHE SAVE
    # ==========================================

    def save_cache(self):

        with open(
            self.cache_file,
            "w"
        ) as f:

            json.dump(
                self.locator_cache,
                f,
                indent=4
            )

    # ==========================================
    # MAIN LOCATOR METHOD
    # ==========================================

    def get_locator(self, element_description):

        element_description = (
            element_description.strip()
        )

        print(
            f"Generating locator for: {element_description}"
        )

        # ==========================================
        # STEP 1 — STATIC KNOWN LOCATORS
        # ==========================================

        static_locators = {

            "username input field in orangehrm login page":
                'page.locator("input[name=\'username\']")',

            "password input field in orangehrm login page":
                'page.locator("input[name=\'password\']")',

            "login button in orangehrm login page":
                'page.get_by_role("button", name="Login")',

            "pim menu":
                'page.get_by_text("PIM")',

            "recruitment menu":
                'page.get_by_text("Recruitment")',

            # "personal details page":
            #     'page.get_by_role("heading", name="Personal Details")',
            #
            # "login page":
            #     'page.get_by_text("Login")',
            #
            # "user dropdown menu":
            #     'page.locator(".oxd-userdropdown-tab")',
            #
            # "logout button":
            #     'page.get_by_text("Logout")',
        }

        key = element_description.lower()

        if key in static_locators:
            locator = static_locators[key]

            print(
                f"Using Static Locator: {locator}"
            )
            ai_metrics.static_locators += 1
            return locator

        # ==========================================
        # STEP 2 — CACHE
        # ==========================================

        if element_description in self.locator_cache:
            ai_metrics.cache_hits += 1

            locator = self.locator_cache[
                element_description
            ]

            print(
                f"CACHE HIT : "
                f"{element_description}"
            )

            return locator


        # ==========================================
        # STEP 3 — AI LOCATOR
        # ==========================================

        from utils.gemini_helper import (
            generate_locator
        )

        ai_locator = generate_locator(
            element_description
        )
        if ai_locator:
            ai_metrics.ai_generated += 1
        print(
            f"AI Locator: {ai_locator}"
        )

        candidates = []

        if ai_locator:
            candidates.append(ai_locator)

        # ==========================================
        # STEP 4 — SEMANTIC ENGINE
        # ==========================================

        semantic_locator = (
            self.semantic.smart_find(
                element_description
            )
        )

        if semantic_locator:
            ai_metrics.ai_generated += 1
            print(
                f"Semantic Locator: "
                f"{semantic_locator}"
            )

            candidates.append(
                semantic_locator
            )

        # ==========================================
        # STEP 5 — FALLBACK HEALING
        # ==========================================

        fallback_locators = (
            self.healing.generate_fallbacks(
                element_description
            )
        )

        candidates.extend(
            fallback_locators
        )

        # REMOVE DUPLICATES

        candidates = list(
            dict.fromkeys(candidates)
        )

        print("\nLocator Candidates:")

        for candidate in candidates:
            print(candidate)

        # ==========================================
        # STEP 6 — RANK LOCATORS
        # ==========================================

        best_locator = self.ranker.rank(
            candidates
        )

        # ==========================================
        # STEP 7 — VALIDATE
        # ==========================================

        if best_locator:

            try:

                obj = eval(
                    best_locator,
                    {"page": self.page}
                )

                if obj.count() > 0:
                    fallback_set = set(
                        fallback_locators
                    )

                    if best_locator in fallback_set:
                        ai_metrics.healed += 1

                        generic_locators = [

                            'page.locator("input")',
                            'page.locator("button")',
                            'page.locator("div")',
                            'page.locator("span")'
                        ]

                        locator_type = (

                            "GENERIC"

                            if best_locator in generic_locators

                            else "SMART"
                        )

                        self.healing_history.append({

                            "element": element_description,

                            "healed_locator": best_locator,

                            "status": "SUCCESS",

                            "locator_type": locator_type

                        })
                        print(
                            f"[HEAL] {element_description}"
                        )
                        print(
                            f"Locator = {best_locator}"
                        )

                        print(
                            f"Type = {locator_type}"
                        )
                        self.healing_logger.info(

                            f"Element={element_description} | "

                            f"Healed Locator={best_locator}"
                        )
                    print(
                        self.healing_history
                    )
                    print(
                        f"\nBest Locator: "
                        f"{best_locator}"
                    )

                    generic_locators = [

                        'page.locator("input")',
                        'page.locator("button")',
                        'page.locator("div")',
                        'page.locator("span")'
                    ]

                    if best_locator not in generic_locators:

                        self.locator_cache[element_description] = best_locator

                        self.save_cache()

                    else:

                        print(
                            f"[CACHE SKIPPED] "
                            f"Generic locator: "
                            f"{best_locator}"
                        )
                    self.locator_logger.info(

                        f"Element={element_description} | "

                        f"Selected Locator={best_locator}"
                    )
                    return best_locator

            except Exception as e:

                print(
                    f"Validation failed: {str(e)}"
                )
        if not best_locator:
            print(
                f"No valid locator found for "
                f"{element_description}"
            )

            ai_metrics.heal_failed += 1

            return None
        # ==========================================
        # STEP 8 — FAILURE SCREENSHOT
        # ==========================================

        self.visual.capture_failure(
            element_description
            .replace(" ", "_")
        )
        ai_metrics.heal_failed += 1
        self.healing_history.append({

            "element": element_description,

            "healed_locator": "Not Found",

            "status": "FAILED"
        })
        self.healing_logger.error(

            f"Element={element_description} | "

            f"Healing Failed"
        )
        print(
            "\nHEALING FAILURE RECORDED:"
        )

        print(
            self.healing_history
        )
        print(
            f"HEALING RECORDED -> "
            f"{element_description}"
        )
        raise Exception(
            f"Unable to identify locator "
            f"for element: "
            f"{element_description}"
        )