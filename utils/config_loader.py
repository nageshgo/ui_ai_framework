import json
import os


class ConfigLoader:

    @staticmethod
    def load():

        environment = os.getenv(
            "ENVIRONMENT",
            "qa"
        ).lower()

        config_path = (
            f"config/{environment}.json"
        )

        print(
            f"[CONFIG] Loading: {config_path}"
        )

        with open(
            config_path,
            "r",
            encoding="utf-8"
        ) as file:

            config = json.load(file)

        return config