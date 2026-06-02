# utils/history_manager.py

import json
import os
from datetime import datetime


class HistoryManager:

    FILE_PATH = "reports/history.json"

    @classmethod
    def save_run(
            cls,
            total,
            passed,
            failed,
            pass_rate,
            execution_time,
            ai_metrics
    ):

        os.makedirs(
            "reports",
            exist_ok=True
        )

        record = {

            "timestamp":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "total": total,

            "passed": passed,

            "failed": failed,

            "pass_rate": pass_rate,

            "execution_time":
                execution_time,

            "static":
                ai_metrics["static"],

            "ai_generated":
                ai_metrics["ai_generated"],

            "healed":
                ai_metrics["healed"],

            "heal_failed":
                ai_metrics["heal_failed"]
        }

        history = []

        if os.path.exists(cls.FILE_PATH):

            with open(
                    cls.FILE_PATH,
                    "r",
                    encoding="utf-8"
            ) as f:

                history = json.load(f)

        history.append(record)

        history = history[-20:]

        with open(
                cls.FILE_PATH,
                "w",
                encoding="utf-8"
        ) as f:

            json.dump(
                history,
                f,
                indent=4
            )

    @classmethod
    def load_history(cls):

        if not os.path.exists(
                cls.FILE_PATH
        ):
            return []

        with open(
                cls.FILE_PATH,
                "r",
                encoding="utf-8"
        ) as f:

            return json.load(f)