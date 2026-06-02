import json
import os


class FailureAnalytics:

    FILE = (
        "reports/failed_elements.json"
    )

    @classmethod
    def load(cls):

        if not os.path.exists(cls.FILE):
            return {}

        try:

            with open(
                    cls.FILE,
                    "r",
                    encoding="utf-8"
            ) as f:

                content = f.read().strip()

                if not content:
                    return {}

                return json.loads(content)

        except Exception:

            return {}

    @classmethod
    def record_failure(
            cls,
            element
    ):

        data = cls.load()

        data[element] = (
                data.get(
                    element,
                    0
                ) + 1
        )

        with open(
                cls.FILE,
                "w",
                encoding="utf-8"
        ) as f:
            json.dump(
                data,
                f,
                indent=4
            )

    @classmethod
    def get_top_failures(
            cls
    ):

        data = cls.load()

        return sorted(

            data.items(),

            key=lambda x: x[1],

            reverse=True

        )[:10]