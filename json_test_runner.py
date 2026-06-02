from datetime import datetime
import json
import traceback
import time

from utils.ai_metrics import ai_metrics
from utils.browser import BrowserManager
from pages.login_page import LoginPage
from utils.action_engine import ActionEngine
from utils.gemini_helper import generate_test_steps
from utils.report_manager import ReportManager
from utils.screenshot_helper import (
    capture_failure_screenshot
)

from config.settings import (
    BASE_URL,
    USERNAME,
    PASSWORD
)

# ==========================================
# LOAD TEST SCENARIOS
# ==========================================

with open(
    "test_scenarios.json",
    "r",
    encoding="utf-8"
) as file:

    test_scenarios = json.load(file)

# ==========================================
# SUITE FILTERING
# ==========================================

import os

suite = os.getenv(
    "SUITE",
    "all"
).lower()

if suite != "all":

    test_scenarios = [

        test

        for test in test_scenarios

        if suite in [

            tag.lower()

            for tag in test.get(
                "tags",
                []
            )
        ]
    ]

print(
    f"[SUITE] {suite}"
)

print(
    f"[TESTS SELECTED] "
    f"{len(test_scenarios)}"
)

# ==========================================
# REPORT MANAGER
# ==========================================

report = ReportManager(

    browser=os.getenv(
        "BROWSER",
        "chrome"
    ),

    environment=os.getenv(
        "ENVIRONMENT",
        "qa"
    ).upper(),

    framework="Playwright + Gemini AI",

    execution_mode="AI Dynamic"

)

# ==========================================
# SUMMARY VARIABLES
# ==========================================

total_tests = len(test_scenarios)

passed_tests = 0

failed_tests = 0

suite_start_time = time.time()

print("\n================================")
print("AI TEST EXECUTION STARTED")
print("================================")

# ==========================================
# EXECUTE TESTS
# ==========================================

for test in test_scenarios:

    browser = None

    page = None

    engine = None

    test_id = test.get(
        "id",
        "UNKNOWN"
    )

    scenario = test.get(
        "scenario",
        ""
    )

    module = test.get(
        "module",
        "General"
    )

    priority = test.get(
        "priority",
        "Medium"
    )

    print("\n================================")

    print(f"TEST ID   : {test_id}")

    print(f"MODULE    : {module}")

    print(f"PRIORITY  : {priority}")

    print(f"SCENARIO  : {scenario}")

    print("================================")

    test_start_time = time.time()

    try:

        # ==================================
        # BROWSER START
        # ==================================

        browser = BrowserManager()

        page = browser.start()

        # ==================================
        # LOGIN
        # ==================================

        login_page = LoginPage(page)

        login_page.open(
            BASE_URL
        )

        login_page.login(
            USERNAME,
            PASSWORD
        )

        # ==================================
        # GENERATE STEPS
        # ==================================

        steps = generate_test_steps(
            scenario
        )

        print(
            "\nGenerated Steps:\n"
        )

        print(steps)

        # ==================================
        # ACTION ENGINE
        # ==================================

        engine = ActionEngine(
            page,
            test_id=test_id
        )

        engine.execution_steps = []

        engine.locator_history = []

        # ==================================
        # EXECUTE TEST
        # ==================================

        engine.execute(
            steps
        )

        duration = (
            time.time()
            - test_start_time
        )
        print(
            "\nPASSED HEALING HISTORY:"
        )

        print(
            engine.healing_history
        )

        report.add_result(

            testcase_id=test_id,

            scenario=scenario,

            status="PASSED",
            module=module,

            duration=duration,

            steps=engine.execution_steps,

            locator_history=
            engine.locator_history,
            healing_history =
            engine.healing_history,

        )

        passed_tests += 1

        print(
            f"\n{test_id} PASSED"
        )

    except Exception as e:

        duration = (
            time.time()
            - test_start_time
        )

        failed_tests += 1

        error_message = str(e)

        screenshot_path = ""

        execution_steps = []

        locator_history = []

        if engine:

            execution_steps = getattr(
                engine,
                "execution_steps",
                []
            )

            locator_history = getattr(
                engine,
                "locator_history",
                []
            )

        if page:

            screenshot_path = (
                capture_failure_screenshot(
                    page,
                    test_id
                )
            )
        print(
            "\nFAILED HEALING HISTORY:"
        )

        print(
            engine.healing_history
        )
        report.add_result(

            testcase_id=test_id,

            scenario=scenario,

            status="FAILED",
            module=module,

            duration=duration,

            error=error_message,

            screenshot=screenshot_path,

            steps=execution_steps,

            locator_history=
            locator_history,
            healing_history =
            engine.healing_history,
        )

        print(
            f"\n{test_id} FAILED"
        )

        print(
            f"ERROR : {error_message}"
        )

        print(
            f"SCREENSHOT : "
            f"{screenshot_path}"
        )

        traceback.print_exc()

    finally:

        try:

            if browser:

                browser.close()

        except Exception:

            pass

        time.sleep(2)

# ==========================================
# FINAL SUMMARY
# ==========================================

suite_duration = (
    time.time()
    - suite_start_time
)

print("\n================================")

print("FINAL EXECUTION SUMMARY")

print("================================")

print(
    f"TOTAL TESTS : {total_tests}"
)

print(
    f"PASSED      : {passed_tests}"
)

print(
    f"FAILED      : {failed_tests}"
)

print(
    f"EXECUTION TIME : "
    f"{round(suite_duration, 2)} sec"
)

# ==========================================
# GENERATE REPORT
# ==========================================

try:

    report.generate_html_report()
    print("\n========== AI ANALYTICS ==========")

    print(
        ai_metrics.get_summary()
    )

    history_file = "reports/history.json"

    new_entry = {

        "timestamp":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "browser":
            os.getenv(
                "BROWSER",
                "chrome"
            ),

        "environment":
            os.getenv(
                "ENVIRONMENT",
                "qa"
            ),

        "suite":
            os.getenv(
                "SUITE",
                "all"
            ),

        "pass_rate":
            round(
                (passed_tests / total_tests) * 100,
                2
            ),

        "execution_time":
            round(
                suite_duration,
                2
            ),

        "healing_rate":
            ai_metrics.get_summary()[
                "success_rate"
            ]
        }

    history = []

    if os.path.exists(
            history_file
    ):
        with open(
                history_file,
                "r"
        ) as file:
            history = json.load(
                file
            )

    history.append(
        new_entry
    )

    with open(
            history_file,
            "w"
    ) as file:

        json.dump(
            history,
            file,
            indent=4
        )
except Exception as e:

    print(
        f"\nREPORT ERROR : {str(e)}"
    )

# ==========================================
# SUITE STATUS
# ==========================================

if failed_tests == 0:

    print(
        "\n====== TEST SUITE PASSED ======"
    )

else:

    print(
        "\n====== TEST SUITE FAILED ======"
    )

print(
    "\nReport Location:"
)

print(
    "reports/ai_execution_report.html"
)