from datetime import datetime
import os
import re
import time
from playwright.sync_api import expect

from agents.locator_agent import LocatorAgent
from utils.failure_analytics import FailureAnalytics
from utils.logger import FrameworkLogger


class ActionEngine:

    def __init__(self, page, test_id=None):

        self.page = page

        self.locator_agent = LocatorAgent(
            self.page
        )
        self.healing_history = (
            self.locator_agent.healing_history
        )
        self.execution_steps = []
        self.locator_history = []
        self.current_test_id = test_id
        self.healing_history = (
            self.locator_agent.healing_history
        )
        self.execution_logger = (
            FrameworkLogger.get_logger(
                "execution",
                "execution.log"
            )
        )

    def execute(self, steps):

        total_steps = len(steps)

        passed_steps = 0

        failed_steps = 0

        failed_step_list = []

        print(
            "\n========== "
            "TEST EXECUTION STARTED "
            "==========\n"
        )

        step_number = 1

        for step in steps:
            step_start_time = time.time()
            try:

                action = step.get(
                    "action",
                    ""
                ).lower()

                element = step.get(
                    "element",
                    ""
                )

                value = step.get(
                    "value",
                    ""
                )

                print(
                    f"\nSTEP {step_number}: "
                    f"{action.upper()} "
                    f"-> {element}"
                )

                # =====================================
                # GET LOCATOR
                # =====================================

                locator = (
                    self.locator_agent
                    .get_locator(element)
                )
                self.locator_history.append({

                    "element": element,

                    "locator": locator

                })

                # =====================================
                # ENTERPRISE AI CLEANUP
                # =====================================

                locator = (
                    locator
                    .replace(
                        "getByRole",
                        "get_by_role"
                    )
                    .replace(
                        "getByText",
                        "get_by_text"
                    )
                    .replace(
                        "getByPlaceholder",
                        "get_by_placeholder"
                    )
                    .replace(
                        "hasPopup",
                        "has_popup"
                    )
                )

                # =====================================
                # REMOVE JS OBJECT STYLE
                # =====================================

                locator = locator.replace(
                    "{ name:",
                    'name='
                )

                # =====================================
                # REMOVE JS REGEX TOKENS
                # =====================================

                locator = locator.replace(
                    "/i",
                    ""
                )

                # =====================================
                # FIX DOUBLE COMMAS
                # =====================================

                locator = locator.replace(
                    ",,",
                    ","
                )

                # =====================================
                # FIX SPACING
                # =====================================

                locator = locator.replace(
                    "name= ",
                    "name="
                )

                # =====================================
                # FIX UNQUOTED NAME VALUES
                # =====================================

                locator = re.sub(
                    r'name=([a-zA-Z0-9_ -]+)',
                    r'name="\1"',
                    locator
                )

                locator = locator.strip()

                print(
                    f"Locator Used: "
                    f"{locator}"
                )

                # =====================================
                # ENTERPRISE SELF-HEALING
                # =====================================

                self.handle_hidden_elements(
                    element
                )

                # =====================================
                # CREATE PLAYWRIGHT LOCATOR
                # =====================================

                if locator.startswith("page."):

                    try:

                        page_locator = eval(
                            locator,
                            {"page": self.page}
                        )

                    except Exception as e:

                        print(
                            "Playwright locator "
                            f"evaluation failed: "
                            f"{str(e)}"
                        )

                        raise e

                else:

                    page_locator = (
                        self.page.locator(
                            locator
                        )
                    )

                # =====================================
                # WAIT FOR ELEMENT
                # =====================================

                page_locator.first.wait_for(
                    state="visible",
                    timeout=30000
                )

                # =====================================
                # CLICK ACTION
                # =====================================

                if action == "click":

                    page_locator.first.click()

                # =====================================
                # FILL ACTION
                # =====================================

                elif action == "fill":

                    page_locator.first.fill(
                        value
                    )

                # =====================================
                # VERIFY ACTION
                # =====================================

                elif action == "verify":

                    expect(
                        page_locator.first
                    ).to_be_visible(
                        timeout=30000
                    )

                # =====================================
                # WAIT ACTION
                # =====================================

                elif action == "wait":

                    time.sleep(
                        int(value)
                    )
                step_duration = round(
                    time.time() - step_start_time,
                    2
                )
                self.execution_steps.append({

                    "step": step_number,

                    "action": action,

                    "element": element,

                    "status": "PASSED",
                    "duration": step_duration
                })
                print(
                    f"STEP {step_number} PASSED"
                )
                self.execution_logger.info(

                    f"{self.current_test_id} | "

                    f"STEP {step_number} | "

                    f"{action.upper()} | "

                    f"{element} | PASSED"
                )
                passed_steps += 1

                step_number += 1

            except Exception as e:
                FailureAnalytics.record_failure(
                    step.get(
                        "element",
                        "Unknown Element"
                    )
                )
                failed_steps += 1

                failed_step_list.append(
                    f"STEP {step_number}: "
                    f"{element}"
                )

                print(
                    f"\nSTEP {step_number} FAILED"
                )
                self.execution_logger.error(

                    f"{self.current_test_id} | "

                    f"STEP {step_number} | "

                    f"{action.upper()} | "

                    f"{element} | FAILED | "

                    f"{str(e)}"
                )
                print(
                    f"ERROR: {str(e)}"
                )

                os.makedirs(
                    "reports/screenshots",
                    exist_ok=True
                )

                timestamp = datetime.now().strftime(
                    "%Y%m%d_%H%M%S"
                )

                screenshot_path = (
                    f"reports/screenshots/"
                    f"{self.current_test_id}_{timestamp}.png"
                )

                self.page.screenshot(
                    path=screenshot_path,
                    full_page=True
                )

                e.screenshot_path = screenshot_path

                import traceback

                traceback.print_exc()
                e.screenshot_path = screenshot_path
                step_duration = round(
                    time.time() - step_start_time,
                    2
                )
                self.execution_steps.append({

                    "step": step_number,

                    "action": action,

                    "element": element,

                    "status": "FAILED",

                    "duration": step_duration,

                    "error": str(e)
                })
                self.healing_history = (
                    self.locator_agent.healing_history
                )
                raise e

        # =====================================
        # FINAL SUMMARY
        # =====================================

        print("\n===================================")
        print("TEST EXECUTION SUMMARY")
        print("===================================")

        print(
            f"TOTAL STEPS   : "
            f"{total_steps}"
        )

        print(
            f"PASSED STEPS  : "
            f"{passed_steps}"
        )

        print(
            f"FAILED STEPS  : "
            f"{failed_steps}"
        )

        if failed_step_list:

            print(
                "\nFAILED STEP DETAILS:"
            )

            for failed in failed_step_list:

                print(failed)
        # Always copy healing history
        self.healing_history = (
            self.locator_agent.healing_history
        )

        print(
            "\nHEALING HISTORY:"
        )
        print(
            self.healing_history
        )
        if failed_steps == 0:

            print(
                "\n========== "
                "TEST EXECUTION PASSED "
                "=========="
            )

        else:

            print(
                "\n========== "
                "TEST EXECUTION FAILED "
                "=========="
            )

    # ==========================================
    # ENTERPRISE SELF-HEALING LOGIC
    # ==========================================

    def handle_hidden_elements(
        self,
        element
    ):

        element = element.lower()

        hidden_element_map = {

            "logout": [
                ".oxd-userdropdown-tab"
            ],

            "my info": [
                ".oxd-main-menu-item"
            ],

            "vacancy": [
                ".oxd-select-text"
            ]
        }

        for key, parent_steps in (
            hidden_element_map.items()
        ):

            if key in element:

                for parent in parent_steps:

                    try:

                        self.page.locator(
                            parent
                        ).first.click()

                        time.sleep(1)

                    except Exception:

                        pass