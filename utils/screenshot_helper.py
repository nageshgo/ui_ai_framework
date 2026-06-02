import os
from datetime import datetime


def capture_failure_screenshot(
        page,
        test_id
):

    try:

        os.makedirs(
            "reports/screenshots",
            exist_ok=True
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        actual_path = (
            f"reports/screenshots/"
            f"{test_id}_{timestamp}.png"
        )

        page.screenshot(
            path=actual_path,
            full_page=True
        )

        print(
            f"Screenshot saved: "
            f"{actual_path}"
        )

        # IMPORTANT:
        # Return path relative to report file

        return (
            f"screenshots/"
            f"{test_id}_{timestamp}.png"
        )

    except Exception as e:

        print(
            f"Screenshot capture failed: "
            f"{str(e)}"
        )

        return ""