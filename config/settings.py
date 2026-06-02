import os

from utils.config_loader import (
    ConfigLoader
)

# Load environment config
config = ConfigLoader.load()

BASE_URL = config["base_url"]

USERNAME = config["username"]

PASSWORD = config["password"]

ENVIRONMENT = config["environment"]

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

MODEL_NAME = "gemini-2.5-flash"

print("\n========== SETTINGS ==========")

print(
    f"Environment : {ENVIRONMENT}"
)

print(
    f"Base URL    : {BASE_URL}"
)

print(
    f"Username    : {USERNAME}"
)

print(
    f"Password    : {'*' * len(PASSWORD)}"
)

print("==============================\n")
