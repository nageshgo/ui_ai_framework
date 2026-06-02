import os
import subprocess
import sys

from utils.config_loader import (
    ConfigLoader
)

# Load environment configuration
config = ConfigLoader.load()

ENVIRONMENT = config["environment"]
BASE_URL = config["base_url"]
USERNAME = config["username"]

print("\n" + "=" * 60)

print(
    f"[ENVIRONMENT] {ENVIRONMENT}"
)

print(
    f"[URL] {BASE_URL}"
)

print(
    f"[USERNAME] {USERNAME}"
)

print("=" * 60 + "\n")

# Browser from Jenkins parameter
browser = os.getenv(
    "BROWSER",
    "chrome"
)

print(
    f"[BROWSER] {browser}"
)

# Pass values to child process
os.environ["BASE_URL"] = BASE_URL
os.environ["USERNAME"] = USERNAME
os.environ["ENVIRONMENT"] = ENVIRONMENT

browser = os.getenv(
    "BROWSER",
    "chrome"
)

if browser == "all":

    browsers = [
        "chrome",
        "firefox"
    ]

else:

    browsers = [
        browser
    ]

overall_result = 0

for current_browser in browsers:

    print(
        "\n" + "=" * 60
    )

    print(
        f"RUNNING TESTS ON "
        f"{current_browser.upper()}"
    )

    print(
        "=" * 60 + "\n"
    )

    os.environ[
        "BROWSER"
    ] = current_browser

    result = subprocess.run(
        [
            sys.executable,
            "json_test_runner.py"
        ]
    )

    if result.returncode != 0:

        overall_result = (
            result.returncode
        )

sys.exit(
    overall_result
)

sys.exit(
    result.returncode
)