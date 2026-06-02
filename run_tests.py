import subprocess
import sys

result = subprocess.run(
    [
        sys.executable,
        "json_test_runner.py"
    ]
)

sys.exit(result.returncode)