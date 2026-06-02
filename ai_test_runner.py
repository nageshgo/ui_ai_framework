import subprocess

from utils.gemini_helper import (
    generate_test_script
)

scenario = input(
    "Enter testcase scenario: "
)

generated_test = generate_test_script(
    scenario
)

file_name = "tests/generated_test.py"

with open(
    file_name,
    "w",
    encoding="utf-8"
) as file:

    file.write(generated_test)

print("\nGenerated Test Script:\n")

print(generated_test)

print("\nRunning pytest...\n")

subprocess.run(
    [
        "pytest",
        file_name,
        "-v"
    ]
)