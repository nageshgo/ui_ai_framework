import os
import subprocess
import sys

browser = os.getenv(
    "BROWSER",
    "chrome"
)

environment = os.getenv(
    "ENVIRONMENT",
    "qa"
)

print(
    f"Browser={browser}"
)

print(
    f"Environment={environment}"
)


result = subprocess.run(
    [
        sys.executable,
        "json_test_runner.py"
    ]
)

sys.exit(result.returncode)